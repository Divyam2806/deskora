import sys
from PyQt6.QtWidgets import QApplication
from multiprocessing import Process, Queue
from pet import DeskoraEntity
from backend import backend_worker

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()  # Required for Windows multiprocessing

    # Setup IPC
    prompt_queue = Queue()
    response_queue = Queue()

    # Start backend
    backend_process = Process(target=backend_worker, args=(prompt_queue, response_queue))
    backend_process.start()

    print("Waiting for backend ready...")
    while True:
        msg = response_queue.get()
        if msg == "__READY__":
            break

    # Start GUI

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    entity_window = DeskoraEntity(prompt_queue, response_queue)
    entity_window.show()
    print("gui started")

    exit_code = app.exec()
    # Clean shutdown
    prompt_queue.put(None)
    backend_process.join()
    sys.exit(exit_code)