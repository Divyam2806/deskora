import os
import webbrowser

def open_calculator():
    """Opens the system calculator. Example: 'Can you open the calculator?'"""
    os.system("calc" if os.name == "nt" else "gnome-calculator")

def open_browser():
    """Opens the default web browser. Example: 'I want to surf the internet.'"""
    webbrowser.open("https://www.google.com")

def get_skills():
    return {
        "open calculator": open_calculator,
        "open browser": open_browser,
    }


# change this func later to not be so hardcoded
def run_skill(skill_name: str):
    if skill_name == "open_calculator":
        open_calculator()
    elif skill_name == "open_browser":
        open_browser()
    else:
        print(f"[WARN] Unknown skill: {skill_name}")