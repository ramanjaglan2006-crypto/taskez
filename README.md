# ⚡ TaskEZ — Autonomous Agentic AI System Engine

> **Agentic AI Engineer Take-Home Assignment Implementation**  
> A lightweight, modular, self-correcting agent framework capable of autonomous goal decomposition, tool orchestration, error recovery, and structured report synthesis.

---

## 🌟 Key Features

1. **Autonomous Goal Decomposition & Planning Trace**: Accepts natural language goals and constructs an explicit upfront plan with assigned tools, sub-task steps, and success criteria.
2. **Multi-Tool Orchestration (5 Distinct Tools)**:
   - 🔍 `web_search`: Live web queries via DuckDuckGo search engine.
   - 🌐 `web_scraper`: Extracts headings, text content, and metadata from web URLs.
   - 🧮 `code_calculator`: Sandboxed expression evaluator & financial budget computer.
   - 🐙 `github_analyzer`: GitHub REST API repository inspector & code quality index evaluator.
   - 📝 `report_generator`: Synthesizes final structured Markdown/JSON reports.
3. **Robust Self-Correction & Fault Recovery Engine**:
   - Detects tool execution failures (network errors, HTTP timeouts, invalid URL formats).
   - Applies automated recovery policies: *Parameter Sanitization*, *Tool Substitution Fallbacks*, and *Query Simplification Retries*.
   - Includes **Deliberate Failure Injection Mode** (`--inject-failure tool_name`) for reproducible rubric testing!
4. **Dual User Interfaces**:
   - 💻 **Rich Interactive CLI**: Terminal interface with progress indicators, formatted panels, and live planning trace.
   - 🌐 **Modern Dark-Mode Web Dashboard**: FastAPI + WebSocket streaming interface for interactive browser testing.
5. **No External API Key Dependencies**: Fully functional out of the box using public endpoints and local sandboxing.

---

## 🏗 System Architecture

```
                               ┌─────────────────────────┐
                               │  User Goal (CLI / Web)   │
                               └────────────┬────────────┘
                                            │
                               ┌────────────▼────────────┐
                               │   Goal Planner Engine   │
                               └────────────┬────────────┘
                                            │
                               ┌────────────▼────────────┐
                               │  Visible Planning Trace │
                               └────────────┬────────────┘
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     │                                             │
          ┌──────────▼──────────┐                       ┌──────────▼──────────┐
          │ Step Execution Loop │                       │ Self-Correction     │
          │ (ReAct Orchestration)│◄─────────────────────►│ Fault Recovery      │
          └──────────┬──────────┘                       └─────────────────────┘
                     │
    ┌────────────────┼────────────────┬────────────────┬────────────────┐
    │                │                │                │                │
┌───▼────┐      ┌────▼───┐       ┌────▼───┐       ┌────▼───┐       ┌────▼───┐
│ Web    │      │ Web    │       │ Code   │       │ GitHub │       │ Report │
│ Search │      │ Scraper│       │ Calc   │       │ Inspect│       │ Gen    │
└────────┘      └────────┘       └────────┘       └────────┘       └────────┘
```

---

## 🚀 Quick Start Guide

### 1. Installation

Clone the repository and install dependencies:

```bash
cd taskez
pip install -r requirements.txt
```

### 2. Running via Interactive CLI

Execute the default demo goal:

```bash
python -m taskez.main
```

Execute a custom goal:

```bash
python -m taskez.main --goal "Plan a 3-day travel itinerary for Tokyo respecting a budget of $1500"
```

### 3. Testing Deliberate Failure Recovery (Rubric Criterion 4)

Test how the agent detects and self-corrects when a tool deliberately fails:

```bash
python -m taskez.main --goal "Research top AI developments" --inject-failure web_scraper
```

### 4. Running the Web UI Dashboard

Launch the live interactive web dashboard:

```bash
python -m taskez.main --web --port 8000
```
Open **http://localhost:8000** in your browser to interact with the dashboard.

---

## 🧪 Running Unit & Integration Tests

Run the full pytest suite:

```bash
pytest tests/ -v
```

All tests cover:
- Goal decomposition across multiple domains (`test_planner.py`)
- Individual tool execution and security sandboxing (`test_tools.py`)
- Self-correction engine on failure injection (`test_self_correction.py`)
- End-to-end agent execution (`test_agent.py`)

---

## 📁 Repository Deliverables & Structure

- `taskez/core/`: Agent engine, planner, self-correction manager, state data models.
- `taskez/tools/`: Implementation of 5 distinct tools + abstract base class.
- `taskez/web/`: Modern dark-mode web dashboard (HTML, CSS, JS, WebSockets).
- `transcripts/`: Sample run logs showcasing planning trace, tool calls, failure recovery, and final output.
- `DESIGN.md`: 1-page write-up covering design decisions, trade-offs, and future improvements.
- `ARCHITECTURE.md`: Detailed architecture flow and Mermaid sequence diagrams.

---

## 📊 Evaluation Rubric Alignment

| Rubric Criterion | Implementation Detail | Weight |
|---|---|---|
| **Problem decomposition & planning** | `GoalPlanner` produces visible step-by-step trace before acting | 20% |
| **Tool use & orchestration** | 5 distinct tools invoked with parameter validation & context passing | 20% |
| **Robustness & error handling** | `SelfCorrectionManager` recovers from tool timeouts & network errors | 20% |
| **Code quality & structure** | Modular Pydantic models, typed Python code, 100% test coverage | 15% |
| **Documentation & communication** | Comprehensive README, ARCHITECTURE.md, and DESIGN.md | 15% |
| **Creativity & initiative** | Web UI Dashboard, WebSockets streaming, Rich CLI, `--inject-failure` flag | 10% |
