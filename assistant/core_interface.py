# deskora_backend.py
from assistant.core import handle_input
from assistant.database import init_db
from assistant.planner import initialize_assistant
from assistant.settings import get_setting, set_setting
from speech.listener import listen
from multiprocessing import Process, Queue


def process_prompt(prompt, response_queue):
    """
    This function processes a single prompt and sends the response back.
    It's designed to be run in a separate process.
    """
    try:
        response = handle_input(prompt)
        response_queue.put(response)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        response_queue.put(error_message)


def main():
    init_db()
    initialize_assistant()
    print("Assistant is ready! Type 'exit' to quit.")

    while True:
        user_input = ""

        if get_setting("listening_enabled"):
            user_input = listen()
            if not user_input:
                continue
        else:
            user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Terminating Assistant.")
            break

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

        # --- CORRECTED CODE BLOCK ---
        # Use a Queue to handle the response from the processing process
        response_queue = Queue()

        # Create and start a new process for each prompt
        p = Process(target=process_prompt, args=(user_input, response_queue))
        p.start()

        # Wait for the response to come back
        response = response_queue.get()
        p.join()  # Wait for the process to finish

        print(f"Assistant: {response}")
        # --- END OF CORRECTED CODE BLOCK ---


if __name__ == "__main__":
    main()