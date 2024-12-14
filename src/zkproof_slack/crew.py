from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from zkproof_slack.tools.custom_tool import SlackPostTool

@CrewBase
class ZkproofSlack():
	"""ZkproofSlack crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def slack_post_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['slack_post_agent'],
			tools=[SlackPostTool()],
			verbose=True
		)

	@task
	def posting_task(self) -> Task:
		return Task(
			config=self.tasks_config['posting_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ZkproofSlack crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
