import pytest
from taskez.core.agent import TaskEZAgent

def test_agent_self_correction_on_failure_injection():
    # Deliberately inject a web_scraper tool failure to test self-correction recovery
    agent = TaskEZAgent(failure_injection_tool="web_scraper")
    report = agent.run(goal="Research top 3 developments in quantum computing")
    
    assert report.self_corrections_made >= 1
    assert report.successful_steps == report.steps_executed
    assert report.failed_steps == 0

def test_agent_end_to_end():
    agent = TaskEZAgent()
    report = agent.run(goal="Given GitHub repo 'https://github.com/fastapi/fastapi', identify potential code quality issues")
    
    assert report.domain == "github_code_analysis"
    assert report.steps_executed == 4
    assert report.successful_steps == 4
    assert "Code Quality Assessment" in str(report.final_output)
