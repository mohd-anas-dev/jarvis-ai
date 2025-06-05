"""
TaskExecutor.py - Task interpretation system for JARVIS AI

This module handles the interpretation of task codes like "48A", "17B", etc.
and executes the corresponding actions.
"""

from webbrowser import open as webopen
from AppOpener import open as appopen
import re

# Task definitions - Each task is a dictionary with a list of actions
TASKS = {
    "48A": [
        {"type": "web", "target": "https://www.youtube.com"},
        {"type": "app", "target": "edge"}
    ],
    "48B": [
        {"type": "web", "target": "https://www.youtube.com"},
        {"type": "web", "target": "https://learning.manipaldubai.com/d2l/home/6735"},
        {"type": "web", "target": "https://chat.openai.com"}
    ],
    "17A": [
        {"type": "web", "target": "https://www.instagram.com"},
        {"type": "web", "target": "https://www.youtube.com"},
        {"type": "app", "target": "whatsapp"},
        {"type": "web", "target": "https://music.youtube.com"}
    ],
    "17B": [
        {"type": "app", "target": "word"},
        {"type": "app", "target": "powerpoint"},
        {"type": "app", "target": "excel"}
    ]
}

def interpret_task_command(command):
    """
    Extracts task code from commands like:
    - "Execute task 48A"
    - "Engage 17A"
    - "Initiate protocol 48B"
    - "Run 17B"
    - "Activate task 48 to be"
    - "Jarvis execute 48 to be"
    - "Execute48b"
    - "48b"
    - "48 b"
    - "execute 48 b"
    - ANY possible variation
    
    Returns the task code if found, None otherwise.
    """
    # Convert to lowercase and strip spaces for consistent processing
    command = command.lower().strip()
    
    # Exclude obviously non-task sentences
    if not any(num in command for num in ["48", "17"]) and not any(action in command for action in ["execute", "engage", "initiate", "run", "activate"]):
        return None
        
    # Exclude natural language sentences unrelated to tasks
    if any(phrase in command for phrase in ["want to be", "going to be", "hope to be", "wish to be"]):
        if not any(action in command for action in ["execute", "engage", "initiate", "run", "activate"]):
            return None
    
    # EXTRACT NUMBERS FIRST - Find all numbers in the command
    numbers = re.findall(r'\d+', command)
    if not numbers:
        return None
    
    # We'll focus on the first number found (usually the task number)
    task_number = numbers[0]
    
    # DETERMINE LETTER - Look for clear letter indicators first
    if "to be" in command or "tobe" in command:
        return f"{task_number}B"
        
    # Look for B indicators
    if any(b_ind in command for b_ind in [" b", "b ", ".b", "b.", ",b", "b,", "-b", "b-", "bee", " to b"]):
        return f"{task_number}B"
        
    # Look for A indicators
    if any(a_ind in command for a_ind in [" a", "a ", ".a", "a.", ",a", "a,", "-a", "a-", "aye", "ay"]):
        return f"{task_number}A"
    
    # Check for standalone format (just the number followed by letter)
    letter_after_num = re.search(rf'{task_number}\s*([ab])', command)
    if letter_after_num:
        return f"{task_number}{letter_after_num.group(1).upper()}"
    
    # Check for any action verb followed by task designation
    action_with_letter = re.search(r'(?:execute|engage|initiate|run|activate).*?(\d+).*?([ab])', command)
    if action_with_letter:
        return f"{action_with_letter.group(1)}{action_with_letter.group(2).upper()}"
    
    # Final fallback - look at the context after the number for A or B hints
    post_number_context = command.split(task_number, 1)[-1].lower()
    
    if 'b' in post_number_context:
        return f"{task_number}B"
    elif 'a' in post_number_context:
        return f"{task_number}A"
    
    # Default to A if no letter indication (less common)
    if any(action in command for action in ["execute", "engage", "initiate", "run", "activate"]):
        return f"{task_number}A"
    
    return None

def execute_task(task_code):
    """
    Executes the actions associated with the given task code.
    Returns a tuple (success, message) where:
    - success: True if task execution was successful, False otherwise
    - message: Response message about the execution
    """
    if task_code not in TASKS:
        return False, f"Unknown task code: {task_code}"
    
    task_actions = TASKS[task_code]
    
    try:
        for action in task_actions:
            if action["type"] == "web":
                webopen(action["target"])
            elif action["type"] == "browser":
                if action["target"].lower() == "edge":
                    appopen("edge", match_closest=True)
                else:
                    appopen(action["target"], match_closest=True)
            elif action["type"] == "app":
                appopen(action["target"], match_closest=True)
        
        # Simple, clean response as requested
        return True, f"Executed task {task_code}"
    
    except Exception as e:
        return False, f"Error executing task {task_code}"

def handle_task_command(command):
    """
    Main function to handle task commands.
    Returns a response message if a task command was detected and executed,
    or None if the command was not a task command.
    """
    # If the command contains "jarvis", remove it for cleaner processing
    if "jarvis" in command.lower():
        command = re.sub(r'\bjarvis\b', '', command, flags=re.IGNORECASE).strip()
    
    task_code = interpret_task_command(command)
    
    if task_code:
        success, message = execute_task(task_code)
        return message
    
    return None

if __name__ == "__main__":
    # Test the task executor - extensive testing of variations
    test_commands = [
        # Standard formats
        "Execute task 48A",
        "Engage 17A",
        "Initiate protocol 48B",
        "Engage with protocol 48b",
        "Engage with protocol 48B",
        "Engage with protocol 48 to be",
        "Run 17B",
        # Variations with "to be"
        "Activate task 48 to be",
        "Jarvis execute 48 to be",
        "Jarvis execute task 48 to be",
        "48 to be",
        # Space variations
        "execute 48 b",
        "execute 48 b.",
        "Execute 48 b.",
        "Execute 48 b",
        "execute task 48 b",
        "execute 48b",
        "execute task 48b",
        "execute task 48b.",
        "execute task 48 to be.",
        "execute task 48 to be",
        "execute48b",
        "executetask48b",
        # Standalone formats
        "48b",
        "48 b",
        "17a",
        "17 a",
        # With Jarvis prefix
        "jarvis execute 48b",
        "jarvis execute task 48b",
        "jarvis execute task 48 to be",
        "jarvis execute task 48 to be.",
        "jarvis 48b",
        "jarvis task 48b",
        "jarvis, 48b please",
        "jarvis, task 48b please",
        # Mixed case
        "ExEcUtE 48B",
        "ExEcUtE task 48B",
        "48To Be",
        # Extra text
        "execute task 48b right now",
        "execute task 48 to be right now",
        "hey jarvis can you please execute task 48b for me",
        "hey jarvis can you please execute task 48 to be for me",
        # Non-task sentences (should return None)
        "I want to be a doctor",
        "48 is my favorite number and I want to be happy"
    ]
    
    for cmd in test_commands:
        result = handle_task_command(cmd)
        print(f"Command: {cmd}")
        print(f"Result: {result}")
        print("-" * 50)