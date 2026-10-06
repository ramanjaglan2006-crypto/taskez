from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import datetime

class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"

class EventType(str, Enum):
    PLANNING_START = "planning_start"
    PLAN_CREATED = "plan_created"
    STEP_START = "step_start"
    TOOL_CALL = "tool_call"
    TOOL_OUTPUT = "tool_output"
    STEP_SUCCESS = "step_success"
    STEP_FAILURE = "step_failure"
    SELF_CORRECTION = "self_correction"
    REPLANNING = "replanning"
    FINAL_REPORT = "final_report"
    ERROR = "error"

class ToolCallSpec(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    rationale: str

class ToolResultSpec(BaseModel):
    success: bool
    tool_name: str
    output: Any
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    recovered_via_fallback: bool = False

class Step(BaseModel):
    id: int
    title: str
    description: str
    assigned_tool: str
    tool_args: Dict[str, Any] = Field(default_factory=dict)
    status: StepStatus = StepStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    attempts: int = 0
    max_attempts: int = 3
    sub_steps: List[str] = Field(default_factory=list)
    recovery_notes: Optional[str] = None

class Plan(BaseModel):
    goal: str
    domain: str
    thought_process: str
    steps: List[Step]
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class TraceEvent(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    event_type: EventType
    step_id: Optional[int] = None
    message: str
    details: Optional[Dict[str, Any]] = None

class AgentReport(BaseModel):
    goal: str
    domain: str
    summary: str
    plan_overview: List[str]
    steps_executed: int
    successful_steps: int
    failed_steps: int
    self_corrections_made: int
    key_findings: List[Dict[str, Any]]
    final_output: Any
    execution_trace: List[TraceEvent]
    total_duration_seconds: float
