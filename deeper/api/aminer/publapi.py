from sys import stderr as perr
import requests
import simplejson
import copy
from time import sleep
import deeper.api.simapi
import deeper.api.simthread


class PublApi(deeper.api.simapi.SimpleApi):
    def __init__(self, top_k, delay, search_term, **kwargs):
        deeper.api.simapi.SimpleApi.__init__(self)
        self.setTopk(top_k)
        self.setDelay(delay)
        self.setSearchTerm(search_term)
        self.setKwargs(kwargs)
        self.setURL("https://api.aminer.org/api/search/pub")
        self.setSession(requests.session())

    def setTopk(self, top_k):
        self.__topk = top_k

    def getTopk(self):
        return self.__topk

    def callAPI(self, params):
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
        size = self.__kwargs['size']
        page = (self.__topk + size - 1) / size
        threads = []
        for query in queries:
            for p in range(0, page):
                params = self.getKwargs()
                params[self.__searchTerm] = ' '.join(query)
                params['offset'] = p * size
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
