import pickle
import os
from data_process import wordset, getElement
from json2csv import Json2csv


class HiddenData:
    """
    A HiddenData object would keep the data crawled from api in json format in a dict. It provides you
    with some methods to manipulate the data, such as, defining your own way to pre-process the
    raw_data, saving the data and matched pairs to files.
    """

    def __init__(self, result_dir, uniqueid, matchlist):
        """
        Initialize the object. The data structures of messages returned by various api are so different
        that users or developers have to define the uniqueid and matchlist of the messages manually.

        :param result_dir: the target directory for output files.
        :param uniqueid: the uniqueid of returned messages.
        :param matchlist: the fields of returned messages for similarity join.
        """
        self.setResultDir(result_dir)
        self.setUniqueId(uniqueid)
        self.setMatchList(matchlist)
        self.setMergeResult({})

    def proResult(self, result_raw):
        """
        Merge the raw data and keep them in a dict. Then, pre-process the raw data for similarity join.

        :param result_raw: the raw result returned by api.
        :return: a list for similarity join. [(['yong', 'jun', 'he', 'simon', 'fraser'],'uniqueid')]
        """
        uniqueid = self.__uniqueId.split('.')
        matchlist = []
        for m in self.__matchList:
            matchlist.append(m.split('.'))

        result_merge = self.__mergeResult
        result_er = []
        for row in result_raw:
            r_id = getElement(uniqueid, row)
            if r_id not in result_merge:
                result_merge[r_id] = row
                bag = []
                for m in matchlist:
                    bag.extend(wordset(getElement(m, row)))
                result_er.append((bag, r_id))
        self.setMergeResult(result_merge)
        return result_er

    def saveResult(self):
        """
        Save the returned massages in the target directory.
        result_dir\\result_file.pkl

                    result_file.csv

                    match_file.pkl

                    match_file.csv
        """
        resultList = self.__mergeResult.values()
        if not os.path.exists(self.__resultDir):
            os.makedirs(self.__resultDir)
        with open(self.__resultDir + '/result_file.pkl', 'wb') as f:
            pickle.dump(resultList, f)
        print self.__resultDir + '/result_file.pkl saved successfully'

        Json2csv(resultList, self.__resultDir + '/result_file.csv')
        print self.__resultDir + '/result_file.csv saved successfully'

    def saveMatchPair(self):
        """
        Save the returned massages in the target directory.
        result_dir\\result_file.pkl

                    result_file.csv

                    match_file.pkl

                    match_file.csv
        """
        savePair = {}
        for m in self.__matchPair:
            savePair[m[0]] = []
        for m in self.__matchPair:
            savePair[m[0]].append(m[1])

        saveList = []
        for q, v in savePair.iteritems():
            saveList.append({'local_id': q, 'remote_id': v})

        if not os.path.exists(self.__resultDir):
            os.makedirs(self.__resultDir)
        with open(self.__resultDir + '/match_file.pkl', 'wb') as f:
            pickle.dump(saveList, f)
        print self.__resultDir + '/match_file saved successfully'

        Json2csv(saveList, self.__resultDir + '/match_file.csv')
        print self.__resultDir + '/match_file.csv saved successfully'

    def setResultDir(self, result_dir):
        self.__resultDir = result_dir

    def getResultDir(self):
        return self.__resultDir

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
