from assistant.planner import generate_plan_from_input
from assistant.settings import get_setting
from assistant.skills.executor import run_skill
from assistant.database import set_fact
from speech.speaker import speak


def say(message: str):
    print(f"Assistant: {message}")
    if get_setting("speaking_enabled"):
        speak(message)

def handle_input(user_input: str):
    plan = generate_plan_from_input(user_input)


    say(plan.get("reply", "Okay."))

    for action in plan.get("actions", []):
        if action["type"] == "run":
            run_skill(action["skill"], *action["args"])
        elif action["type"] == "store":
            set_fact(action["key"], action["value"])

    return plan.get("reply", "Okay.")