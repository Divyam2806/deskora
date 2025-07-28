import os
import webbrowser

from assistant.skills.decorator import skill


@skill
def open_calculator():
    """Opens the system calculator. Example: 'Can you open the calculator?'"""
    os.system("calc" if os.name == "nt" else "gnome-calculator")

@skill
def open_browser():
    """Opens the default web browser. Example: 'I want to surf the internet.'"""
    webbrowser.open("https://www.google.com")