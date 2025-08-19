from assistant.core import handle_input
from assistant.database import init_db
from assistant.planner import initialize_assistant
from assistant.settings import get_setting, set_setting
from speech.listener import listen


def main():
    init_db()
    initialize_assistant()
    print("Assistant is ready! Type 'exit' to quit.")

    while True:
        # Decide how to get user input based on settings
        if get_setting("listening_enabled"):
            user_input = listen()
            if not user_input:
                continue  # Retry if voice input failed
        else:
            user_input = input("You: ").strip()  # fallback to keyboard

        # Handle toggle commands
        if user_input == "enable speaking":
            set_setting("speaking_enabled", True)
            print("Speaking enabled.")
            continue
        elif user_input == "disable speaking":
            set_setting("speaking_enabled", False)
            print("Speaking disabled.")
            continue
        elif user_input == "enable listening":
            set_setting("listening_enabled", True)
            print("Listening enabled.")
            continue
        elif user_input == "disable listening":
            set_setting("listening_enabled", False)
            print("Listening disabled.")
            continue

        if user_input.lower() == "exit":
            print("Terminating Assistant.")
            break


        handle_input(user_input)

if __name__ == "__main__":
    main()