import json, re
from assistant.llm import generate_response
from assistant import skills

def extract_json(text: str) -> str:
    """Try to extract the first {...} JSON block from LLM output"""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None

def get_skill_docs() -> dict:
    """Extracts all skill function names and their docstrings from skills.py"""
    docs = {}
    for name in dir(skills):
        func = getattr(skills, name)
        if callable(func) and func.__doc__:
            docs[name] = func.__doc__.strip()
    return docs


def build_planner_prompt(user_input: str) -> str:
    skill_docs = get_skill_docs()

    skill_descriptions = "\n".join([
        f"- {name}: {desc.split('Example:')[0].strip()}\n  Example:{desc.split('Example:')[1].strip()}"
        if "Example:" in desc else f"- {name}: {desc}"
        for name, desc in skill_docs.items()
    ])

    return f"""
You are a smart AI assistant named Diskora that plans how to respond to a user.
When the user gives an input, your job is to:

1. Reply in natural language as the assistant.
2. Generate a list of actions to run (skills) or store (facts).

Here are the available skills you can use:
{skill_descriptions}

Use this format strictly:

{{
  "reply": "<natural language reply to the user>",
  "actions": [
    {{ "type": "run", "skill": "<skill_name>" }},
    {{ "type": "store", "key": "<fact_key>", "value": "<fact_value>" }}
  ]
}}

Only respond with the JSON object. Do not explain, do not greet, do not add extra text outside the JSON block.

User: {user_input}
""".strip()


def generate_plan_from_input(user_input: str) -> dict:
    prompt = build_planner_prompt(user_input)
    raw_response = generate_response(prompt)

    json_string = extract_json(raw_response)
    if not json_string:
        print("[ERROR] No JSON found in LLM output.")
        print(raw_response)
        return {"reply": "Sorry, I didn't understand that.", "actions": []}

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        print("[WARN] LLM gave malformed JSON:")
        print(raw_response)
        return {
            "reply": "Sorry, I didn't quite understand that.",
            "actions": []
        }
