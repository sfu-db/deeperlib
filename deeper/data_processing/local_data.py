import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
from data_process import wordset


class LocalData:
    """
    A LocalData object would read the data from input file and then process the raw data. At last,
    it would generate a set of uniqueid, .a list for similarity join and a dict for query pool generation.
    """

    def __init__(self, localpath, uniqueid, querylist, matchlist):
        """
        Initialize the object. The data structures of messages input by users or developers are so different
        that users or developers have to define the uniqueid, querylist and matchlist of the messages manually.

        :param localpath: The path of input file.
        :param uniqueid: The uniqueid of messages in the file.
        :param querylist: The fields of messages for query pool generation..
        :param matchlist: The fields of messages for similarity join.
        """
        self.setLocalPath(localpath)
        self.setUniqueId(uniqueid)
        self.setQueryList(querylist)
        self.setMatchList(matchlist)
        self.loadLocalData()

    def loadLocalData(self):
        """
        Load local data and then generate three important data structures used for smart crawl.
        **localdata_ids** Collect a set of uniqueid. ('uniqueid1', 'uniqueid2')

        **localdata_query** Split the fields into a list of words defined by querylist of each message.
        Filter out stop words and words whose length<3 from the list of words.
        Then generate a dict for query pool generation. {'uniqueid':['database'. 'laboratory']}

        **localdata_er** A list for similarity join. [(['yong', 'jun', 'he', 'simon', 'fraser'],'uniqueid')]
        """
        with open(self.__localPath, 'rb') as f:
            data_raw = pickle.load(f)
        localdata_query = {}
        localdata_er = []
        localdata_ids = set()
        stop_words = ['and', 'for', 'the', 'with', 'about']
        for row in data_raw:
            try:
                r_id = eval(self.__uniqueId)
            except KeyError:
                continue
            localdata_ids.add(r_id)
            tempbag = []
            for v in self.__queryList:
                tempbag.extend(wordset(eval(v)))
            bag = []
            for word in tempbag:
                if word not in stop_words and len(word) >= 3:
                    bag.append(word)
            localdata_query[r_id] = bag
            bag = []
            for v in self.__matchList:
                try:
                    bag.extend(wordset(eval(v)))
                except KeyError:
                    continue
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
