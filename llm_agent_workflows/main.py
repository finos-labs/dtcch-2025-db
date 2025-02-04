from dotenv import load_dotenv
from crew import Task, Crew
from agents.agent_sections_to_actions import AgentSectionsToActions
from agents.agent_actions_to_data_point import AgentActionsToDataPoints



def main():
    # Load environment variables
    load_dotenv()

    agent_sections_to_actions = AgentSectionsToActions()
    agent_action_to_data_points = AgentActionsToDataPoints()

    # Create a crew with these agents
    crew = Crew(
        agents=[agent_sections_to_actions, agent_action_to_data_points],
        max_iterations=1,  # Agents will iterate through tasks twice
        verbose=True
    )
    
    # Define tasks with dependencies
    tasks = [
        Task(
            description=f"""
        You are an expert in KYC (Know Your Customer) compliance and data mapping. 
        Your task is to analyze a given text and determine whether it contains a KYC action. 
        If it does, extract the corresponding data point required for compliance.
        
        Below are the steps you need to follow:
        1. Analyze the input text carefully. The input may or may not contain a KYC-related action. If the text does not contain a clear action, respond with "No Action Detected"
        2. Identify if the text describes an action related to KYC. KYC actions usually involve identifying, verifying, confirming, conducting screening, or assigning roles.
        3. Extract the corresponding KYC data point. The data point is the key piece of information that must be collected to complete the action. Common data points include: "First name", "Last name", "Role", "Residential Address", "Screening Result", "UBO Role", etc
        4. Format your response in the following structure:
        {{
        "action_detected": true,
        "action": "<Extracted KYC Action>",
        "data_point": "<Corresponding Data Point>"
        }}
        If no action is found, return:
        {{
        "action_detected": false
        }}
        
        Please do it for below piece of texts individually:
        1. Identify the Natural Person Client Senior Manager's residential address
        2. Add Ultimate Beneficial Owner role to Client Senior Manager with Significant control
        3. Verify the last name of any Natural Person Client Senior Managers (CSMs)
        4. JVMA is a company that has a big client base
        """,
            agent_role="kyc_analyst",
            expected_output="To know the data points from actions for KYC",
            context=f"""
            Below are some examples where first we have the action and then the data point after the comma for your understanding:
            Create Natural Person Client Senior Manager profile for identified Client Senior Managers, Natural Person Client Senior Manager Role
            Identify the first name of any Natural Person Client Senior Managers (CSMs), First name
            Identify the middle name of any Natural Person Client Senior Managers (CSMs), Middle name
            Verify the middle name of any Natural Person Client Senior Managers (CSMs), Middle name
            Identify the last name of any Natural Person Client Senior Managers (CSMs), Last name
            Verify the last name of any Natural Person Client Senior Managers (CSMs), Last name
            Identify the Natural Person Client Senior Manager's role at the client?, Role
            Conduct screening on the Natural Person Client Senior Manager, Screening Result
            Has a Client Senior Manager been identified as a Relative or Close Associate of a Politically Exposed Person?, RCA Flag
            Confirm if a Client Senior Manager have significant control of the client, Significant control
            Confirm if KYC Ops agree with ACO assessment of Client Senior Manager's Significant control, Significant control KYC Ops agreement
            Add Ultimate Beneficial Owner role to Client Senior Manager with Significant control, UBO role
            """,
            dependencies=[]
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
