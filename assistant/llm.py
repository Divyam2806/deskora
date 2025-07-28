from llama_cpp import Llama
from assistant.memory import load_memory



# llm = Llama(
#     model_path="models/phi3-mini.gguf",  # your downloaded model
#     n_ctx=3000,                          # context size
#     n_threads=9,
#     verbose=False,
#     chat_format= "chatml"
# ) code commented bcs instead of llm, gemini is being used

_system_prompt_cache = None

def get_system_prompt(force_refresh=False) -> str:
    global _system_prompt_cache
    if _system_prompt_cache is None or force_refresh:
        _system_prompt_cache = build_system_prompt()
    return _system_prompt_cache

# Build dynamic system prompt based on memory
# def build_system_prompt():
#     memory = load_memory()
#     prefs = memory.get("preferences", {})
#     facts = memory.get("facts", {})
#
#     tone = prefs.get("tone", "neutral")
#     emojis = prefs.get("emojis", True)
#     concise = prefs.get("concise", False)
#     name = facts.get("name", "friend")
#     project = facts.get("project", "your ongoing work")
#
#     style = f"Respond in a {tone} tone."
#     if emojis:
#         style += " Use emojis to sound friendly."
#     if concise:
#         style += " Keep your responses short and to the point."
#
#     return (
#         f"You are a helpful desktop assistant named Deskora.\n"
#         f"The user is named {name} and is working on {project}.\n"
#         f"{style}"
#     )

# SYSTEM_PROMPT = build_system_prompt()

# New function to send any prompt and get raw response
def generate_response(user_prompt: str) -> str:
    result = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=512
    )
    return result["choices"][0]["message"]["content"].strip()