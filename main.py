from assistant.core import handle_input
from assistant.database import init_db
from assistant.planner import initialize_assistant
from assistant.settings import get_setting
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

        if user_input.lower() == "exit":
            print("Terminating Assistant.")
            break

        handle_input(user_input)

if __name__ == "__main__":
    main()