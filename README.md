# AWS Bedrock Multi-Agent Framework

A lightweight framework for building multi-agent systems using AWS Bedrock's Claude model. This framework allows you to create collaborative AI agents that can work together on complex tasks, with built-in support for task dependencies and iterative refinement.

## What It Does

- **Multi-Agent Collaboration**: Create multiple AI agents with different roles and expertise
- **Task Dependencies**: Define tasks with dependencies to create complex workflows
- **Iterative Refinement**: Agents can iterate multiple times to improve their outputs
- **Context Sharing**: Agents can build upon each other's work through task dependencies
- **AWS Bedrock Integration**: Uses Claude 3.5 Sonnet for high-quality responses

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up AWS credentials in `.env`:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token  # if using temporary credentials
```

3. Run the example:
```bash
./run.sh
```

## Creating Your Own Multi-Agent System

1. **Define Your Agents**
```python
from crew import Agent

researcher = Agent(
    role="Research Analyst",
    goal="Gather and analyze information",
    backstory="Expert in data analysis",
    tools=["web_search", "data_analysis"],
    verbose=True
)
```

2. **Create Tasks**
```python
from crew import Task

research_task = Task(
    description="Research market trends",
    agent_role="Research Analyst",
    expected_output="Market analysis report",
    dependencies=[]  # No dependencies for first task
)

write_task = Task(
    description="Write market report",
    agent_role="Content Writer",
    expected_output="Final report",
    dependencies=["Research market trends"]  # Depends on research task
)
```

3. **Set Up Your Crew**
```python
from crew import Crew

crew = Crew(
    agents=[researcher, writer],
    max_iterations=2,  # Agents will iterate twice
    verbose=True
)

# Execute tasks
results = crew.execute_tasks([research_task, write_task])
```

## Configuration Options

### Agent Configuration
- `role`: The agent's specialized role
- `goal`: What the agent aims to achieve
- `backstory`: Context about the agent's expertise
- `tools`: List of tools the agent can use
- `verbose`: Whether to show detailed output

### Task Configuration
- `description`: What needs to be done
- `agent_role`: Which agent should handle this task
- `expected_output`: What the task should produce
- `dependencies`: List of tasks that must complete first
- `context`: Additional context (auto-populated from dependencies)

### Crew Configuration
- `agents`: List of agents in the crew
- `max_iterations`: How many times to iterate (default: 2)
- `verbose`: Whether to show detailed output

## Example Use Cases

1. **Content Creation Pipeline**
   - Research Analyst gathers information
   - Content Writer creates content
   - Editor reviews and refines

2. **Market Analysis**
   - Data Analyst collects market data
   - Market Analyst interprets trends
   - Report Writer creates final report

3. **Code Review Process**
   - Code Reviewer analyzes code
   - Security Expert checks for vulnerabilities
   - Documentation Writer updates docs

## Project Structure

```
hackathon/
├── .env                  # AWS credentials
├── README.md            # Project documentation
├── crew/                # Core implementation
│   ├── __init__.py     # Package initialization
│   ├── agent.py        # Agent class
│   ├── crew.py         # Crew orchestration
│   └── task.py         # Task class
├── main.py             # Main application file
├── requirements.txt    # Dependencies
└── run.sh             # Run script
```

## Requirements

- Python 3.8+
- AWS account with Bedrock access
- Required packages (see requirements.txt)

## Error Handling

The framework includes built-in error handling for:
- Expired AWS credentials
- Missing environment variables
- Task dependency issues
- Agent execution errors

## Best Practices

1. **Agent Design**
   - Give agents clear, focused roles
   - Provide detailed backstories
   - Set specific goals

2. **Task Management**
   - Break complex tasks into smaller steps
   - Define clear dependencies
   - Set appropriate iteration counts

3. **Error Handling**
   - Keep AWS credentials up to date
   - Monitor agent outputs
   - Use verbose mode for debugging

## Contributing

Feel free to submit issues and pull requests to improve the framework.
