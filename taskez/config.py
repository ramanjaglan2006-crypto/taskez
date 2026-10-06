import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    app_name: str = "TaskEZ Autonomous Agent Engine"
    version: str = "1.0.0"
    debug: bool = True
    
    # LLM Settings (Supports hybrid autonomous heuristic engine or external LLM API if key provided)
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    
    # Execution timeouts and retries
    max_retries_per_step: int = 3
    tool_timeout_seconds: float = 10.0
    
    # Default failure injection setting for testing/demoing
    inject_failures_by_default: bool = False

settings = Settings()
