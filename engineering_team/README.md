# EngineeringTeam Crew

Welcome to the EngineeringTeam Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Set your LLM API key (e.g., `GROQ_API_KEY`) in a `.env` or the shell**

- Modify `src/engineering_team/config/agents.yaml` to define your agents
- Modify `src/engineering_team/config/tasks.yaml` to define your tasks
- Modify `src/engineering_team/crew.py` to add your own logic, tools and specific args
- Modify `src/engineering_team/main.py` to add custom inputs for your agents and tasks

## Running the Project

From the `engineering_team/` folder:

```bash
crewai run
# or
uv run run_crew
```

This initializes the EngineeringTeam crew and runs the tasks defined in your configuration.

Outputs are written under `engineering_team/output/`:
- `{module_name}_design.md`
- `{module_name}` (Python module)
- `app.py` (Gradio UI)
- `test_{module_name}`

## Understanding Your Crew

The engineering_team Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Notes

- Code execution is disabled by default; no Docker required. If you enable sandboxed code execution, use `code_execution_mode="safe"` and install Docker. For direct host execution, use `unsafe` in trusted environments only.
- Default Groq models are set in `src/engineering_team/config/agents.yaml`. Update them if a model is decommissioned.

## Support

For support, questions, or feedback regarding the EngineeringTeam Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
