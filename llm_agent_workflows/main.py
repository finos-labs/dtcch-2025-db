from dotenv import load_dotenv
from crew import Task, Crew
from agents.agent_sections_to_actions import AgentSectionsToActions


def main():
    # Load environment variables
    load_dotenv()

    agent_sections_to_actions = AgentSectionsToActions()

    # Create a crew with these agents
    crew = Crew(
        agents=[agent_sections_to_actions],
        max_iterations=1,  # Agents will iterate through tasks twice
        verbose=True
    )
    
    # Define tasks with dependencies
    tasks = [
        agent_sections_to_actions.task_section_to_actions()
    ]

    
    # Execute the workflow
    print("\nStarting Content Creation Workflow...\n")
    results = crew.execute_tasks(tasks)

    
    # Print final results
    print("\nWorkflow Complete! Final Results:")
    for task, result in results.items():
        print(f"\nTask: {task}")
        print(f"Result: {result}\n")
        print("-" * 80)

if __name__ == "__main__":
    main()
