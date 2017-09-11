import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
from data_process import wordset


class HiddenData:
    def __init__(self, resultpath, matchpath, uniqueid, matchlist):
        self.setResultPath(resultpath)
        self.setMatchPath(matchpath)
        self.setUniqueId(uniqueid)
        self.setMatchList(matchlist)
        self.setMergeResult({})

    def proResult(self, result_raw):
        result_merge = self.__mergeResult
        result_er = []
        for row in result_raw:
            r_id = eval(self.__uniqueId)
            if r_id not in result_merge:
                result_merge[r_id] = row
                bag = []
                for v in self.__matchList:
                    try:
                        bag.extend(wordset(eval(v)))
                    except KeyError:
                        continue
                result_er.append((bag, r_id))
        self.setMergeResult(result_merge)
        return result_er

    def saveResult(self):
        resultList = self.__mergeResult.values()
        with open(self.__resultPath, 'wb') as f:
            pickle.dump(resultList, f)

    def saveMatchPair(self):
        savePair = {}
        for m in self.__matchPair:
            savePair[m[0]] = []
        for m in self.__matchPair:
            savePair[m[0]].append(m[1])
        with open(self.__matchPath, 'wb') as f:
            pickle.dump(savePair, f)

    def setResultPath(self, resultpath):
        self.__resultPath = resultpath

    def getResultPath(self):
        return self.__resultPath

    def setMatchPath(self, matchpath):
        self.__matchPath = matchpath

    def getMatchPath(self):
        return self.__matchPath

    def setUniqueId(self, uniqueid):
        self.__uniqueId = uniqueid

    def getUniqueId(self):
        return self.__uniqueId

    def setMatchList(self, matchlist):
        self.__matchList = matchlist

    def getMatchList(self):
        return self.__matchList

    def setMatchPair(self, matchpair):
        self.__matchPair = matchpair

    def getMatchPair(self):
        return self.__matchPair

    def setMergeResult(self, mergeresult):
        self.__mergeResult = mergeresult

    def getMergeResult(self):
        return self.__mergeResult
