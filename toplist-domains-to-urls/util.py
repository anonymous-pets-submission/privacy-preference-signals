from pathlib import Path
import threading
import queue

data = Path(".")

def as_completed(worker_fn, tasks, workers: int = 100):
    todo = queue.Queue()
    for task in tasks:
        todo.put_nowait(task)

    results = queue.Queue()

    def worker():
        while True:
            try:
                task = todo.get_nowait()
            except queue.Empty:
                return

            try:
                result = worker_fn(task)
            except Exception as e:
                results.put(e)
            else:
                results.put(result)

    for _ in range(workers):
        threading.Thread(target=worker).start()

    def result_iter():
        for _ in range(len(tasks)):
            result = results.get()
            if isinstance(result, Exception):
                raise result
            else:
                yield result

    return result_iter()
