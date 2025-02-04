from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Task:
    description: str
    agent_role: str  # The role responsible for this task
    expected_output: str
    context: str = ""
    dependencies: List[str] = None  # List of task IDs that must be completed first
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
