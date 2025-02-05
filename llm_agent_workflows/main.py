from dotenv import load_dotenv
from crew import Task, Crew
from agents.agent_kyc_review_policy import AgentKYCReviewPolicy
from pdfplumber import PDF


def main():
    # Load environment variables
    load_dotenv()

    agent_kyc_review_policy = AgentKYCReviewPolicy()

    # Create a crew with these agents
    crew = Crew(
        agents=[agent_kyc_review_policy],
        max_iterations=1,  # Agents will iterate through tasks twice
        verbose=False
    )

    # example of section, provided by agent form Matthew
    section = "Standard identification procedures will usually apply. In some cases, the firm holding the existing account may be willing to confirm the identity of the account holder to the new firm, and to provide evidence of the identification checks carried out. Care will need to be exercised by the receiving firm to be satisfied that the previous verification procedures provide an appropriate level of assurance for the new account, which may have different risk characteristics from the one held with the other firm."

    # Declaration of tasks
    task_section_to_action = agent_kyc_review_policy.task_section_to_actions(section)
    task_action_to_data_point = agent_kyc_review_policy.task_actions_to_data_points(previous_task=task_section_to_action)

    # Define tasks with dependencies
    tasks = [ task_section_to_action,
              task_action_to_data_point
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


def doc_processing(pdf: PDF):
    """Command-line interface for the PDFHandler."""

    # Initialize PDF Handler
    handler = PDFHandler()
    try:
        print(f"Processing PDF: {pdf}")
        print(f"Output will be saved to: {args.output}")
        if page_range:
            if isinstance(page_range, tuple):
                print(f"Processing pages {page_range[0]} to {page_range[1]}")
            else:
                print(f"Processing pages {', '.join(map(str, page_range))}")
        else:
            print("Processing all pages")

        handler.process_pdf(args.examples_pdf, args.output, page_range)

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    main()
