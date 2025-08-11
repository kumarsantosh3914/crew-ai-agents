# StockPicker Crew

A hierarchical multi‑agent workflow built with [crewAI](https://crewai.com). It finds trending companies in a sector, researches them, and picks the best one. Includes optional web search (Serper), push notifications (Pushover), and memory (short/long/entity).

## What you get
- Hierarchical crew with a manager delegating tasks
- Structured outputs using Pydantic models
- Optional push notifications and memory storage

---

## Project structure
```
stock_picker/
  README.md
  pyproject.toml
  src/stock_picker/
    main.py                 # Entrypoint (auto-loads .env)
    crew.py                 # Agents, tasks, tools, memory wiring
    config/
      agents.yaml           # Agent roles, goals, and model choices
      tasks.yaml            # Task descriptions and outputs
    tools/
      push_tool.py          # Pushover tool (PushNotificationTool)
  memory/                   # SQLite + RAG storages (created at runtime)
  knowledge/                # Optional knowledge sources
  output/                   # Generated outputs (created at runtime)
```

---

## Prerequisites
- Python 3.10–3.13
- Models/providers:
  - Groq: set `GROQ_API_KEY`
  - OpenAI (if any `openai/...` models or embeddings): set `OPENAI_API_KEY`
  - Serper tool: set `SERPER_API_KEY`
  - Pushover tool: set `PUSHOVER_USER`, `PUSHOVER_TOKEN`
- Optional: [UV](https://docs.astral.sh/uv/) for fast, reproducible envs

---

## Installation
```bash
# From the repository root
pip install uv  # optional
crewai install
```

---

## Environment variables (.env)
This project auto‑loads `.env` from:
- `stock_picker/.env` (project root), and/or
- repo root `.env`

Example `.env`:
```
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
PUSHOVER_USER=your_pushover_user
PUSHOVER_TOKEN=your_pushover_token
```

---

## Configuration
- `src/stock_picker/config/agents.yaml`
  - All agents can use the same provider for simplicity. Examples:
    - Groq: `model: groq/llama-3.1-8b-instant`
    - OpenAI: `model: openai/gpt-4o` (requires `OPENAI_API_KEY`)
  - Ensure every agent has a valid `model` and the corresponding API key is available.

- `src/stock_picker/config/tasks.yaml`
  - `find_trending_companies`: returns a structured list (`TrendingCompanyList`)
  - `research_trending_companies`: returns detailed research (`TrendingCompanyResearchList`)
  - `pick_best_company`: final selection and reasoning

- `src/stock_picker/crew.py`
  - Tools: `SerperDevTool()` for web search; `PushNotificationTool()` for Pushover
  - Memory (optional): long/short/entity memory storages. If you don’t set `OPENAI_API_KEY`, either set a supported embedder or comment out these memory blocks while testing.

---

## Running
```bash
cd stock_picker
crewai run
```
Inputs used (by default): sector = Technology, current_year = current year.

---

## Troubleshooting
- “Model not found” or fallback to wrong provider
  - Ensure `model:` in `agents.yaml` matches a provider you have a key for.
  - Remove env overrides that force defaults (e.g., unset `LITELLM_MODEL`).
- 401/403/429 or provider 500
  - Keys missing/invalid, rate limits, or transient provider errors. Use lighter models (e.g., `llama-3.1-8b-instant`) and retry.
- Serper/Pushover tools not working
  - Make sure `SERPER_API_KEY`, `PUSHOVER_USER`, `PUSHOVER_TOKEN` are in `.env`.
- Memory errors
  - Comment out memory blocks in `crew.py` until embedder keys are set.

---

## Notes
- This template is designed for extensibility. Add tools, tweak prompts, or change the process as needed.
- For production, prefer consistent providers across agents and enable a single set of credentials.
