import json, regex as re
from assistant.llm import generate_response #if using local llm
from assistant.gemini_llm import generate_response_from_gemini, initial_assistant_prompt
from assistant.memory import load_memory
from assistant.skills import skill_registry


def extract_json(text: str) -> dict:
    """Extract and parse the first valid JSON block with 'reply' and 'actions' keys."""
    matches = re.findall(r"\{(?:[^{}]|(?R))*\}", text, re.DOTALL)

    for candidate in matches:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict) and "reply" in parsed and "actions" in parsed:
                return parsed
        except json.JSONDecodeError:
            continue

    return {"reply": "Sorry, I didn't quite understand that.", "actions": []}


def get_skill_docs() -> dict:
    """Extracts all skill names and their docstrings from the registered skills."""
    docs = {}
    for name, func in skill_registry.items():
        if func.__doc__:
            docs[name] = func.__doc__.strip()
    return docs


def build_planner_prompt() -> str:
    skill_docs = get_skill_docs()

    skill_descriptions = "\n".join([
        f"- {name}: {desc.split('Example:')[0].strip()}\n  Example:{desc.split('Example:')[1].strip()}"
        if "Example:" in desc else f"- {name}: {desc}"
        for name, desc in skill_docs.items()
    ])

    memory = load_memory()
    prefs = memory.get("preferences", {})
    facts = memory.get("facts", {})

    tone = prefs.get("tone", "neutral")
    emojis = prefs.get("emojis", True)
    concise = prefs.get("concise", False)
    name = facts.get("name", "friend")
    project = facts.get("project", "your ongoing work")

    style = f"Respond in a {tone} tone."
    if emojis:
        style += " Use emojis to sound friendly."
    if concise:
        style += " Keep your responses short and to the point."


    system = f"You are a helpful desktop assistant named Deskora.\nThe user is named {name} and is working on {project}.\n{style}"

    instructions = f"""
You are a smart AI assistant named Diskora that plans how to respond to a user.
When the user gives an input, your job is to:

1. Reply in natural language as the assistant.
2. Generate a list of actions:
   - Use `"type": "run"` with `"skill"` to run assistant skills.
   - Use `"type": "store"` with `"key"` and `"value"` to store facts **only if the input contains a new fact**.

Here are the available skills you can use:
{skill_descriptions}

Only include items in the 'actions' list if they are clearly needed:\n
- Use a 'run' action if the user wants to trigger a specific skill (e.g., open an app).\n
- Use a 'store' action only if the user gives you a new piece of factual information that should be remembered long-term (e.g., their name, preferences, goals).\n
- If the input doesn't involve a skill or fact, leave 'actions' as an empty list.\n\n
Do NOT store general advice, step-by-step instructions, or explanations — those belong in the 'reply'.\n\n
Format your entire response as a strict JSON object like this:\n

{{
  "reply": "<natural language reply to the user>",
  "actions": [
    {{ "type": "run", "skill": "<skill_name>", "args":[<arguments_list>] }},
    {{ "type": "store", "key": "<fact_key>", "value": "<fact_value>" }}
  ]
}}
Include only valid JSON. Do not add any markdown, explanations, or text outside the JSON.\n\n
Now, based on the user's input that will be provided later, generate your JSON response:\n

"""

    return f"{system}\n\n{instructions}"

# User: {user_input}

#initialize assistant with starter prompt
def initialize_assistant():
    initial_assistant_prompt(build_planner_prompt())

def generate_plan_from_input(user_input: str) -> dict:
    # prompt = build_planner_prompt(user_input)
    # raw_response = generate_response(prompt)
    raw_response = generate_response_from_gemini(user_input)

    # print("[DEBUG] The raw response is:\n", raw_response)

    parsed_data = extract_json(raw_response)

    print("[DEBUG] The JSON response is:\n", parsed_data)

    if not parsed_data:
        print("[ERROR] No JSON found in LLM output.")
        print(raw_response)
        return {"reply": "Sorry, I didn't understand that.", "actions": []}

    # No need to json.loads again — it's already parsed
    return parsed_data

