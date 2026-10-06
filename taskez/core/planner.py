from typing import List, Dict, Any
from taskez.core.state import Plan, Step, StepStatus

class GoalPlanner:
    """
    Decomposes natural language user goals into structured, actionable plans
    with step dependencies, tool assignments, and tool argument parameters.
    """
    
    def decompose_goal(self, goal: str) -> Plan:
        goal_lower = goal.lower()
        
        # Domain 1: GitHub Repository Analysis
        if "github.com" in goal_lower or "repo" in goal_lower or "repository" in goal_lower or "code quality" in goal_lower:
            domain = "github_code_analysis"
            thought = "Analyzed user goal. Detected request for GitHub repository inspection and code quality review. Formulating 4-step execution plan: (1) Extract repository metrics and code quality via GitHub API, (2) Analyze README and file structure, (3) Evaluate test coverage and license compliance using code calculator, (4) Synthesize final code quality report."
            
            # Extract repository URL if present
            repo_url = "https://github.com/fastapi/fastapi"
            words = goal.split()
            for w in words:
                if "github.com" in w:
                    repo_url = w.strip("',\"()")
                    break
                    
            steps = [
                Step(
                    id=1,
                    title="Fetch GitHub Repository Metadata & Metrics",
                    description=f"Query public GitHub REST API for repository parameters of {repo_url}",
                    assigned_tool="github_analyzer",
                    tool_args={"repo_url": repo_url}
                ),
                Step(
                    id=2,
                    title="Search for Related Technical Benchmarks",
                    description="Perform web search to check community sentiment and alternative projects",
                    assigned_tool="web_search",
                    tool_args={"query": f"GitHub repository quality reviews for {repo_url.split('/')[-1]}"}
                ),
                Step(
                    id=3,
                    title="Calculate Quality Index Score",
                    description="Execute mathematical evaluation to compute overall repository health score",
                    assigned_tool="code_calculator",
                    tool_args={"expression": "100 - (15 if license == 'None' else 0) - (25 if not has_readme else 0) - min(30, open_issues * 0.5)"}
                ),
                Step(
                    id=4,
                    title="Synthesize Code Review Report",
                    description="Compile findings into structured Markdown/JSON summary report",
                    assigned_tool="report_generator",
                    tool_args={"title": f"Code Quality Assessment: {repo_url}", "goal": goal}
                )
            ]

        # Domain 2: Travel Planning & Budget Calculator
        elif "travel" in goal_lower or "itinerary" in goal_lower or "budget" in goal_lower or "city" in goal_lower or "trip" in goal_lower:
            domain = "travel_budget_planning"
            thought = "Detected travel itinerary and budget request. Formulating 4-step execution plan: (1) Research top attractions, dining, and accommodations for target city, (2) Scrape cost & tip details, (3) Calculate day-by-day itemized budget allocations using sandboxed math calculator, (4) Produce final structured itinerary report."
            
            city = "Tokyo"
            for c in ["tokyo", "paris", "london", "new york", "san francisco", "berlin", "rome", "kyoto", "barcelona"]:
                if c in goal_lower:
                    city = c.capitalize()
                    break

            steps = [
                Step(
                    id=1,
                    title=f"Research Attractions & Spots in {city}",
                    description=f"Search live web for top 3-day itinerary spots, attractions, and cultural highlights in {city}",
                    assigned_tool="web_search",
                    tool_args={"query": f"top 3-day itinerary attractions dining budget in {city}"}
                ),
                Step(
                    id=2,
                    title="Scrape Detailed Travel Guidelines & Costs",
                    description=f"Extract cost breakdown and transit options for {city}",
                    assigned_tool="web_scraper",
                    tool_args={"url": f"https://html.duckduckgo.com/html/?q={city}+travel+costs"}
                ),
                Step(
                    id=3,
                    title="Compute Itemized Budget & Expenses",
                    description="Run math calculator to allocate lodging, meals, transport, and buffer across 3 days",
                    assigned_tool="code_calculator",
                    tool_args={"expression": "daily_hotel * 3 + daily_food * 3 + total_transit + activity_budget"}
                ),
                Step(
                    id=4,
                    title=f"Generate 3-Day Travel Itinerary Report for {city}",
                    description="Synthesize itinerary, budget breakdown, and local tips into structured report",
                    assigned_tool="report_generator",
                    tool_args={"title": f"3-Day Curated Travel & Budget Plan: {city}", "goal": goal}
                )
            ]

        # Domain 3: Topic Research & Market Summarization
        else:
            domain = "topic_research_summarization"
            thought = f"Detected general research & summarization goal. Formulating 4-step execution plan: (1) Perform multi-query live web search on target topic, (2) Scrape primary source details, (3) Evaluate trend statistics using calculator tool, (4) Generate executive summary report."
            
            steps = [
                Step(
                    id=1,
                    title="Perform Multi-Source Web Search",
                    description=f"Search live web for top developments and recent updates on: '{goal}'",
                    assigned_tool="web_search",
                    tool_args={"query": goal}
                ),
                Step(
                    id=2,
                    title="Extract Deep Source Insights",
                    description="Extract detailed web page content from primary search result",
                    assigned_tool="web_scraper",
                    tool_args={"url": f"https://html.duckduckgo.com/html/?q={goal.replace(' ', '+')}"}
                ),
                Step(
                    id=3,
                    title="Analyze Trends & Compute Metrics",
                    description="Run code calculator to evaluate quantitative highlights and counts",
                    assigned_tool="code_calculator",
                    tool_args={"expression": "sum([10, 25, 40, 15]) / 4.0"}
                ),
                Step(
                    id=4,
                    title="Generate Structured Research Brief",
                    description="Synthesize research findings, statistics, and citations into structured report",
                    assigned_tool="report_generator",
                    tool_args={"title": f"Research Brief: {goal}", "goal": goal}
                )
            ]

        return Plan(
            goal=goal,
            domain=domain,
            thought_process=thought,
            steps=steps
        )
