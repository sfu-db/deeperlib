from sys import stderr as perr
import requests
import rauth
import copy
import simplejson
from time import sleep
import deeperlib.api.simapi
import deeperlib.api.simthread


class SearchApi(deeperlib.api.simapi.SimpleApi):
    """
    A subclass implemented for yelp/business/search api----https://www.yelp.com/developers/documentation/v3/business_search
    """

    def __init__(self, client_id, client_secret, top_k, delay, search_term, **kwargs):
        """
        Initialize the object. Set id and secret to obtain JWT Token. Create session with the token.
        Set other parameters and top_k for future api call.

        :param client_id: client_id
        :param client_secret: client_secret
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
        self.setURL('https://api.yelp.com/v3/businesses/search')
        self.setID(client_id, client_secret)
        self.setToken()
        self.setSession(session=rauth.OAuth2Session(access_token=self.__token["access_token"]))

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
                if 'businesses' in re:
                    result = re['businesses']
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
        limit = self.__kwargs['limit']
        page = (self.__topk + limit - 1) / limit
        threads = []
        for query in queries:
            for p in range(0, page):
                params = self.getKwargs()
                params[self.__searchTerm] = '+'.join(query)
                params['offset'] = p * limit
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
        self.__apiID = {"grant_type": "client_credentials"}
        self.__apiID['client_id'] = client_id
        self.__apiID['client_secret'] = client_secret

    def getID(self):
        return self.__apiID

    def setToken(self):
        self.__token = requests.post("https://api.yelp.com/oauth2/token", self.__apiID).json()

    def getToken(self):
        return self.__token

    def setSession(self, session):
        self.__session = session

    def getSession(self):
        return self.__session
