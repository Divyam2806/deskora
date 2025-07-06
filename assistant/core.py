from assistant.planner import generate_plan_from_input
from assistant.skills import run_skill
from assistant.database import set_fact

def say(message: str):
    print(f"Assistant: {message}")

def handle_input(user_input: str):
    plan = generate_plan_from_input(user_input)

    say(plan.get("reply", "Okay."))

    for action in plan.get("actions", []):
        if action["type"] == "run":
            run_skill(action["skill"])
        elif action["type"] == "store":
            set_fact(action["key"], action["value"])