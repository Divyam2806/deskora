import os
import webbrowser
import subprocess
from assistant.skills.decorator import skill


@skill
def open_browser():
    """Opens the default web browser. Example: 'I want to surf the internet.'"""
    webbrowser.open("https://www.google.com")

# Predefined aliases (do not give space between 2 words)
APP_ALIASES = {
    "calculator": "calc",
    "notepad": "notepad",
    "vscode": "code",
    "explorer": "explorer",
    "commandprompt": "cmd",
}

@skill
def open_application(app_name: str) -> str:
    """
        Opens a desktop application on a Windows system.
        Args:
            app_name (str): The name of the application the user wants to open.
        Example:
            User says "Open app_name" → call open_application("app_name")
        """
    app_key = app_name.strip().lower().replace(" ", "")
    command = APP_ALIASES.get(app_key, app_key)  # fallback to raw name

    try:
        subprocess.Popen(command)
        return f"Opening {app_name}"
    except FileNotFoundError:
        # Fallback: try launching via Windows shell
        try:
            os.system(f'start "" {command}')
            return f"Opening {app_name}"
        except Exception as e:
            return f"Couldn't open '{app_name}'. Error: {e}"