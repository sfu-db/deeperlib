import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
from data_process import wordset


class LocalData:
    def __init__(self, localpath, uniqueid, querylist, matchlist):
        self.setLocalPath(localpath)
        self.setUniqueId(uniqueid)
        self.setQueryList(querylist)
        self.setMatchList(matchlist)
        self.loadLocalData()

    def loadLocalData(self):
        with open(self.__localPath, 'rb') as f:
            data_raw = pickle.load(f)
        localdata_query = {}
        localdata_er = []
        localdata_ids = set()
        common_words = ['and', 'for', 'the', 'with', 'about']
        for row in data_raw:
            r_id = eval(self.__uniqueId)
            localdata_ids.add(r_id)
            tempbag = []
            for v in self.__queryList:
                tempbag.extend(wordset(eval(v)))
            bag = []
            for word in tempbag:
                if word not in common_words and len(word) >= 3:
                    bag.append(word)
            localdata_query[r_id] = bag
            bag = []
            for v in self.__matchList:
                bag.extend(wordset(eval(v)))
            localdata_er.append((bag, r_id))
        self.setlocalData(localdata_ids, localdata_query, localdata_er)

    def setLocalPath(self, localpath):
        self.__localPath = localpath

    def getLocalPath(self):
        return self.__localPath

    def setUniqueId(self, uniqueid):
        self.__uniqueId = uniqueid

    def getUniqueId(self):
        return self.__uniqueId

    def setQueryList(self, querylist):
        self.__queryList = querylist

    def getQueryList(self):
        return self.__queryList

    def setMatchList(self, matchlist):
        self.__matchList = matchlist

    def getMatchList(self):
        return self.__matchList

    def setlocalData(self, localdata_ids, localdata_query, localdata_er):
        self.__localdataIds = localdata_ids
        self.__localdataQuery = localdata_query
        self.__localdataEr = localdata_er

    def getlocalData(self):
        return self.__localdataIds, self.__localdataQuery, self.__localdataEr
