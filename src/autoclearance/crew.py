
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os

@CrewBase
class AutoclearanceCrew():
	"""Autoclearance crew"""

	agents_config = os.path.join(os.path.dirname(__file__), 'config', 'agents.yaml')
	tasks_config = os.path.join(os.path.dirname(__file__), 'config', 'tasks.yaml')

	@agent
	def ingest_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['ingest_agent'],
			verbose=True,
			llm='gpt-4o-mini',
		)

	@agent
	def auditor_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['auditor_agent'],
			verbose=True,
		)

	@task
	def ingest_task(self) -> Task:
		return Task(
			config=self.tasks_config['ingest_task'],
		)

	@task
	def audit_task(self) -> Task:
		return Task(
			config=self.tasks_config['audit_task'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=[
				self.ingest_agent(),
				self.auditor_agent()
			],
			tasks=[
				self.ingest_task(),
				self.audit_task()
			],
			process=Process.sequential,
			verbose=True,
		)