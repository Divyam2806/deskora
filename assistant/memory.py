
import json
import os

MEMORY_FILE = "memory.json"

# Default memory structure
DEFAULT_MEMORY = {
    "preferences": {
        "tone": "neutral",
        "emojis": True,
        "concise": False
    },
    "facts": {},
    "feedback": []
}

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_MEMORY.copy()

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_fact(key: str, value: str):
    memory = load_memory()
    memory["facts"][key] = value
    save_memory(memory)
    print(f"[MEMORY] Saved fact: {key} = {value}")

