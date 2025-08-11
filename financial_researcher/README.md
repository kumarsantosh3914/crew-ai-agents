# FinancialResearcher Crew

A simple two‑agent financial research workflow built with [crewAI](https://crewai.com). A `researcher` gathers information for a company, and an `analyst` produces a polished report. The final report is saved to `financial_researcher/output/report.md`.

## What you get
- Ready‑to‑run crew with agents and tasks defined in YAML
- Clear hand‑off: research → analysis/report
- Extensible tool interface for web/knowledge retrieval

---

## Project structure
```
financial_researcher/
  README.md                # This file
  pyproject.toml           # Project metadata and crewAI integration
  src/financial_researcher/
    main.py                # Run entrypoint (used by crewAI CLI)
    crew.py                # Crew/agents/tasks wiring
    config/
      agents.yaml          # Agent definitions (roles, goals, models)
      tasks.yaml           # Task definitions (descriptions, outputs)
  knowledge/               # Optional local knowledge base
    user_preference.txt
  output/                  # Generated report (created at runtime)
    report.md
```

---

## Prerequisites
- Python 3.10–3.13
- A supported LLM provider API key. Defaults here use Groq models, so set `GROQ_API_KEY`. You can switch models/providers in `agents.yaml`.
- Recommended: [UV](https://docs.astral.sh/uv/) for fast, reproducible Python environments.

---

## Installation
1) Install UV (optional but recommended):
```bash
pip install uv
```

2) Install dependencies:
```bash
# From the repository root
crewai install
```

3) Provide credentials
- Option A: Place a `.env` file in any of these locations (auto‑loaded):
  - `financial_researcher/.env` (project root)
  - repo root `.env` (one directory above `financial_researcher`)
- Option B: Export variables in the shell
  - Linux/macOS: `export GROQ_API_KEY=your_key`
  - Windows PowerShell: `$Env:GROQ_API_KEY = "your_key"`
- If you switch to OpenAI models, set `OPENAI_API_KEY` instead.

---

## Configuration
- `src/financial_researcher/config/agents.yaml`
  - Agents:
    - `researcher`: `groq/deepseek-r1-distill-llama-70b`
    - `analyst`: `groq/llama-3.1-8b-instant`
  - Tweak role, goal, backstory, or switch models/providers.

- `src/financial_researcher/config/tasks.yaml`
  - `research_task` produces structured research for `{company}`.
  - `analysis_task` takes `research_task` as context and writes `output/report.md`.

- `src/financial_researcher/main.py`
  - Sets the company via `inputs = { 'company': 'Tesla' }`. Change this to research a different company.
  - Automatically loads `.env` from the project root or repo root.

---

## Running the crew
From the repository root:
```bash
cd financial_researcher
crewai run
```
This uses `pyproject.toml` metadata (`[tool.crewai] type = "crew"`) and runs the crew defined in `src/financial_researcher/`.

Output will be created under `financial_researcher/output/`:
- `report.md` — the final analyst report

If `output/` does not exist, the program will create it automatically.

Windows note: use PowerShell. If `.env` isn’t picked up, set `$Env:GROQ_API_KEY` in the same shell before running.

---

## Customizing
- Company: edit `src/financial_researcher/main.py` and set `inputs['company']`.
- Agents: edit `agents.yaml` to change roles, goals, backstories, or models.
- Tasks: edit `tasks.yaml` to adjust instructions or outputs.
- Tools: add custom tools and wire them to agents in `crew.py`.

---

## Troubleshooting
- Authentication errors
  - Ensure `.env` exists in the project or repo root or export the key in the shell.
  - Groq: `GROQ_API_KEY` must be set when using `groq/...` models.
- Report not created
  - Ensure the `analysis_task` in `tasks.yaml` points to `output/report.md`.
- Import or long startup delay
  - The first run may download/load packages; avoid interrupting. If needed, run again after dependencies are installed.

---

## Support
- crewAI docs: [docs.crewai.com](https://docs.crewai.com)
- crewAI GitHub: [github.com/joaomdmoura/crewai](https://github.com/joaomdmoura/crewai)
- Community Discord: [discord.com/invite/X4JWnZnxPb](https://discord.com/invite/X4JWnZnxPb)
