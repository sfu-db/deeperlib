import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
from data_process import wordset


class SampleData:
    """
    A SampleData object would read the data from input file and then process the raw data. At last,
    it would generate a dict for query pool generation.
    """

    def __init__(self, samplepath, uniqueid, querylist):
        """
        Initialize the object. The data structures of messages input by users or developers are so different
        that users or developers have to define the uniqueid and querylist of the messages manually.

        :param samplepath: the path of input file.
        :param uniqueid: the uniqueid of messages in the file.
        :param querylist: the fields of messages for query pool generation..
        """
        self.setSamplePath(samplepath)
        self.setUniqueId(uniqueid)
        self.setQueryList(querylist)
        self.loadSample()

    def loadSample(self):
        """
        Load sample data and then generate a same data structures as localdata_query used for smart crawl.

        **sample** Split the fields into a list of words defined by querylist of each message.
        Then generate a dict for query pool generation. {'uniqueid':['database'. 'laboratory']}
        """
        with open(self.__samplePath, 'rb') as f:
            sample_raw = pickle.load(f)
        sample = {}
        for row in sample_raw:
            try:
                r_id = eval(self.__uniqueId)
            except KeyError:
                continue
            bag = []
            for v in self.__queryList:
                try:
                    bag.extend(wordset(eval(v)))
                except KeyError:
                    continue
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
