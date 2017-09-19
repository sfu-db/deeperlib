from sys import stderr as perr
import pickle
import csv
from data_process import wordset, getElement


class SampleData:
    """
    A SampleData object would read the data from input file and then process the raw data. At last,
    it would generate a dict for query pool generation.
    """

    def __init__(self, sample_ratio, samplepath, filetype, uniqueid, querylist):
        """
        Initialize the object. The data structures of messages input by users or developers are so different
        that users or developers have to define the uniqueid and querylist of the messages manually.

        :param sample_ratio: the ratio of sample.
        :param samplepath: the path of input file.
        :param filetype: file type
        :param uniqueid: the uniqueid of messages in the file.
        :param querylist: the fields of messages for query pool generation.
        """
        self.setRatio(sample_ratio)
        self.setSamplePath(samplepath)
        self.setFileType(filetype)
        self.setUniqueId(uniqueid)
        self.setQueryList(querylist)
        if self.__filetype == 'pkl':
            self.read_pickle()
        elif self.__filetype == 'csv':
            self.read_csv()
        else:
            print >> perr, 'This file type is not supported now.'
            exit(0)

    def read_pickle(self):
        """
        Load sample data and then generate a same data structures as localdata_query used for smart crawl.

        **sample** Split the fields into a list of words defined by querylist of each message.
        Then generate a dict for query pool generation. {'uniqueid':['database'. 'laboratory']}
        """
        with open(self.__samplePath, 'rb') as f:
            sample_raw = pickle.load(f)

        uniqueid = self.__uniqueId.split('.')
        querylist = []
        for q in self.__queryList:
            querylist.append(q.split('.'))

        sample = {}
        for row in sample_raw:
            r_id = getElement(uniqueid, row)
            bag = []
            for q in querylist:
                bag.extend(wordset(getElement(q, row)))
            sample[r_id] = bag
        self.setSample(sample)

    def read_csv(self):
        """
        Load sample data and then generate a same data structures as localdata_query used for smart crawl.

        **sample** Split the fields into a list of words defined by querylist of each message.
        Then generate a dict for query pool generation. {'uniqueid':['database'. 'laboratory']}
        """
        with open(self.__samplePath, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            sample_raw = [row for row in reader]

        uniqueid_index = 0
        querylist_index = []
        try:
            header = sample_raw.pop(0)
            uniqueid_index = header.index(self.__uniqueId)
            for q in self.__queryList:
                querylist_index.append(header.index(q))
        except ValueError:
            print >> perr, "Can't find attributes"
            exit(0)

        sample = {}
        for row in sample_raw:
            try:
                r_id = row[uniqueid_index]
            except IndexError:
                continue
            bag = []
            for q in querylist_index:
                try:
                    bag.extend(wordset(row[q]))
                except IndexError:
                    continue
            sample[r_id] = bag
        self.setSample(sample)

    def setSamplePath(self, samplepath):
        self.__samplePath = samplepath

    def getSamplePath(self):
        return self.__samplePath

    def setFileType(self, filetype):
        self.__filetype = filetype.lower().strip()

    def getFileType(self):
        return self.__filetype

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

    def setRatio(self, sample_ratio):
        self.__sampleRatio = sample_ratio

    def getRatio(self):
        return self.__sampleRatio