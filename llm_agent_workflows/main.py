from dotenv import load_dotenv
from crew import Agent, Task, Crew

def main():
    # Load environment variables
    load_dotenv()
    
    # Create agents with specific roles and goals
    researcher = Agent(
        role="Research Analyst",
        goal="Gather and analyze information to provide data-driven insights",
        backstory="Expert in data analysis with a focus on market research and trend identification",
        tools=["web_search", "data_analysis"],
        verbose=True
    )
    
    writer = Agent(
        role="Content Strategist",
        goal="Create compelling content based on research insights",
        backstory="Experienced content creator with expertise in digital marketing",
        tools=["content_editor", "seo_analyzer"],
        verbose=True
    )
    
    reviewer = Agent(
        role="Quality Assurance",
        goal="Ensure accuracy and quality of final deliverables",
        backstory="Detail-oriented professional with experience in content review and optimization",
        tools=["grammar_checker", "fact_checker"],
        verbose=True
    )
    
    # Create a crew with these agents
    crew = Crew(
        agents=[researcher, writer, reviewer],
        max_iterations=2,  # Agents will iterate through tasks twice
        verbose=True
    )
    
    # Define tasks with dependencies
    tasks = [
        Task(
            description="Research current AI trends in healthcare",
            agent_role="Research Analyst",
            expected_output="Comprehensive analysis of AI healthcare trends",
            dependencies=[]
        ),
        Task(
            description="Create a blog post about AI in healthcare",
            agent_role="Content Strategist",
            expected_output="Engaging blog post",
            dependencies=["Research current AI trends in healthcare"]
        ),
        Task(
            description="Review and optimize the blog post",
            agent_role="Quality Assurance",
            expected_output="Polished final content",
            dependencies=["Create a blog post about AI in healthcare"]
        )
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
