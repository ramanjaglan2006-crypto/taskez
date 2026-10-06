import pytest
from taskez.core.planner import GoalPlanner
from taskez.core.state import Plan

def test_planner_github_domain():
    planner = GoalPlanner()
    goal = "Given GitHub repo 'https://github.com/fastapi/fastapi', identify code quality issues"
    plan: Plan = planner.decompose_goal(goal)
    
    assert plan.domain == "github_code_analysis"
    assert len(plan.steps) == 4
    assert plan.steps[0].assigned_tool == "github_analyzer"
    assert plan.steps[3].assigned_tool == "report_generator"

def test_planner_travel_domain():
    planner = GoalPlanner()
    goal = "Plan a 3-day itinerary for Tokyo, respecting a given budget and interests."
    plan: Plan = planner.decompose_goal(goal)
    
    assert plan.domain == "travel_budget_planning"
    assert len(plan.steps) == 4
    assert plan.steps[2].assigned_tool == "code_calculator"

def test_planner_general_research_domain():
    planner = GoalPlanner()
    goal = "Research and summarize the top 3 developments in AI frameworks"
    plan: Plan = planner.decompose_goal(goal)
    
    assert plan.domain == "topic_research_summarization"
    assert len(plan.steps) == 4
