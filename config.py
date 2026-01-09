"""
Configuration management for LangGraph + PydanticAI Agent System
"""

from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class AgentModelConfig(BaseModel):
    """Configuration for individual agent models."""

    planning: str = Field(
        default="openai:gpt-4o", description="Model for planning agent"
    )
    decomposition: str = Field(
        default="openai:gpt-4o", description="Model for decomposition agent"
    )
    execution: str = Field(
        default="openai:gpt-4o", description="Model for execution agent"
    )
    verification: str = Field(
        default="openai:gpt-4o", description="Model for verification agent"
    )
    final_verification: str = Field(
        default="openai:gpt-4o", description="Model for final verification agent"
    )


class TaskConfig(BaseModel):
    """Configuration for task execution."""

    max_attempts: int = Field(
        default=3, ge=1, le=10, description="Max retry attempts per task"
    )
    max_iterations: int = Field(
        default=20, ge=1, le=100, description="Max workflow iterations"
    )
    execution_timeout: int = Field(
        default=300, ge=10, le=3600, description="Task execution timeout in seconds"
    )


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # API Keys
    openai_api_key: Optional[str] = Field(
        default=None, validation_alias="OPENAI_API_KEY"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None, validation_alias="ANTHROPIC_API_KEY"
    )

    # Model Configuration
    default_model: str = Field(
        default="openai:gpt-4o", description="Default model for all agents"
    )
    agent_models: AgentModelConfig = Field(default_factory=AgentModelConfig)

    # Task Configuration
    task_config: TaskConfig = Field(default_factory=TaskConfig)

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")

    # Persistence
    checkpoint_dir: str = Field(
        default="./checkpoints", description="Directory for checkpoints"
    )
    enable_checkpointing: bool = Field(
        default=True, description="Enable state checkpointing"
    )

    # Performance
    enable_streaming: bool = Field(
        default=False, description="Enable streaming responses"
    )
    max_concurrent_tasks: int = Field(
        default=1, ge=1, le=10, description="Max concurrent task execution"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    def get_model_for_agent(self, agent_type: str) -> str:
        """Get the model configuration for a specific agent type."""
        return getattr(self.agent_models, agent_type, self.default_model)

    def validate_api_keys(self) -> bool:
        """Validate that required API keys are present."""
        model_prefix = self.default_model.split(":")[0]

        if model_prefix == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI models")
        elif model_prefix == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required for Anthropic models")

        return True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def update_settings(**kwargs) -> Settings:
    """Update settings programmatically."""
    global settings
    for key, value in kwargs.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    return settings
