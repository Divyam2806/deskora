from assistant.core_interface import start_assistant, process_prompt
from queue import Empty

# --- IPC Worker Function ---
def backend_worker(prompt_queue, response_queue):
    print("Backend worker process started.")
    start_assistant()
    response_queue.put("__READY__")
    while True:
        try:
            prompt = prompt_queue.get(timeout=1)
        except Empty:
            continue  # Check again

        if prompt is None:
            print("Backend worker shutting down.")
            break

        if prompt.lower() == "exit":
            response_queue.put("__SHUTDOWN__")  # special signal
            break

        print(f"Processing prompt: {prompt}")
        response = process_prompt(prompt)
        response_queue.put(response)
