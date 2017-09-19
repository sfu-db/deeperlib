from abc import ABCMeta, abstractmethod


class SimpleApi:
    """
    An interface of many abstract methods. Users or developers could build their own subclasses of SimpleApi
    to support specific api.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def callAPI(self, params):
        return

    @abstractmethod
    def callMulAPI(self, queries):
        return

    @abstractmethod
    def setTopk(self, top_k):
        return

    @abstractmethod
    def getTopk(self):
        return

    @abstractmethod
    def setDelay(self, delay):
        return

    @abstractmethod
    def getDelay(self):
        return

    @abstractmethod
    def setSearchTerm(self, search_term):
        return

    @abstractmethod
    def getSearchTerm(self):
        return

    @abstractmethod
    def setKwargs(self, kwargs):
        return

    @abstractmethod
    def getKwargs(self):
        return

    @abstractmethod
    def setURL(self, url):
        return

    @abstractmethod
    def getURL(self):
        return

    @abstractmethod
    def setID(self, client_id, client_secret):
        return

    @abstractmethod
    def getID(self):
        return

    @abstractmethod
    def setToken(self):
        return

    @abstractmethod
    def getToken(self):
        return

    @abstractmethod
    def setSession(self, session):
        return

    @abstractmethod
    def getSession(self):
        return
