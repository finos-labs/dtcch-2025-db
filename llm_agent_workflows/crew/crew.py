from typing import List, Dict
from .agent import Agent
from .task import Task

class Crew:
    def __init__(self, agents: List[Agent], max_iterations: int = 2, verbose: bool = False):
        self.agents = {agent.role: agent for agent in agents}
        self.verbose = verbose
        self.task_results = {}
        self.max_iterations = max_iterations
        
    def execute_tasks(self, tasks: List[Task]) -> Dict[str, str]:
        """Execute a list of tasks in the correct order based on dependencies"""
        iteration = 0
        while iteration < self.max_iterations:
            if self.verbose:
                print(f"\nIteration {iteration + 1}/{self.max_iterations}")
            
            for task in tasks:
                # Check if dependencies are met
                if task.dependencies:
                    context = "\n".join([
                        f"{self.task_results.get(dep.context, 'Not completed')}"
                        for dep in task.dependencies
                    ])
                    task.context = context
                
                # Get the responsible agent
                agent = self.agents.get(task.agent_role)
                if not agent:
                    raise ValueError(f"No agent found for role: {task.agent_role}")
                
                # Execute the task
                if self.verbose:
                    print(f"\nExecuting Task: {task.description}")
                    print(f"Agent: {agent.role}")
                    if task.context:
                        print(f"Context from dependencies:\n{task.context}\n")
                
                result = agent.execute_task(task.description, task.context)
                # validation of json
                try:
                    self._validation(task.validation_type)
                except Exception as e:
                    print(f"Validation error: {e}")

                self.task_results[task.description] = result
                
                if result is None:  # If there was an error, stop execution
                    return self.task_results
            
            iteration += 1

        return self.task_results

    def _validation(self, validation_type: str):
        #TODO: add validation depending on string need to validate the type too
        pass