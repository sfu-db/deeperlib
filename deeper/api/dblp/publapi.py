from sys import stderr as perr
import requests
import simplejson
import copy
from time import sleep
import deeper.api.simapi
import deeper.api.simthread


class PublApi(deeper.api.simapi.SimpleApi):
    """
    A subclass implemented for dblp/search/publ api----http://dblp.org/search/publ/api
    """

    def __init__(self, delay, search_term, **kwargs):
        """
        Initialize the object. Set url and create session. Set other parameters for future api call.

        :param delay: time interval between a failed api call and the next api call
        :param search_term: the field for query string
        :param kwargs: other parameters
        """
        deeper.api.simapi.SimpleApi.__init__(self)
        self.setDelay(delay)
        self.setSearchTerm(search_term)
        self.setKwargs(kwargs)
        self.setSession(requests.session())
        self.setURL('http://dblp.org/search/publ/api')

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
                if 'hit' in re['result']['hits']:
                    return re['result']['hits']['hit']
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
        threads = []
        for query in queries:
            params = self.getKwargs()
            params[self.__searchTerm] = '+'.join(query)
            t = deeper.api.simthread.SimpleThread(self.callAPI, (params,), self.callAPI.__name__)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        mresult = []
        for t in threads:
            mresult.extend(t.getResult())
        return mresult

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
        self.__kwargs['format'] = 'json'

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

    def getToken(self):
        pass

    def setToken(self):
        pass

    def setSession(self, session):
        self.__session = session

    def getSession(self):
        return self.__session
