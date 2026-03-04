# Production-Ready LangGraph + PydanticAI Agent System

A sophisticated, production-ready AI agent system that combines **LangGraph** for workflow orchestration with **PydanticAI** agents as execution nodes. This system handles complex, long-running tasks through intelligent planning, decomposition, execution, and verification.

## 🌟 Production Features

### ✅ Centralized Configuration
- **Environment-based settings** via `.env` file
- **Model configuration** from a single source
- **Per-agent model customization** (use different models for different agents)
- **Runtime configuration updates**

### ✅ Robust Error Handling
- **Custom exception classes** for different error types
- **Automatic retry logic** with configurable max attempts
- **Timeout protection** for long-running tasks
- **Graceful degradation** on failures

### ✅ Production Logging
- **Structured logging** with file and console output
- **Configurable log levels**
- **Detailed execution traces**
- **Performance metrics**

### ✅ State Persistence
- **SQLite checkpointing** for long-running workflows
- **State recovery** after failures
- **Execution history** tracking

### ✅ Monitoring & Observability
- **Task statistics** and success rates
- **Execution time tracking**
- **Dependency validation**
- **Task graph visualization**

### ✅ Type Safety
- **Pydantic models** for all data structures
- **Structured outputs** from agents
- **Validation** at every step

## 📁 Project Structure

```
AIAgent/
├── langgraph_pydantic_agent.py  # Main agent system
├── config.py                     # Configuration management
├── logger.py                     # Logging setup
├── exceptions.py                 # Custom exceptions
├── utils.py                      # Utility functions
├── requirements_langgraph.txt    # Dependencies
├── .env.example                  # Example environment file
├── .env                          # Your environment file (create this)
├── checkpoints/                  # SQLite checkpoints (auto-created)
├── logs/                         # Log files (auto-created)
└── outputs/                      # Execution results (auto-created)
```

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements_langgraph.txt

# Copy example env file
copy .env.example .env

# Edit .env with your API keys
notepad .env
```

### 2. Configuration

Edit `.env` file:

```bash
# Required: Set your API key
OPENAI_API_KEY=sk-your-key-here

# Optional: Use different models for different agents
DEFAULT_MODEL=openai:gpt-4o
AGENT_MODELS__PLANNING=openai:gpt-4o
AGENT_MODELS__EXECUTION=openai:gpt-4o
AGENT_MODELS__VERIFICATION=openai:gpt-4o-mini  # Use cheaper model for verification

# Optional: Adjust task settings
TASK_CONFIG__MAX_ATTEMPTS=3
TASK_CONFIG__MAX_ITERATIONS=20
```

### 3. Run the Agent

```python
import asyncio
from langgraph_pydantic_agent import run_agent

async def main():
    result = await run_agent(
        user_request="Your complex task here",
        system_prompt="You are a helpful AI assistant."
    )
    
    print(result["final_summary"])

asyncio.run(main())
```

## 🎯 Usage Examples

### Example 1: Software Development Task

```python
result = await run_agent(
    user_request="""
    Create a REST API with the following features:
    1. User authentication (JWT)
    2. CRUD operations for products
    3. Database integration (PostgreSQL)
    4. API documentation (OpenAPI/Swagger)
    5. Unit tests
    """,
    system_prompt="You are an expert software developer."
)
```

### Example 2: Data Analysis Task

```python
result = await run_agent(
    user_request="""
    Analyze the sales data:
    1. Load data from CSV file
    2. Clean and preprocess data
    3. Perform statistical analysis
    4. Create visualizations (charts, graphs)
    5. Generate a comprehensive report
    """,
    system_prompt="You are a data analyst expert."
)
```

### Example 3: Custom Model Configuration

```python
from config import get_settings, update_settings

# Update settings programmatically
settings = update_settings(
    default_model="openai:gpt-4o",
    agent_models={
        "planning": "openai:gpt-4o",
        "decomposition": "openai:gpt-4o",
        "execution": "openai:gpt-4o",
        "verification": "openai:gpt-4o-mini",  # Cheaper model
        "final_verification": "openai:gpt-4o"
    }
)

result = await run_agent(
    user_request="Your task here",
    settings=settings
)
```

## ⚙️ Configuration Reference

### Model Configuration

Set models from **one place** - either in `.env` or programmatically:

#### Option 1: Environment Variables (.env)

```bash
# Set default model for all agents
DEFAULT_MODEL=openai:gpt-4o

# Override specific agents (optional)
AGENT_MODELS__PLANNING=openai:gpt-4o
AGENT_MODELS__DECOMPOSITION=openai:gpt-4o
AGENT_MODELS__EXECUTION=openai:gpt-4o
AGENT_MODELS__VERIFICATION=openai:gpt-4o-mini
AGENT_MODELS__FINAL_VERIFICATION=openai:gpt-4o
```

#### Option 2: Programmatic Configuration

```python
from config import update_settings

settings = update_settings(
    default_model="openai:gpt-4o",
    agent_models={
        "planning": "openai:gpt-4o",
        "verification": "openai:gpt-4o-mini"
    }
)
```

### Supported Models

```python
# OpenAI
"openai:gpt-4o"
"openai:gpt-4o-mini"
"openai:gpt-4-turbo"

# Anthropic
"anthropic:claude-3-opus-20240229"
"anthropic:claude-3-sonnet-20240229"

# Local (Ollama)
"ollama:llama3"
"ollama:mistral"
```

### Task Configuration

```bash
# Max retry attempts per task
TASK_CONFIG__MAX_ATTEMPTS=3

# Max workflow iterations (prevents infinite loops)
TASK_CONFIG__MAX_ITERATIONS=20

# Task execution timeout (seconds)
TASK_CONFIG__EXECUTION_TIMEOUT=300
```

### Logging Configuration

```bash
# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Log file path (optional)
LOG_FILE=./logs/agent.log
```

### Persistence Configuration

```bash
# Checkpoint directory
CHECKPOINT_DIR=./checkpoints

# Enable/disable checkpointing
ENABLE_CHECKPOINTING=true
```

## 🏗️ Architecture

### Flow Diagram

```
User Request
     ↓
Create Plan (Planning Agent)
     ↓
Select Next Task (based on dependencies)
     ↓
Is Executable? ──No──→ Decompose (Decomposition Agent)
     ↓                        ↓
    Yes                  (back to Select Next)
     ↓
Execute Task (Execution Agent)
     ↓
Verify Execution (Verification Agent)
     ↓
  Success? ──No──→ Retry (up to max attempts)
     ↓                   ↓
    Yes              Failed? → End with Error
     ↓
More Tasks? ──Yes──→ (back to Select Next)
     ↓
    No
     ↓
Final Verification (Final Verification Agent)
     ↓
Need Replan? ──Yes──→ (back to Create Plan)
     ↓
    No
     ↓
Generate Summary → End
```

### Agent Responsibilities

| Agent | Model Config Key | Purpose |
|-------|-----------------|---------|
| **Planning Agent** | `planning` | Creates high-level task plan |
| **Decomposition Agent** | `decomposition` | Breaks complex tasks into subtasks |
| **Execution Agent** | `execution` | Executes individual tasks |
| **Verification Agent** | `verification` | Validates task execution |
| **Final Verification Agent** | `final_verification` | Assesses overall completion |

## 📊 Monitoring & Debugging

### View Execution Logs

```python
# Logs are automatically written to console and file
# Check logs/agent.log for detailed traces
```

### Get Task Statistics

```python
from utils import get_task_statistics

stats = get_task_statistics(result["tasks"])
print(f"Success Rate: {stats['success_rate']}%")
print(f"Total Attempts: {stats['total_attempts']}")
```

### Visualize Task Graph

```python
from utils import generate_task_graph_visualization

dot_content = generate_task_graph_visualization(
    result["tasks"],
    output_file="task_graph.dot"
)

# Render with Graphviz
# dot -Tpng task_graph.dot -o task_graph.png
```

### Save Execution State

```python
from utils import save_state_to_file

filepath = save_state_to_file(result, output_dir="./outputs")
print(f"State saved to: {filepath}")
```

### Validate Dependencies

```python
from utils import validate_task_dependencies

errors = validate_task_dependencies(result["tasks"])
if errors:
    for error in errors:
        print(f"⚠️ {error}")
```

## 🔧 Advanced Usage

### Custom Tools

Add custom tools to agents:

```python
from pydantic_ai import Tool, RunContext

def search_web(ctx: RunContext, query: str) -> str:
    """Search the web for information."""
    # Your implementation
    return f"Search results for: {query}"

def write_file(ctx: RunContext, filename: str, content: str) -> str:
    """Write content to a file."""
    # Your implementation
    return f"Written to {filename}"

# Add tools when creating agents
# (Modify AgentFactory in langgraph_pydantic_agent.py)
```

### Custom State Fields

Extend the state for your needs:

```python
class CustomAgentState(AgentState):
    custom_field: str
    additional_data: dict[str, Any]
```

### Error Handling

```python
from exceptions import (
    TaskExecutionError,
    MaxRetriesExceededError,
    ConfigurationError
)

try:
    result = await run_agent(user_request="...")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except MaxRetriesExceededError as e:
    print(f"Task {e.task_id} failed after {e.max_attempts} attempts")
```

## 🧪 Testing

```python
# Run with test configuration
from config import Settings, TaskConfig

test_settings = Settings(
    default_model="openai:gpt-4o-mini",  # Cheaper for testing
    task_config=TaskConfig(
        max_attempts=2,
        max_iterations=5
    ),
    enable_checkpointing=False  # Faster for tests
)

result = await run_agent(
    user_request="Simple test task",
    settings=test_settings
)
```

## 📈 Performance Optimization

### Use Cheaper Models for Simple Tasks

```bash
# Use GPT-4o for complex reasoning
AGENT_MODELS__PLANNING=openai:gpt-4o
AGENT_MODELS__DECOMPOSITION=openai:gpt-4o

# Use GPT-4o-mini for verification (cheaper)
AGENT_MODELS__VERIFICATION=openai:gpt-4o-mini
```

### Adjust Timeouts

```bash
# Reduce timeout for faster tasks
TASK_CONFIG__EXECUTION_TIMEOUT=60
```

### Disable Checkpointing for Short Tasks

```bash
ENABLE_CHECKPOINTING=false
```

## 🐛 Troubleshooting

### Issue: API Key Error

```
ValueError: OPENAI_API_KEY is required for OpenAI models
```

**Solution**: Set your API key in `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### Issue: Import Errors

```
ModuleNotFoundError: No module named 'pydantic_ai'
```

**Solution**: Install dependencies:
```bash
pip install -r requirements_langgraph.txt
```

### Issue: Tasks Not Executing

**Check**:
1. Task dependencies are correctly defined
2. `is_executable` flag is set properly
3. Review logs for errors

### Issue: Infinite Loops

**Solution**: Adjust max iterations:
```bash
TASK_CONFIG__MAX_ITERATIONS=10
```

## 📝 Best Practices

1. **Clear Task Descriptions**: Provide detailed, specific task descriptions
2. **Proper Dependencies**: Clearly define task dependencies
3. **Model Selection**: Use appropriate models for each agent type
4. **Monitor Logs**: Watch execution logs for issues
5. **Validate Dependencies**: Check for circular dependencies
6. **Set Timeouts**: Configure appropriate timeouts for your tasks
7. **Use Checkpointing**: Enable for long-running workflows
8. **Save Results**: Persist execution results for analysis

## 📄 License

This is a production-ready template - customize and use as needed for your projects!

## 🤝 Contributing

Extend and improve this template for your specific use cases.

---

**Built with ❤️ using LangGraph and PydanticAI**
