# Debate Crew

A minimal multi‑agent debate system built with [crewAI](https://crewai.com). Two debate agents argue for and against a motion, and a judge agent decides the winner. Outputs are written to Markdown files under `debate/output/`.

## What you get
- A ready‑to‑run crew with agents and tasks defined in YAML
- Simple entrypoint to run a full debate over a motion
- Extensible tool interface for retrieval or custom logic

---

## Project structure
```
debate/
  README.md                # This file
  pyproject.toml           # Project metadata and crewAI integration
  src/debate/
    main.py                # Run entrypoint (used by crewAI CLI)
    crew.py                # Crew/agents/tasks wiring
    config/
      agents.yaml          # Agent definitions (roles, goals, models)
      tasks.yaml           # Task definitions (descriptions, outputs)
    tools/
      custom_tool.py       # Example of a custom crewAI tool
  output/                  # Debate outputs
    propose.md             # Pro side argument
    oppose.md              # Con side argument
    decide.md              # Judge decision
  knowledge/               # Optional local knowledge base
    user_preference.txt
```

---

## Prerequisites
- Python 3.10–3.13
- A supported LLM provider API key. This repo’s default agents use Groq models, so set `GROQ_API_KEY`. You can switch models/providers in `agents.yaml`.
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

3) Set environment variables for your model provider(s):
- If using Groq (default in this repo):
  - On Linux/macOS: `export GROQ_API_KEY=your_key`
  - On Windows PowerShell: `$Env:GROQ_API_KEY = "your_key"`
- If you switch to OpenAI models: set `OPENAI_API_KEY` instead.

You may also create a local `.env` file and export variables there, depending on your environment/tooling.

---

## Configuration
- `src/debate/config/agents.yaml`
  - Defines the `debater` and `judge` agents. Default models:
    - `debater`: `groq/llama-3.1-8b-instant`
    - `judge`: `groq/deepseek-r1-distill-llama-70b`
  - Tweak role, goal, backstory, or switch models/providers.

- `src/debate/config/tasks.yaml`
  - `propose` and `oppose` generate arguments and write to `output/propose.md` and `output/oppose.md`.
  - `decide` reads those arguments and writes a decision to `output/decide.md`.

- `src/debate/main.py`
  - Sets the motion text used by all tasks via `inputs = { 'motion': '...' }`.
  - Update the motion here to change the debate topic.

- `src/debate/tools/custom_tool.py`
  - Example tool showing how to add custom capabilities. Wire tools into agents in `crew.py`.

---

## Running a debate
From the repository root:
```bash
crewai run
```
This uses `pyproject.toml` metadata (`[tool.crewai] type = "crew"`) and runs the crew defined in `src/debate/`.

Outputs will be created under `debate/output/`:
- `propose.md` — argument in favor of the motion
- `oppose.md` — argument against the motion
- `decide.md` — judge’s decision and rationale

If the `output/` directory does not exist, create it before running.

Windows note: open PowerShell and run the same command from the project root. Ensure your API keys are set in the current shell (see Installation).

---

## Customizing
- Change the motion: edit `src/debate/main.py` and modify the `inputs['motion']` string.
- Adjust agents: edit `src/debate/config/agents.yaml` to change roles, goals, backstories, or models.
- Adjust tasks: edit `src/debate/config/tasks.yaml` to change task descriptions, expected outputs, or output paths.
- Add tools: implement new tools under `src/debate/tools/` and attach them to agents in `src/debate/crew.py`.

---

## Known limitations (in this template)
- A single `debater` agent is used for both sides; consider creating distinct `proposer`/`opposer` agents for diversity.
- Debate steps run sequentially; `propose` and `oppose` could run in parallel for faster execution.
- `pyproject.toml` exposes `train`, `replay`, `test` entry points, but they are not implemented in `src/debate/main.py`.

---

## Suggested roadmap
- Parallelize `propose` and `oppose`, then run `decide`.
- Use separate agents (and possibly models) for Pro and Con.
- Add rebuttal rounds and a structured rubric for the judge (optionally JSON output with scores).
- Integrate retrieval or web search tools and require citations.
- Add telemetry/logging and a batch runner for multiple motions.

---

## Troubleshooting
- Command not found: `crewai`
  - Install with `pip install crewai` (already included via `crewai[tools]` dependency) or ensure your environment is activated.
- Authentication errors
  - Verify `GROQ_API_KEY` (or your chosen provider’s key) is available in the runtime environment.
- Nothing written to `output/`
  - Ensure the directory exists and that the configured output paths in `tasks.yaml` are correct.

---

## Support
- crewAI docs: [docs.crewai.com](https://docs.crewai.com)
- crewAI GitHub: [github.com/joaomdmoura/crewai](https://github.com/joaomdmoura/crewai)
- Community Discord: [discord.com/invite/X4JWnZnxPb](https://discord.com/invite/X4JWnZnxPb)
