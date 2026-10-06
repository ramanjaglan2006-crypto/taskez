from typing import Tuple, Dict, Any, Optional
from taskez.core.state import Step, StepStatus, TraceEvent, EventType
from taskez.tools.base import BaseTool

class SelfCorrectionManager:
    """
    Monitors tool execution errors (e.g. timeouts, rate limits, invalid input params, network failure)
    and applies self-correction policies:
      1. Parameter adjustment (e.g. simplifying search queries, sanitizing URLs)
      2. Tool substitution / Fallback (e.g. falling back from web scraper to search summary)
      3. Dynamic Re-planning & retries with exponential backoff notes.
    """
    
    def handle_step_failure(
        self,
        step: Step,
        error_msg: str,
        available_tools: Dict[str, BaseTool]
    ) -> Tuple[bool, Step, TraceEvent, Dict[str, Any]]:
        """
        Determines if step can be recovered via self-correction.
        Returns (recovered_flag, updated_step, correction_trace_event, updated_tool_args).
        """
        step.attempts += 1
        
        # Strategy 1: URL / Invalid Input parameter correction
        if "Invalid URL" in error_msg or "Must start with http" in error_msg:
            old_url = step.tool_args.get("url", "")
            fixed_url = "https://" + old_url if not old_url.startswith("http") else "https://duckduckgo.com"
            step.tool_args["url"] = fixed_url
            step.recovery_notes = f"Self-Correction: Corrected invalid URL format to '{fixed_url}'"
            
            trace = TraceEvent(
                event_type=EventType.SELF_CORRECTION,
                step_id=step.id,
                message=f"Detected parameter error on Step {step.id}. Sanitized URL payload to '{fixed_url}'.",
                details={"strategy": "parameter_sanitization", "original_error": error_msg}
            )
            step.status = StepStatus.RETRYING
            return True, step, trace, step.tool_args

        # Strategy 2: Tool Fallback substitution (e.g., WebScraper tool failure -> Fallback to WebSearch tool)
        if step.assigned_tool == "web_scraper" and ("HTTP Error" in error_msg or "timed out" in error_msg or "INDUCED FAILURE" in error_msg):
            query = step.tool_args.get("url", "travel information").replace("https://", "").replace("http://", "")
            step.assigned_tool = "web_search"
            step.tool_args = {"query": f"summary information for {query[:40]}"}
            step.recovery_notes = f"Self-Correction: Substituted failed web_scraper tool with web_search tool fallback."
            
            trace = TraceEvent(
                event_type=EventType.SELF_CORRECTION,
                step_id=step.id,
                message=f"Step {step.id} tool '{step.assigned_tool}' failed. Switched tool dynamically to 'web_search' fallback.",
                details={"strategy": "tool_substitution", "new_tool": "web_search", "error": error_msg}
            )
            step.status = StepStatus.RETRYING
            return True, step, trace, step.tool_args

        # Strategy 3: Query Simplification for WebSearch or GitHub tool timeouts
        if step.assigned_tool in ["web_search", "github_analyzer"] and step.attempts < step.max_attempts:
            if "query" in step.tool_args:
                original_q = step.tool_args["query"]
                simplified_q = " ".join(original_q.split()[:3])  # Truncate query keywords
                step.tool_args["query"] = simplified_q
                step.recovery_notes = f"Self-Correction: Simplified search query keywords to '{simplified_q}'"
            elif "repo_url" in step.tool_args:
                step.recovery_notes = f"Self-Correction: Retrying GitHub API query with default fallback repository params."
                
            trace = TraceEvent(
                event_type=EventType.SELF_CORRECTION,
                step_id=step.id,
                message=f"Attempt {step.attempts}/{step.max_attempts} failed for Step {step.id}. Applying query simplification retry strategy.",
                details={"strategy": "retry_with_simplified_args", "error": error_msg}
            )
            step.status = StepStatus.RETRYING
            return True, step, trace, step.tool_args

        # Max retries exceeded or unrecoverable error
        step.status = StepStatus.FAILED
        step.error = error_msg
        trace = TraceEvent(
            event_type=EventType.STEP_FAILURE,
            step_id=step.id,
            message=f"Step {step.id} failed after {step.attempts} attempts. Error: {error_msg}",
            details={"fatal": True, "error": error_msg}
        )
        return False, step, trace, step.tool_args
