from assistant.core import handle_input
from assistant.database import init_db
from assistant.planner import initialize_assistant

def start_assistant():
    """
    Initializes the assistant (DB, planner, etc.).
    Call this once in backend process.
    """
    init_db()
    initialize_assistant()
    print("Assistant is ready!")

def process_prompt(prompt: str) -> str:
    """
    Handles a single user prompt and returns the response.
    """
    response = handle_input(prompt)
    return response or "No response generated."
