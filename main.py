from assistant.core import handle_input
from assistant.database import init_db

def main():
    init_db()
    print("Assistant is ready! Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Terminating Assistant.")
            break

        handle_input(user_input)

if __name__ == "__main__":
    main()