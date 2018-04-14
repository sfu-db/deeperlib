from sys import stderr as perr
import requests
import copy
import simplejson
from time import sleep
import deeperlib.api.simapi
import deeperlib.api.simthread


class DetailsApi(deeperlib.api.simapi.SimpleApi):
    def __init__(self, delay, search_term, **kwargs):
        """
        Initialize the object.
        Set other parameters and top_k for future api call.

        :param top_k: top-k constraint
        :param delay: time interval between a failed api call and the next api call
        :param search_term: the field for query string
        :param kwargs: other parameters
        """
        deeperlib.api.simapi.SimpleApi.__init__(self)
        self.setDelay(delay)
        self.setSearchTerm(search_term)
        self.setKwargs(kwargs)
        self.setURL('https://maps.googleapis.com/maps/api/place/details/json?')
        self.setSession(requests.session())

    def callAPI(self, params):
        """
        Call api until it returns messages successfully.

        :param params: all the parameters needed by an api
        :return: businesses in returned documents
        """
        while True:
            try:
                resp = self.__session.get(self.__searchURL, params=params)
                re = resp.json()
                return re
            except simplejson.scanner.JSONDecodeError:
                print >> perr, 'JSONDecodeError error!!!'
                sleep(self.__delay)
                continue
            except requests.ConnectionError:
                print >> perr, 'ConnectionError error!!!'
                sleep(self.__delay)
                continue

    def callMulAPI(self, queries):
        """
        Call api with multiple threads. Therefore, we can issue several queries and get all of the top k
        documents at the same time.

        :param queries: queries list
        :return: messages returned from api
        """
        threads = []
        for query in queries:
            params = self.getKwargs()
            params[self.__searchTerm] = query
            t = deeperlib.api.simthread.SimpleThread(self.callAPI, (params,), self.callAPI.__name__)
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        mresult = []
        for t in threads:
            re = t.getResult()
            if 'result' in re:
                mresult.append(re['result'])
        return mresult

    def setTopk(self, top_k):
        self.__topk = top_k

    def getTopk(self):
        return self.__topk

    def setDelay(self, delay):
        self.__delay = delay

    def getDelay(self):
        return self.__delay

    def setSearchTerm(self, search_term):
        self.__searchTerm = search_term

    def getSearchTerm(self):
        return self.__searchTerm

    def setKwargs(self, kwargs):
        self.__kwargs = kwargs

    def getKwargs(self):
        return copy.deepcopy(self.__kwargs)

    def setURL(self, url):
        self.__searchURL = url

    def getURL(self):
        return self.__searchURL

    def setID(self, client_id, client_secret):
        return

    def getID(self):
        return

    def setToken(self):
        return

    def getToken(self):
        return

    def setSession(self, session):
        self.__session = session

    def getSession(self):
        return self.__session
