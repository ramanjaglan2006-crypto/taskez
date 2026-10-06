import sys
import os
import argparse
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

from taskez.core.agent import TaskEZAgent
from taskez.core.state import EventType, TraceEvent

console = Console()

def render_trace_event(event: TraceEvent):
    """Renders live event stream to Rich Console."""
    if event.event_type == EventType.PLANNING_START:
        console.print(Panel(f"[bold cyan]🎯 Goal Received:[/bold cyan] {event.message}", title="TaskEZ Agent Initialized", border_style="cyan"))

    elif event.event_type == EventType.PLAN_CREATED:
        console.print("\n[bold green]🧠 Autonomous Planning Trace (Decomposed Steps):[/bold green]")
        steps = event.details.get("steps", []) if event.details else []
        table = Table(title=f"Plan Domain: [yellow]{event.details.get('domain', 'general')}[/yellow]", show_header=True, header_style="bold magenta")
        table.add_column("Step #", style="dim", width=8)
        table.add_column("Sub-Goal / Title", style="bold white", width=35)
        table.add_column("Assigned Tool", style="green", width=20)
        table.add_column("Status", style="yellow", width=12)

        for s in steps:
            table.add_row(str(s.get("id")), s.get("title"), s.get("assigned_tool"), s.get("status"))
        console.print(table)
        console.print(f"[dim]Thought Process: {event.details.get('thought_process')}[/dim]\n")

    elif event.event_type == EventType.STEP_START:
        console.print(f"[bold blue]▶ [Step {event.step_id}][/bold blue] {event.message}")

    elif event.event_type == EventType.TOOL_CALL:
        details = event.details or {}
        tool_name = details.get("tool_name", "tool")
        args_str = json.dumps(details.get("arguments", {}), indent=2)
        console.print(f"  [dim yellow]🛠 Invoking Tool [{tool_name}]:[/dim yellow]")
        console.print(Syntax(args_str, "json", theme="monokai", line_numbers=False))

    elif event.event_type == EventType.STEP_SUCCESS:
        console.print(f"  [bold green]✔ {event.message}[/bold green]\n")

    elif event.event_type == EventType.SELF_CORRECTION:
        console.print(Panel(
            f"[bold yellow]⚠️ Self-Correction Triggered on Step {event.step_id}:[/bold yellow]\n{event.message}",
            title="⚡ Fault Recovery Engine",
            border_style="yellow"
        ))

    elif event.event_type == EventType.STEP_FAILURE:
        console.print(f"  [bold red]✖ {event.message}[/bold red]\n")

def main():
    parser = argparse.ArgumentParser(description="TaskEZ - Autonomous Agentic AI System")
    parser.add_argument("--goal", type=str, help="High-level natural language goal for the agent")
    parser.add_argument("--inject-failure", type=str, choices=["web_search", "web_scraper", "code_calculator", "github_analyzer"],
                        help="Deliberately trigger a failure on a specific tool to test self-correction")
    parser.add_argument("--web", action="store_true", help="Launch FastAPI Web UI Dashboard")
    parser.add_argument("--port", type=int, default=8000, help="Port for Web UI Dashboard")
    parser.add_argument("--export-json", type=str, help="Path to save execution transcript JSON")
    
    args = parser.parse_args()

    # Launch Web Server if requested
    if args.web:
        console.print(f"[bold green]🚀 Launching TaskEZ Web UI Dashboard on http://localhost:{args.port}...[/bold green]")
        import uvicorn
        from taskez.server import app
        uvicorn.run(app, host="0.0.0.0", port=args.port)
        return

    # Interactive prompt if no goal provided
    goal = args.goal
    if not goal:
        console.print(Panel.fit("[bold cyan]TaskEZ - Autonomous Agent Engine[/bold cyan]\nEnter a high-level goal or press Enter for default demo goal.", border_style="cyan"))
        goal = console.input("[bold yellow]Enter your goal: [/bold yellow]").strip()
        if not goal:
            goal = "Given GitHub repo 'https://github.com/fastapi/fastapi', identify code quality issues and calculate health index."

    failure_tool = args.inject_failure
    console.print(f"\n[bold magenta]⚡ Starting TaskEZ Execution Engine...[/bold magenta]")
    if failure_tool:
        console.print(f"[bold red]🧪 Failure Injection Active: Deliberately breaking tool '[/bold red]{failure_tool}[bold red]' to test self-correction.[/bold red]\n")

    agent = TaskEZAgent(failure_injection_tool=failure_tool)
    agent.register_event_listener(render_trace_event)

    report = agent.run(goal)

    # Render Final Output Report
    console.print(Panel("[bold green]✨ FINAL STRUCTURED AGENT REPORT[/bold green]", border_style="green"))
    console.print(Markdown(str(report.final_output)))
    
    console.print(f"\n[bold cyan]📊 Summary Metrics:[/bold cyan]")
    console.print(f" • Domain: [yellow]{report.domain}[/yellow]")
    console.print(f" • Total Steps Executed: [bold]{report.steps_executed}[/bold]")
    console.print(f" • Successful Steps: [green]{report.successful_steps}[/green]")
    console.print(f" • Self-Corrections Triggered: [yellow]{report.self_corrections_made}[/yellow]")
    console.print(f" • Total Execution Duration: [magenta]{report.total_duration_seconds}s[/magenta]\n")

    if args.export_json:
        with open(args.export_json, "w") as f:
            f.write(report.json(indent=2))
        console.print(f"[bold green]💾 Saved transcript to '{args.export_json}'[/bold green]")

if __name__ == "__main__":
    main()
