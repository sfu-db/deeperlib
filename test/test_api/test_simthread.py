import unittest
from deeper.api.simthread import SimpleThread


def sayhello():
    return 'hello'


class SimthreadTestCase(unittest.TestCase):
    def runTest(self):
        threads = []
        for i in range(3):
            t = SimpleThread(sayhello, (), sayhello.__name__)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        for t in threads:
            if t.getResult() != 'hello':
                assert False
        assert True
