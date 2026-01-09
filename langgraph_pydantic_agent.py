"""
Production-Ready LangGraph + PydanticAI Agent System
A complex task execution system using LangGraph for flow control and PydanticAI for agent nodes.
"""

from typing import Annotated, Literal, TypedDict, Optional, Any
from datetime import datetime
from enum import Enum
from pathlib import Path
import json
import asyncio
from contextlib import asynccontextmanager

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel, Field, ValidationError
from pydantic_ai import Agent, RunContext

from config import get_settings, Settings
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)


# ============================================================================
# MODELS & STATE
# ============================================================================

class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class Task(BaseModel):
    """Represents a single task in the execution plan."""
    id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed task description")
    dependencies: list[str] = Field(default_factory=list, description="List of task IDs this task depends on")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current task status")
    is_executable: bool = Field(default=False, description="Whether task can be directly executed")
    result: Optional[str] = Field(default=None, description="Task execution result")
    error: Optional[str] = Field(default=None, description="Error message if task failed")
    attempt_count: int = Field(default=0, ge=0, description="Number of execution attempts")
    max_attempts: int = Field(default=3, ge=1, le=10, description="Maximum execution attempts")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def update_status(self, status: TaskStatus) -> None:
        """Update task status and timestamp."""
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def mark_completed(self, result: str) -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.updated_at = datetime.utcnow()
    
    def mark_failed(self, error: str) -> None:
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.error = error
        self.updated_at = datetime.utcnow()
    
    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.attempt_count < self.max_attempts


class AgentState(TypedDict):
    """State shared across all nodes in the LangGraph."""
    user_request: str
    system_prompt: str
    tasks: list[Task]
    current_task_id: Optional[str]
    execution_results: dict[str, str]
    final_summary: Optional[str]
    error_message: Optional[str]
    iteration_count: int
    max_iterations: int
    start_time: datetime
    metadata: dict[str, Any]


class PlanningResult(BaseModel):
    """Structured output from planning agent."""
    tasks: list[Task]
    reasoning: str


class DecompositionResult(BaseModel):
    """Structured output from decomposition agent."""
    subtasks: list[Task]
    reasoning: str


class VerificationResult(BaseModel):
    """Structured output from verification agent."""
    passed: bool
    reasoning: str
    suggestions: Optional[str] = None


class FinalVerificationResult(BaseModel):
    """Structured output from final verification agent."""
    complete: bool
    needs_replan: bool
    reasoning: str
    summary: str


# ============================================================================
# AGENT FACTORY
# ============================================================================

class AgentFactory:
    """Factory for creating configured PydanticAI agents."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        logger.info("Initializing AgentFactory with settings")
    
    def create_planning_agent(self) -> Agent:
        """Create planning agent with configured model."""
        model = self.settings.get_model_for_agent("planning")
        logger.info(f"Creating planning agent with model: {model}")
        
        return Agent(
            model,
            result_type=PlanningResult,
            system_prompt="""You are a strategic planning agent. Your role is to:
            1. Analyze the user's request thoroughly
            2. Break it down into high-level, logical tasks
            3. Identify dependencies between tasks
            4. Determine which tasks are directly executable vs need decomposition
            
            Guidelines:
            - Create tasks with unique IDs (use format: task_001, task_002, etc.)
            - Each task should have a clear, specific description
            - Mark tasks as executable ONLY if they can be directly executed without further breakdown
            - Identify all dependencies accurately
            - Keep the plan at a high level - avoid too much detail
            
            Return a structured plan with tasks and your reasoning.
            """,
        )
    
    def create_decomposition_agent(self) -> Agent:
        """Create decomposition agent with configured model."""
        model = self.settings.get_model_for_agent("decomposition")
        logger.info(f"Creating decomposition agent with model: {model}")
        
        return Agent(
            model,
            result_type=DecompositionResult,
            system_prompt="""You are a task decomposition agent. Your role is to:
            1. Take a complex, non-executable task
            2. Break it down into smaller, executable subtasks
            3. Identify dependencies between subtasks
            4. Ensure each subtask is concrete and actionable
            
            Guidelines:
            - Use results from dependency tasks to inform your decomposition
            - Create subtasks with unique IDs (use parent_id as prefix: task_001_sub_001)
            - Each subtask should be specific, measurable, and executable
            - Mark all subtasks as executable=True
            - Maintain logical dependencies
            
            Return structured subtasks and your reasoning.
            """,
        )
    
    def create_execution_agent(self) -> Agent:
        """Create execution agent with configured model."""
        model = self.settings.get_model_for_agent("execution")
        logger.info(f"Creating execution agent with model: {model}")
        
        return Agent(
            model,
            system_prompt="""You are a task execution agent. Your role is to:
            1. Execute the given task based on its description
            2. Use available tools to complete the task
            3. Provide clear, detailed results
            4. Report any errors or issues encountered
            
            Guidelines:
            - Be thorough and precise in your execution
            - Use dependency results when available
            - Provide structured, actionable output
            - If you encounter errors, explain them clearly
            
            Return the execution result as a string.
            """,
        )
    
    def create_verification_agent(self) -> Agent:
        """Create verification agent with configured model."""
        model = self.settings.get_model_for_agent("verification")
        logger.info(f"Creating verification agent with model: {model}")
        
        return Agent(
            model,
            result_type=VerificationResult,
            system_prompt="""You are a verification agent. Your role is to:
            1. Review the execution result of a task
            2. Verify it meets the task requirements
            3. Check for correctness and completeness
            4. Provide clear pass/fail assessment
            
            Guidelines:
            - Be strict but fair in your verification
            - Check if the result actually addresses the task description
            - If failed, provide specific suggestions for improvement
            - Consider the context and dependencies
            
            Return a structured verification result.
            """,
        )
    
    def create_final_verification_agent(self) -> Agent:
        """Create final verification agent with configured model."""
        model = self.settings.get_model_for_agent("final_verification")
        logger.info(f"Creating final verification agent with model: {model}")
        
        return Agent(
            model,
            result_type=FinalVerificationResult,
            system_prompt="""You are a final verification agent. Your role is to:
            1. Review all completed tasks
            2. Verify the overall goal has been achieved
            3. Identify any gaps or issues
            4. Determine if replanning is needed or if we're done
            
            Guidelines:
            - Assess if the original user request has been fully satisfied
            - Check for completeness and quality
            - If gaps exist, recommend replanning
            - Provide a comprehensive summary
            
            Return a structured final verification result.
            """,
        )


# ============================================================================
# LANGGRAPH NODES
# ============================================================================

class AgentNodes:
    """Container for all LangGraph node functions."""
    
    def __init__(self, agent_factory: AgentFactory, settings: Settings):
        self.factory = agent_factory
        self.settings = settings
        
        # Initialize agents
        self.planning_agent = agent_factory.create_planning_agent()
        self.decomposition_agent = agent_factory.create_decomposition_agent()
        self.execution_agent = agent_factory.create_execution_agent()
        self.verification_agent = agent_factory.create_verification_agent()
        self.final_verification_agent = agent_factory.create_final_verification_agent()
    
    async def create_plan_node(self, state: AgentState) -> AgentState:
        """Node: Create high-level plan using planning agent."""
        logger.info("=" * 60)
        logger.info("🎯 Creating high-level plan...")
        logger.info("=" * 60)
        
        try:
            result = await self.planning_agent.run(
                f"""User Request: {state['user_request']}
                
                System Context: {state['system_prompt']}
                
                Create a high-level plan to accomplish this request.
                Break it down into logical tasks with dependencies.
                """
            )
            
            # Extract tasks from structured output
            planning_result: PlanningResult = result.data
            tasks = planning_result.tasks
            
            # Set max_attempts from config
            for task in tasks:
                task.max_attempts = self.settings.task_config.max_attempts
            
            state["tasks"] = tasks
            state["iteration_count"] = state.get("iteration_count", 0) + 1
            
            logger.info(f"Created {len(tasks)} high-level tasks")
            logger.info(f"Reasoning: {planning_result.reasoning}")
            
        except Exception as e:
            logger.error(f"Error in create_plan_node: {e}", exc_info=True)
            state["error_message"] = f"Planning failed: {str(e)}"
        
        return state
    
    async def select_next_task_node(self, state: AgentState) -> AgentState:
        """Node: Select the next task to execute based on dependencies."""
        logger.info("\n📋 Selecting next task...")
        
        tasks = state["tasks"]
        
        # Find a pending task whose dependencies are all completed
        for task in tasks:
            if task.status != TaskStatus.PENDING:
                continue
            
            # Check if all dependencies are completed
            if task.dependencies:
                dependencies_met = all(
                    any(t.id == dep_id and t.status == TaskStatus.COMPLETED for t in tasks)
                    for dep_id in task.dependencies
                )
                
                if not dependencies_met:
                    continue
            
            # Found a task ready to execute
            state["current_task_id"] = task.id
            task.update_status(TaskStatus.IN_PROGRESS)
            logger.info(f"   ✓ Selected task: {task.title} (ID: {task.id})")
            return state
        
        # No task found
        state["current_task_id"] = None
        logger.info("   ℹ No more tasks to execute")
        return state
    
    async def check_task_executable_node(self, state: AgentState) -> AgentState:
        """Node: Check if current task is executable."""
        current_task = next(
            (t for t in state["tasks"] if t.id == state["current_task_id"]),
            None
        )
        
        if current_task:
            logger.info(f"\n🔍 Checking task: {current_task.title}")
            logger.info(f"   Executable: {current_task.is_executable}")
        
        return state
    
    async def decompose_task_node(self, state: AgentState) -> AgentState:
        """Node: Decompose non-executable task into smaller tasks."""
        logger.info("\n🔨 Decomposing task into subtasks...")
        
        current_task = next(
            (t for t in state["tasks"] if t.id == state["current_task_id"]),
            None
        )
        
        if not current_task:
            logger.warning("No current task found for decomposition")
            return state
        
        try:
            # Gather results from dependency tasks
            dependency_results = {
                dep_id: state["execution_results"].get(dep_id, "No result available")
                for dep_id in current_task.dependencies
            }
            
            result = await self.decomposition_agent.run(
                f"""Task to decompose:
                ID: {current_task.id}
                Title: {current_task.title}
                Description: {current_task.description}
                
                Dependency Results:
                {json.dumps(dependency_results, indent=2)}
                
                Break this down into smaller, executable subtasks.
                Each subtask should be marked as executable=True.
                """
            )
            
            decomposition_result: DecompositionResult = result.data
            subtasks = decomposition_result.subtasks
            
            # Set max_attempts from config
            for subtask in subtasks:
                subtask.max_attempts = self.settings.task_config.max_attempts
            
            # Remove the current task and add subtasks
            state["tasks"] = [t for t in state["tasks"] if t.id != current_task.id]
            state["tasks"].extend(subtasks)
            
            logger.info(f"   ✓ Created {len(subtasks)} subtasks")
            logger.info(f"   Reasoning: {decomposition_result.reasoning}")
            
        except Exception as e:
            logger.error(f"Error in decompose_task_node: {e}", exc_info=True)
            current_task.mark_failed(f"Decomposition failed: {str(e)}")
        
        return state
    
    async def execute_task_node(self, state: AgentState) -> AgentState:
        """Node: Execute the current task."""
        logger.info("\n⚙️ Executing task...")
        
        current_task = next(
            (t for t in state["tasks"] if t.id == state["current_task_id"]),
            None
        )
        
        if not current_task:
            logger.warning("No current task found for execution")
            return state
        
        logger.info(f"   Task: {current_task.title}")
        logger.info(f"   Attempt: {current_task.attempt_count + 1}/{current_task.max_attempts}")
        
        # Gather dependency results
        dependency_results = {
            dep_id: state["execution_results"].get(dep_id, "No result available")
            for dep_id in current_task.dependencies
        }
        
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self.execution_agent.run(
                    f"""Execute this task:
                    Title: {current_task.title}
                    Description: {current_task.description}
                    
                    Dependency Results:
                    {json.dumps(dependency_results, indent=2)}
                    
                    Execute the task and provide detailed results.
                    """
                ),
                timeout=self.settings.task_config.execution_timeout
            )
            
            current_task.result = str(result.data)
            current_task.attempt_count += 1
            logger.info(f"   ✓ Execution completed")
            
        except asyncio.TimeoutError:
            error_msg = f"Execution timeout after {self.settings.task_config.execution_timeout}s"
            current_task.error = error_msg
            current_task.attempt_count += 1
            logger.error(f"   ❌ {error_msg}")
            
        except Exception as e:
            current_task.error = str(e)
            current_task.attempt_count += 1
            logger.error(f"   ❌ Execution error: {e}", exc_info=True)
        
        return state
    
    async def verify_execution_node(self, state: AgentState) -> AgentState:
        """Node: Verify task execution."""
        logger.info("\n✅ Verifying execution...")
        
        current_task = next(
            (t for t in state["tasks"] if t.id == state["current_task_id"]),
            None
        )
        
        if not current_task:
            logger.warning("No current task found for verification")
            return state
        
        try:
            result = await self.verification_agent.run(
                f"""Verify this task execution:
                Task: {current_task.title}
                Description: {current_task.description}
                Result: {current_task.result}
                Error: {current_task.error}
                
                Does this meet the requirements?
                """
            )
            
            verification_result: VerificationResult = result.data
            
            if verification_result.passed:
                current_task.mark_completed(current_task.result or "")
                state["execution_results"][current_task.id] = current_task.result or ""
                logger.info(f"   ✅ Task verified successfully")
                logger.info(f"   Reasoning: {verification_result.reasoning}")
            else:
                logger.warning(f"   ❌ Verification failed: {verification_result.reasoning}")
                
                if current_task.can_retry():
                    current_task.update_status(TaskStatus.PENDING)
                    logger.info(f"   🔄 Task will be retried (attempt {current_task.attempt_count}/{current_task.max_attempts})")
                else:
                    current_task.mark_failed(f"Verification failed: {verification_result.reasoning}")
                    state["error_message"] = f"Task '{current_task.title}' failed after {current_task.max_attempts} attempts"
                    logger.error(f"   ❌ Task failed after max attempts")
        
        except Exception as e:
            logger.error(f"Error in verify_execution_node: {e}", exc_info=True)
            current_task.mark_failed(f"Verification error: {str(e)}")
        
        return state
    
    async def final_verification_node(self, state: AgentState) -> AgentState:
        """Node: Final verification of all tasks."""
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Final verification...")
        logger.info("=" * 60)
        
        completed_tasks = [t for t in state["tasks"] if t.status == TaskStatus.COMPLETED]
        failed_tasks = [t for t in state["tasks"] if t.status == TaskStatus.FAILED]
        
        try:
            result = await self.final_verification_agent.run(
                f"""Review the completed work:
                
                Original Request: {state['user_request']}
                
                Completed Tasks ({len(completed_tasks)}):
                {json.dumps([{'title': t.title, 'result': t.result} for t in completed_tasks], indent=2)}
                
                Failed Tasks ({len(failed_tasks)}):
                {json.dumps([{'title': t.title, 'error': t.error} for t in failed_tasks], indent=2)}
                
                Has the original request been fully satisfied?
                Should we replan and continue, or are we done?
                """
            )
            
            final_result: FinalVerificationResult = result.data
            state["final_summary"] = final_result.summary
            state["metadata"]["final_verification"] = final_result.model_dump()
            
            logger.info(f"Complete: {final_result.complete}")
            logger.info(f"Needs Replan: {final_result.needs_replan}")
            logger.info(f"Reasoning: {final_result.reasoning}")
            
        except Exception as e:
            logger.error(f"Error in final_verification_node: {e}", exc_info=True)
            state["error_message"] = f"Final verification failed: {str(e)}"
        
        return state
    
    async def generate_summary_node(self, state: AgentState) -> AgentState:
        """Node: Generate final summary for user."""
        logger.info("\n" + "=" * 60)
        logger.info("📊 Generating final summary...")
        logger.info("=" * 60)
        
        completed_tasks = [t for t in state["tasks"] if t.status == TaskStatus.COMPLETED]
        failed_tasks = [t for t in state["tasks"] if t.status == TaskStatus.FAILED]
        
        execution_time = (datetime.utcnow() - state["start_time"]).total_seconds()
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    EXECUTION SUMMARY                         ║
╚══════════════════════════════════════════════════════════════╝

📋 Original Request:
{state['user_request']}

📊 Statistics:
   • Completed Tasks: {len(completed_tasks)}
   • Failed Tasks: {len(failed_tasks)}
   • Total Iterations: {state['iteration_count']}
   • Execution Time: {execution_time:.2f}s

────────────────────────────────────────────────────────────────
✅ COMPLETED TASKS:
────────────────────────────────────────────────────────────────
"""
        
        for i, task in enumerate(completed_tasks, 1):
            summary += f"\n{i}. {task.title}\n"
            summary += f"   Result: {task.result[:200]}{'...' if len(task.result or '') > 200 else ''}\n"
        
        if failed_tasks:
            summary += "\n────────────────────────────────────────────────────────────────"
            summary += "\n❌ FAILED TASKS:"
            summary += "\n────────────────────────────────────────────────────────────────\n"
            for i, task in enumerate(failed_tasks, 1):
                summary += f"\n{i}. {task.title}\n"
                summary += f"   Error: {task.error}\n"
        
        summary += "\n────────────────────────────────────────────────────────────────"
        summary += f"\n📝 Final Assessment:\n{state.get('final_summary', 'N/A')}"
        summary += "\n════════════════════════════════════════════════════════════════"
        
        state["final_summary"] = summary
        logger.info(summary)
        
        return state


# ============================================================================
# ROUTING FUNCTIONS
# ============================================================================

def route_after_task_selection(state: AgentState) -> Literal["check_executable", "final_verification"]:
    """Route after task selection."""
    if state["current_task_id"] is None:
        return "final_verification"
    return "check_executable"


def route_after_executable_check(state: AgentState) -> Literal["execute", "decompose"]:
    """Route based on whether task is executable."""
    current_task = next(
        (t for t in state["tasks"] if t.id == state["current_task_id"]),
        None
    )
    
    if current_task and current_task.is_executable:
        return "execute"
    return "decompose"


def route_after_verification(state: AgentState) -> Literal["select_next", "error_end"]:
    """Route after verification."""
    if state.get("error_message"):
        current_task = next(
            (t for t in state["tasks"] if t.id == state["current_task_id"]),
            None
        )
        # Only end on error if task truly failed (not just needs retry)
        if current_task and current_task.status == TaskStatus.FAILED:
            return "error_end"
    return "select_next"


def route_after_final_verification(state: AgentState) -> Literal["replan", "summary"]:
    """Route after final verification."""
    metadata = state.get("metadata", {})
    final_verification = metadata.get("final_verification", {})
    
    # Check iteration limit
    if state["iteration_count"] >= state["max_iterations"]:
        logger.warning(f"Max iterations ({state['max_iterations']}) reached")
        return "summary"
    
    if final_verification.get("needs_replan", False):
        logger.info("Replanning required")
        return "replan"
    
    return "summary"


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_agent_graph(settings: Settings) -> StateGraph:
    """Create and configure the LangGraph workflow."""
    logger.info("Creating agent graph...")
    
    # Initialize factory and nodes
    factory = AgentFactory(settings)
    nodes = AgentNodes(factory, settings)
    
    # Initialize graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("create_plan", nodes.create_plan_node)
    workflow.add_node("select_next", nodes.select_next_task_node)
    workflow.add_node("check_executable", nodes.check_task_executable_node)
    workflow.add_node("decompose", nodes.decompose_task_node)
    workflow.add_node("execute", nodes.execute_task_node)
    workflow.add_node("verify", nodes.verify_execution_node)
    workflow.add_node("final_verification", nodes.final_verification_node)
    workflow.add_node("summary", nodes.generate_summary_node)
    
    # Set entry point
    workflow.set_entry_point("create_plan")
    
    # Add edges
    workflow.add_edge("create_plan", "select_next")
    workflow.add_edge("decompose", "select_next")
    workflow.add_edge("execute", "verify")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "select_next",
        route_after_task_selection,
        {
            "check_executable": "check_executable",
            "final_verification": "final_verification"
        }
    )
    
    workflow.add_conditional_edges(
        "check_executable",
        route_after_executable_check,
        {
            "execute": "execute",
            "decompose": "decompose"
        }
    )
    
    workflow.add_conditional_edges(
        "verify",
        route_after_verification,
        {
            "select_next": "select_next",
            "error_end": END
        }
    )
    
    workflow.add_conditional_edges(
        "final_verification",
        route_after_final_verification,
        {
            "replan": "create_plan",
            "summary": "summary"
        }
    )
    
    workflow.add_edge("summary", END)
    
    logger.info("Agent graph created successfully")
    return workflow


# ============================================================================
# CHECKPOINTING
# ============================================================================

def get_checkpointer(settings: Settings):
    """Get the appropriate checkpointer based on settings."""
    if not settings.enable_checkpointing:
        logger.info("Checkpointing disabled, using MemorySaver")
        return MemorySaver()
    
    checkpoint_dir = Path(settings.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = checkpoint_dir / "checkpoints.db"
    logger.info(f"Using SQLite checkpointer at: {db_path}")
    
    return SqliteSaver.from_conn_string(str(db_path))


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def run_agent(
    user_request: str,
    system_prompt: str = "",
    tools: list = None,
    settings: Optional[Settings] = None
) -> AgentState:
    """
    Run the agent with the given request.
    
    Args:
        user_request: The user's task request
        system_prompt: Optional system prompt override
        tools: Optional list of tools to provide to agents
        settings: Optional settings override
    
    Returns:
        Final agent state with results
    """
    # Use provided settings or get global settings
    if settings is None:
        settings = get_settings()
    
    # Validate API keys
    try:
        settings.validate_api_keys()
    except ValueError as e:
        logger.error(f"API key validation failed: {e}")
        raise
    
    # Create graph
    workflow = create_agent_graph(settings)
    
    # Compile with checkpointing
    checkpointer = get_checkpointer(settings)
    app = workflow.compile(checkpointer=checkpointer)
    
    # Initialize state
    initial_state: AgentState = {
        "user_request": user_request,
        "system_prompt": system_prompt or "You are a helpful AI assistant.",
        "tasks": [],
        "current_task_id": None,
        "execution_results": {},
        "final_summary": None,
        "error_message": None,
        "iteration_count": 0,
        "max_iterations": settings.task_config.max_iterations,
        "start_time": datetime.utcnow(),
        "metadata": {},
    }
    
    # Run the graph
    thread_id = f"run_{datetime.utcnow().isoformat()}"
    config = {"configurable": {"thread_id": thread_id}}
    
    logger.info("\n" + "=" * 60)
    logger.info("🤖 STARTING AGENT EXECUTION")
    logger.info("=" * 60)
    logger.info(f"Request: {user_request}")
    logger.info(f"Thread ID: {thread_id}")
    logger.info("=" * 60 + "\n")
    
    final_state = None
    try:
        async for state in app.astream(initial_state, config):
            final_state = state
            # Get the actual state from the dict (it's wrapped)
            if isinstance(state, dict):
                for key, value in state.items():
                    final_state = value
                    break
        
        logger.info("\n" + "=" * 60)
        logger.info("🏁 EXECUTION COMPLETE")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Fatal error during execution: {e}", exc_info=True)
        if final_state is None:
            final_state = initial_state
        final_state["error_message"] = f"Fatal error: {str(e)}"
    
    return final_state


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage of the agent system."""
    
    # Example: Override settings programmatically
    settings = get_settings()
    
    # You can also update specific models
    # settings.agent_models.planning = "openai:gpt-4o"
    # settings.agent_models.verification = "openai:gpt-4o-mini"
    
    # Run the agent
    result = await run_agent(
        user_request="Create a Python web scraper that extracts product data from an e-commerce site and saves it to a database",
        system_prompt="You are a helpful AI assistant specialized in software development.",
        settings=settings
    )
    
    # Check results
    if result.get("error_message"):
        logger.error(f"\n❌ Error: {result['error_message']}")
    else:
        logger.info(f"\n✅ Success!")
        logger.info(f"\nFinal Summary:\n{result.get('final_summary', 'No summary available')}")
    
    # Save results to file
    output_dir = Path("./outputs")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"result_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Convert tasks to dict for JSON serialization
    result_dict = dict(result)
    result_dict["tasks"] = [t.model_dump() for t in result.get("tasks", [])]
    result_dict["start_time"] = result["start_time"].isoformat()
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_dict, f, indent=2, default=str)
    
    logger.info(f"\n💾 Results saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
