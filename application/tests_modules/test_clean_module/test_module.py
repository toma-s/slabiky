from application.source.end import End
from application.source.thread_module import ThreadModule


class TestModule(ThreadModule):

    def __init__(self, pipes: list):
        super().__init__(pipes)
        self.received = []

    def run(self):
        pipe_in = self.get_pipes()[0]

        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                print('Test Module: No word yet, waiting')
                pipe_in.wait()
            word = pipe_in.get()
            pipe_in.release()

            self.received.append(word)
            print('Got item: {}, instance of \'{}\''.format(word, word.__class__.__name__))

            if isinstance(word, End):
                print('Clean Module: Got to the End')
                print('Clean Module: Finished working')
                break
