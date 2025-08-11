from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from coder.tools import NextJsScaffoldTool, ReactViteScaffoldTool

@CrewBase
class Coder():
    """Coder crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=30, 
            max_retry_limit=3 
        )

    @agent
    def web_scaffolder(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scaffolder'],
            verbose=True,
            tools=[
                NextJsScaffoldTool(),
                ReactViteScaffoldTool(),
            ],
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
        )

    @task
    def scaffold_task(self) -> Task:
        return Task(
            config=self.tasks_config['scaffold_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Coder crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
