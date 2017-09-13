import threading


class SimpleThread(threading.Thread):
    """
    A simple subclass of the Thread class. We can create new thread for customized function easily.
    """

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        self.res = apply(self.func, self.args)
