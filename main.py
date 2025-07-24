from assistant.core import handle_input
from assistant.database import init_db
from assistant.planner import initialize_assistant


def main():
    init_db()
    initialize_assistant()
    print("Assistant is ready! Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Terminating Assistant.")
            break

        handle_input(user_input)

if __name__ == "__main__":
    main()