import time
import abc
from typing import Any, Dict, Optional
from taskez.core.state import ToolResultSpec

class BaseTool(abc.ABC):
    name: str
    description: str
    
    def __init__(self, simulate_failure: bool = False, failure_type: Optional[str] = None):
        """
        :param simulate_failure: If True, tool deliberately triggers an error for robustness/self-correction demo.
        :param failure_type: "timeout", "invalid_response", "network_error", "permission_denied"
        """
        self.simulate_failure = simulate_failure
        self.failure_type = failure_type or "invalid_response"

    def execute(self, **kwargs: Any) -> ToolResultSpec:
        start_time = time.time()
        
        # Check for induced failure flag
        if self.simulate_failure:
            time.sleep(0.1)
            duration = (time.time() - start_time) * 1000
            if self.failure_type == "timeout":
                return ToolResultSpec(
                    success=False,
                    tool_name=self.name,
                    output=None,
                    error=f"[INDUCED FAILURE] Tool '{self.name}' timed out after 10.0s waiting for upstream server.",
                    execution_time_ms=duration
                )
            elif self.failure_type == "network_error":
                return ToolResultSpec(
                    success=False,
                    tool_name=self.name,
                    output=None,
                    error=f"[INDUCED FAILURE] Tool '{self.name}' failed with HTTP 503 Service Unavailable.",
                    execution_time_ms=duration
                )
            else:
                return ToolResultSpec(
                    success=False,
                    tool_name=self.name,
                    output=None,
                    error=f"[INDUCED FAILURE] Tool '{self.name}' returned invalid/corrupted payload.",
                    execution_time_ms=duration
                )
        
        try:
            result_data = self._run(**kwargs)
            duration = (time.time() - start_time) * 1000
            return ToolResultSpec(
                success=True,
                tool_name=self.name,
                output=result_data,
                execution_time_ms=duration
            )
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return ToolResultSpec(
                success=False,
                tool_name=self.name,
                output=None,
                error=f"Error executing {self.name}: {str(e)}",
                execution_time_ms=duration
            )

    @abc.abstractmethod
    def _run(self, **kwargs: Any) -> Any:
        """Actual tool logic implemented by subclass."""
        pass
