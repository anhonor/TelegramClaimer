import json
import queue
import threading
from typing import Union

class Processor:
    def __init__(self, threads: int = 50) -> None:
        self.tasks = queue.Queue()
        self.thread_count = threads
        self.thread_lock = threading.Lock()
        self.thread_stop_event = threading.Event()

        self.threads = set()

        for thread in range(self.thread_count):
            worker = threading.Thread(target = self.newWorker)
            worker.daemon = True
            worker.start()
            self.threads.add(worker)

    def newTask(self, *args, **kwargs) -> None:
        self.tasks.put((args, kwargs))

    def newWorker(self) -> None:
        while not self.thread_stop_event.is_set():
            try:
                task = self.tasks.get(timeout=1)
                if task is None:
                    continue
                args, kwargs = task
                args[1](*args, **kwargs)
                self.tasks.task_done()
            except queue.Empty:
                continue

    def waitCompletion(self) -> None:
        self.tasks.join()

    def stop(self) -> None:
        self.thread_stop_event.set()
        for thread in self.threads:
            thread.join()
