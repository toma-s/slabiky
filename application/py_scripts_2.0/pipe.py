class Pipe:
    def __init__(self, queue, condition):
        self._queue = queue
        self._condition = condition

    def acquire(self):
        return self._condition.acquire()

    def release(self):
        return self._condition.release()

    def wait(self):
        return self._condition.wait()

    def notify(self):
        return self._condition.notify()

    def put(self, value):
        self._queue.put(value)

    def get(self):
        return self._queue.get()

    def empty(self):
        return self._queue.empty()

    def get_queue(self):
        return self._queue

    def get_condition(self):
        return self._condition
