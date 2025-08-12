# Crew Agents Monorepo

Central hub for multiple crewAI-based agent projects:

- `coder/` — multi-agent coding assistant template
- `debate/` — two-sided debate with a judge
- `engineering_team/` — AI engineering team that designs, writes code, UI, and tests
- `financial_researcher/` — researcher + analyst producing a company report
- `stock_picker/` — hierarchical crew that finds, researches, and picks a stock

Each subproject is independently runnable and has its own `README.md` with details. This root README gives common setup and quickstart links.

---

## Prerequisites

- Python 3.10–3.13 (3.10+ required; <3.14)
- API key for your chosen models/providers
  - Groq (used by defaults in several crews): set `GROQ_API_KEY`
  - OpenAI (if you switch to `openai/...` models): set `OPENAI_API_KEY`
- Optional: [UV](https://docs.astral.sh/uv/) for fast, reproducible envs

---

## Install once (from repo root)

```bash
pip install uv          # optional but recommended
crewai install          # installs dependencies for active project when running
```

Notes:
- Some projects expect running commands inside their own folder; follow the per-project instructions below.
- If a provider/model is changed in `agents.yaml`, ensure the corresponding API key is exported.

---

## Environment variables (.env)

You can place a `.env` in a project folder (e.g., `financial_researcher/.env`) and/or in the repo root. Typical variables:

```
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key         # stock_picker tool (optional)
PUSHOVER_USER=your_pushover_user       # stock_picker notifications (optional)
PUSHOVER_TOKEN=your_pushover_token
```

On Windows PowerShell, you can also export in-shell:

```powershell
$Env:GROQ_API_KEY = "your_key"
```

---

## Projects overview and quickstart

### 1) `coder/`

- Template for a multi-agent coding workflow.
- Configure agents/tasks under `src/coder/config/`.
- Quickstart:
  - Set `OPENAI_API_KEY` (or your chosen provider key).
  - Run from the project folder: `crewai run`
- Outputs example: a `report.md` about LLMs (default sample flow).

More: see `coder/README.md`.

---

### 2) `debate/`

- Two debaters (pro/contra) and a judge. Writes Markdown outputs to `debate/output/`.
- Default models (editable in `src/debate/config/agents.yaml`):
  - debater: `groq/llama-3.1-8b-instant`
  - judge: `groq/deepseek-r1-distill-llama-70b`
- Quickstart (from repo root): `crewai run`
- Edit the motion in `src/debate/main.py`.

More: see `debate/README.md`.

---

### 3) `engineering_team/`

- Multi-agent “engineering team” that designs, generates code, a Gradio UI, and tests.
- Outputs to `engineering_team/output/` (design doc, module, app.py, tests).
- Quickstart (run inside the folder):
  - `crewai run`
  - or `uv run run_crew`
- Notes: code execution disabled by default; see `src/engineering_team/crew.py` for modes and models.

More: see `engineering_team/README.md`.

---

### 4) `financial_researcher/`

- Two-agent workflow: `researcher` → `analyst` → `output/report.md`.
- Default models in `src/financial_researcher/config/agents.yaml` (Groq). Set `GROQ_API_KEY`.
- Quickstart:
  - From the project folder: `crewai run`
  - Set the company in `src/financial_researcher/main.py` (`inputs['company']`).

More: see `financial_researcher/README.md`.

---

### 5) `stock_picker/`

- Hierarchical crew finds trending companies, researches them, and picks a winner.
- Optional tools: Serper (web search), Pushover (notifications), memory stores.
- Quickstart:
- From the project folder: `crewai run`
  - Provide `.env` with `GROQ_API_KEY` and optional tool keys.
- Defaults: sector = Technology; current year auto-detected.

More: see `stock_picker/README.md`.

---

## Common issues

- Model/auth errors: confirm the right `model:` per agent and matching API key in env.
- Nothing written to `output/`: ensure the output directory exists or that tasks point to correct paths.
- CLI missing: install `crewai` (included via project metadata) and activate the environment. With UV, prefer `uv run crewai run` inside a project folder if needed.

---

## Repository structure

```
crew-agents/
  README.md
  coder/
  debate/
  engineering_team/
  financial_researcher/
  stock_picker/
```

Each subfolder contains:

- `pyproject.toml` with `[tool.crewai]` metadata
- `src/<project_name>/` with `main.py`, `crew.py`, `config/`, and optional `tools/`
- `README.md` with detailed instructions

---

