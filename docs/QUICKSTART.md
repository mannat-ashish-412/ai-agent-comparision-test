# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements_langgraph.txt
```

### Step 2: Set Up Environment

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your API key
notepad .env
```

In `.env`, set:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 3: Run Example

```bash
python example.py
```

## 📝 Your First Agent

Create a file `my_agent.py`:

```python
import asyncio
from langgraph_pydantic_agent import run_agent

async def main():
    result = await run_agent(
        user_request="Create a Python function to calculate fibonacci numbers",
        system_prompt="You are a Python programming expert."
    )
    
    print(result["final_summary"])

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python my_agent.py
```

## 🎯 Configure Models

### Option 1: Environment Variables (Recommended)

Edit `.env`:
```bash
# Use GPT-4o for all agents
DEFAULT_MODEL=openai:gpt-4o

# Or customize per agent
AGENT_MODELS__PLANNING=openai:gpt-4o
AGENT_MODELS__EXECUTION=openai:gpt-4o
AGENT_MODELS__VERIFICATION=openai:gpt-4o-mini  # Cheaper for verification
```

### Option 2: Programmatic

```python
from config import update_settings

settings = update_settings(
    default_model="openai:gpt-4o",
    agent_models={
        "verification": "openai:gpt-4o-mini"  # Override just verification
    }
)

result = await run_agent(
    user_request="Your task",
    settings=settings
)
```

## 📊 Monitor Execution

Check the logs:
```bash
# View real-time logs
type logs\agent.log

# Or on Linux/Mac
tail -f logs/agent.log
```

View saved results:
```bash
# Results are saved in outputs/ directory
dir outputs
```

## 🔧 Common Configurations

### Fast & Cheap (Testing)

```bash
DEFAULT_MODEL=openai:gpt-4o-mini
TASK_CONFIG__MAX_ATTEMPTS=2
TASK_CONFIG__MAX_ITERATIONS=5
ENABLE_CHECKPOINTING=false
```

### Production (Robust)

```bash
DEFAULT_MODEL=openai:gpt-4o
TASK_CONFIG__MAX_ATTEMPTS=3
TASK_CONFIG__MAX_ITERATIONS=20
ENABLE_CHECKPOINTING=true
LOG_LEVEL=INFO
```

### Cost-Optimized

```bash
AGENT_MODELS__PLANNING=openai:gpt-4o
AGENT_MODELS__DECOMPOSITION=openai:gpt-4o
AGENT_MODELS__EXECUTION=openai:gpt-4o
AGENT_MODELS__VERIFICATION=openai:gpt-4o-mini  # Cheaper
AGENT_MODELS__FINAL_VERIFICATION=openai:gpt-4o-mini  # Cheaper
```

## 📚 Next Steps

1. Read the full [README](LANGGRAPH_AGENT_README.md)
2. Explore [example.py](example.py) for more examples
3. Customize agents in [langgraph_pydantic_agent.py](langgraph_pydantic_agent.py)
4. Add your own tools and capabilities

## ❓ Troubleshooting

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
pip install -r requirements_langgraph.txt
```

**Problem**: `ValueError: OPENAI_API_KEY is required`
```bash
# Solution: Set API key in .env
OPENAI_API_KEY=sk-your-key-here
```

**Problem**: Tasks not executing
```bash
# Solution: Check logs
type logs\agent.log
```

## 🎉 You're Ready!

Start building complex AI agents with LangGraph + PydanticAI!
