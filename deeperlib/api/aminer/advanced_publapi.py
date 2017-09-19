from sys import stderr as perr
import requests
import simplejson
import copy
from time import sleep
import deeperlib.api.simapi
import deeperlib.api.simthread


class AdvancedPublApi(deeperlib.api.simapi.SimpleApi):
    """
    A subclass implemented for aminer/search/pub/advanced api----https://api.aminer.org/api/search/pub/advanced
    """

    def __init__(self, top_k, delay, search_term, **kwargs):
        """
        Initialize the object. Set url and create session. Set other parameters and top_k for
        future api call.

        :param top_k: top-k constraint
        :param delay: time interval between a failed api call and the next api call
        :param search_term: the field for query string
        :param kwargs: other parameters
        """
        deeperlib.api.simapi.SimpleApi.__init__(self)
        self.setTopk(top_k)
        self.setDelay(delay)
        self.setSearchTerm(search_term)
        self.setKwargs(kwargs)
        self.setURL("https://api.aminer.org/api/search/pub/advanced")
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
                if 'result' in re:
                    result = re['result']
                    return result
                else:
                    return []
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
        size = self.__kwargs['size']
        page = (self.__topk + size - 1) / size
        threads = []
        for query in queries:
            for p in range(0, page):
                params = self.getKwargs()
                params[self.__searchTerm] = '+'.join(query)
                params['offset'] = p * size
                t = deeperlib.api.simthread.SimpleThread(self.callAPI, (params,), self.callAPI.__name__)
                threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        mresult = []
        for t in threads:
            mresult.extend(t.getResult())
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
        pass

    def getID(self):
        pass

    def setToken(self):
        pass

    def getToken(self):
        pass

    def setSession(self, session):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            'Accept': "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
        }
        session.headers = headers
        self.__session = session

    def getSession(self):
        return self.__session
