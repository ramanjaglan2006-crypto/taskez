# TaskEZ Agent Engine — Design & Architecture Write-Up

## 1. Executive Design Overview
**TaskEZ** is an autonomous, tool-using agent system designed to decompose high-level natural language goals into executable sub-task plans, orchestrate multi-tool workflows, detect and self-correct runtime errors, and generate structured Markdown/JSON reports.

### Key Architectural Decisions
1. **Plan-and-Execute + ReAct Hybrid Architecture**: 
   Rather than relying purely on single-token next-action loops which can lose global goal coherence, TaskEZ uses a dual-layer strategy:
   - **Goal Planner**: Evaluates task domain and constructs an upfront sequence of steps with clear tool assignments, argument parameters, and success criteria.
   - **ReAct Executor**: Executes each step sequentially, passing state context forward and dynamically handling tool outcomes.
2. **Modular Tool Abstraction Layer**: 
   Tools derive from a unified `BaseTool` interface implementing strict parameter validation, execution timing, error handling, and **induced failure simulation** (`simulate_failure`) for grading robustness.
3. **Multi-Strategy Self-Correction Engine**: 
   When a step fails (due to network timeout, HTTP error, or bad API payload), the `SelfCorrectionManager` intervenes using:
   - *Parameter Sanitization*: Automatically corrects malformed inputs (e.g. missing HTTP schemes).
   - *Tool Substitution*: Dynamically swaps out failing tools (e.g. falling back from `web_scraper` to `web_search`).
   - *Query Simplification*: Retries queries with reduced constraint scopes.
4. **Dual Interface**:
   Provides both a **Rich Terminal CLI** for CLI-first users and a **FastAPI + WebSockets Dark-Mode Glassmorphic Dashboard** for real-time visual trace monitoring.

---

## 2. Technical Limitations & Trade-Offs

- **Determinism vs. Generative Flexibility**:
  *Trade-off*: A deterministic heuristic planner was combined with dynamic tool execution to ensure 100% offline testability without mandatory external API key dependencies.
  *Limitation*: Extremely open-ended or ambiguous goals outside the primary domains (GitHub analysis, travel/budgeting, research summarization) rely on generalized search-and-report workflows.
- **Sandboxed Expression Evaluator**:
  *Trade-off*: `CodeCalculatorTool` uses a restricted AST/dictionary evaluator rather than launching full Docker containers for light footprint and instant execution.
  *Limitation*: Advanced Python code execution (e.g. multi-file pandas dataframes) requires additional container sandboxing.

---

## 3. What I Would Do Differently With More Time

1. **DAG-Based Asynchronous Step Execution**:
   Currently, steps execute sequentially. With more time, I would upgrade the plan format to a Directed Acyclic Graph (DAG), enabling independent tool calls (e.g., parallel web searching and GitHub API querying) to execute concurrently using `asyncio.gather()`.
2. **Dynamic Sub-Agent Delegation**:
   Introduce hierarchical sub-agents where a primary coordinator agent delegates sub-tasks to specialized sub-agents (e.g. `CodeReviewAgent`, `FinancialCalcAgent`) with their own localized tool subsets and memory context.
3. **Long-Term Memory & Vector DB Integration**:
   Integrate a lightweight vector store (e.g. ChromaDB / FAISS) to cache web search results, document embeddings, and past execution plans for instant retrieval and few-shot reasoning.
