from module import Module
import threading


class ThreadModule(Module):
    def __init__(self, pipes):
        super(Module).__init__()
        self._pipes = pipes
        self._thread = threading.Thread(target=self.run)

    def run(self):
        raise NotImplementedError()

    def start(self):
        self._thread.start()

    def join(self):
        return self._thread.join()

    def get_pipes(self):
        return self._pipes
