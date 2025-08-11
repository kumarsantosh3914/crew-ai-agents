import os
import sys
import warnings

from datetime import datetime

from coder.crew import Coder
from coder.tools import NextJsScaffoldTool, ReactViteScaffoldTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

assignment = 'Write a python program to calculate the first 10,000 terms \
    of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + ...'

def run():
    """
    Run the crew.
    """
    # Default behavior runs the original coding task
    inputs = {'assignment': assignment}
    try:
        result = Coder().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def scaffold_next():
    """CLI helper to scaffold a Next.js project without LLM."""
    project_name = os.environ.get("PROJECT_NAME") or (sys.argv[1] if len(sys.argv) > 1 else "next-app")
    typescript = (os.environ.get("TYPESCRIPT", "true").lower() != "false")
    tailwind = (os.environ.get("TAILWIND", "true").lower() != "false")
    package_manager = os.environ.get("PM", "npm")
    target_root = os.environ.get("TARGET_ROOT", "output")
    app_router = (os.environ.get("APP_ROUTER", "true").lower() != "false")

    tool = NextJsScaffoldTool()
    created_path = tool.run(
        project_name=project_name,
        typescript=typescript,
        tailwind=tailwind,
        package_manager=package_manager,
        target_root=target_root,
        app_router=app_router,
    )
    print(created_path)


def scaffold_react():
    """CLI helper to scaffold a React + Vite project without LLM."""
    project_name = os.environ.get("PROJECT_NAME") or (sys.argv[1] if len(sys.argv) > 1 else "react-app")
    typescript = (os.environ.get("TYPESCRIPT", "true").lower() != "false")
    tailwind = (os.environ.get("TAILWIND", "true").lower() != "false")
    package_manager = os.environ.get("PM", "npm")
    target_root = os.environ.get("TARGET_ROOT", "output")

    tool = ReactViteScaffoldTool()
    created_path = tool.run(
        project_name=project_name,
        typescript=typescript,
        tailwind=tailwind,
        package_manager=package_manager,
        target_root=target_root,
    )
    print(created_path)
