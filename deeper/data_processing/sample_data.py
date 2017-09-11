import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
from data_process import wordset


class SampleData:
    def __init__(self, samplepath, uniqueid, querylist):
        self.setSamplePath(samplepath)
        self.setUniqueId(uniqueid)
        self.setQueryList(querylist)
        self.loadSample()

    def loadSample(self):
        with open(self.__samplePath, 'rb') as f:
            sample_raw = pickle.load(f)
        sample = {}
        for row in sample_raw:
            r_id = eval(self.__uniqueId)
            bag = []
            for v in self.__queryList:
                bag.extend(wordset(eval(v)))
            sample[r_id] = bag
        self.setSample(sample)

    def setSamplePath(self, samplepath):
        self.__samplePath = samplepath

    def getSamplePath(self):
        return self.__samplePath

    def setUniqueId(self, uniqueid):
        self.__uniqueId = uniqueid

    def getUniqueId(self):
        return self.__uniqueId

    def setQueryList(self, querylist):
        self.__queryList = querylist

    def getQueryList(self):
        return self.__queryList

    def setSample(self, sample):
        self.__sample = sample

    def getSample(self):
        return self.__sample
