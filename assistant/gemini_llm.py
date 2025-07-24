import os
from dotenv import load_dotenv
from google import genai

# from assistant.planner import build_planner_prompt

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

# Constants
MESSAGE_LIMIT_BEFORE_SUMMARY = 10
# INITIAL_PROMPT=

# global state
client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-2.5-flash")
message_counter = 0

#summarize previous chats and reset message limit
def summarize_and_reset_chat():
    from assistant.planner import build_planner_prompt
    global message_counter, chat

    print("[DEBUG] summarizing chat......")

    # Get all messages except the initial instruction message
    messages = chat.get_history()[1:]

    # Extract all text parts for summarization
    message_texts = []
    for msg in messages:
        parts = [part.text for part in msg.parts if hasattr(part, "text")]
        message_texts.extend(parts)

    joined_text = "\n".join(message_texts)
    summary_prompt = (
            "Summarize the following conversation in a concise way. "
            "Focus on what the assistant learned, what facts were stored, "
            "and any unresolved user goals:\n\n"
            f"{joined_text}"
    )

    # Send to Gemini for summarization
    summary_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=summary_prompt
    )

    summary = summary_response.text.strip()

    # Start new chat and re-initialize with instruction + summary
    chat = client.chats.create(model="gemini-2.5-flash")
    chat.send_message(build_planner_prompt())
    chat.send_message(f"Here is the summary of our past conversation:\n{summary}")
    message_counter = 0

# prompt gemini api with user input
def generate_response_from_gemini(user_input: str) -> str:
    global message_counter
    message_counter += 1
    response = chat.send_message(user_input)

    if message_counter >= MESSAGE_LIMIT_BEFORE_SUMMARY:
        summarize_and_reset_chat()

    return response.text

# initialize the assistant with the starter instruction and system prompt
def initial_assistant_prompt(initial_prompt: str):
    chat.send_message(initial_prompt)
