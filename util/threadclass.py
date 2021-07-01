from abc import abstractmethod
from threading import Thread, Lock


class ThreadClass:
    def __init__(self):
        self.lock = Lock()
        self.stopped = False

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    @abstractmethod
    def run(self):
        pass
