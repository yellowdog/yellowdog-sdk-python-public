from threading import Thread


class ChainedThread(Thread):
    def __init__(self, callback, target):   # NOSONAR
        super(ChainedThread, self).__init__()
        self.__target = target
        self.__callback = callback

    def run(self):
        try:
            res = self.__target()
        finally:
            del self.__target
        self.__callback(res)
