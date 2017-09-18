from sys import stderr as perr
import pickle
import csv
from data_process import wordset, getElement


class LocalData:
    """
    A LocalData object would read the data from input file and then process the raw data. At last,
    it would generate a set of uniqueid, .a list for similarity join and a dict for query pool generation.
    """

    def __init__(self, localpath, filetype, uniqueid, querylist, matchlist):
        """
        Initialize the object. The data structures of messages input by users or developers are so different
        that users or developers have to define the uniqueid, querylist and matchlist of the messages manually.

        :param localpath: the path of input file.
        :param filetype: file type
        :param uniqueid: the uniqueid of messages in the file.
        :param querylist: the fields of messages for query pool generation..
        :param matchlist: the fields of messages for similarity join.
        """
        self.setLocalPath(localpath)
        self.setFileType(filetype)
        self.setUniqueId(uniqueid)
        self.setQueryList(querylist)
        self.setMatchList(matchlist)
        if self.__filetype == 'pkl':
            self.read_pickle()
        elif self.__filetype == 'csv':
            self.read_csv()
        else:
            print >> perr, 'This file type is not supported now.'
            exit(0)

    def read_pickle(self):
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

        uniqueid = self.__uniqueId.split('.')
        querylist = []
        for q in self.__queryList:
            querylist.append(q.split('.'))
        matchlist = []
        for m in self.__matchList:
            matchlist.append(m.split('.'))

        localdata_query = {}
        localdata_er = []
        localdata_ids = set()
        stop_words = ['and', 'for', 'the', 'with', 'about']
        for row in data_raw:
            r_id = getElement(uniqueid, row)
            localdata_ids.add(r_id)

            tempbag = []
            for q in querylist:
                tempbag.extend(wordset(getElement(q, row)))

            bag = []
            for word in tempbag:
                if word not in stop_words and len(word) >= 3:
                    bag.append(word)
            localdata_query[r_id] = bag

            bag = []
            for m in matchlist:
                bag.extend(wordset(getElement(m, row)))
            localdata_er.append((bag, r_id))
        self.setlocalData(localdata_ids, localdata_query, localdata_er)

    def read_csv(self):
        """
        Load local data and then generate three important data structures used for smart crawl.
        **localdata_ids** Collect a set of uniqueid. ('uniqueid1', 'uniqueid2')

        **localdata_query** Split the fields into a list of words defined by querylist of each message.
        Filter out stop words and words whose length<3 from the list of words.
        Then generate a dict for query pool generation. {'uniqueid':['database'. 'laboratory']}

        **localdata_er** A list for similarity join. [(['yong', 'jun', 'he', 'simon', 'fraser'],'uniqueid')]
        """
        with open(self.__localPath, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            data_raw = [row for row in reader]

        uniqueid_index = 0
        querylist_index = []
        matchlist_index = []
        try:
            header = data_raw.pop(0)
            uniqueid_index = header.index(self.__uniqueId)
            for q in self.__queryList:
                querylist_index.append(header.index(q))
            for m in self.__matchList:
                matchlist_index.append(header.index(m))
        except ValueError:
            print >> perr, "Can't find attributes"
            exit(0)

        localdata_query = {}
        localdata_er = []
        localdata_ids = set()
        stop_words = ['and', 'for', 'the', 'with', 'about']
        for row in data_raw:
            try:
                r_id = row[uniqueid_index]
            except IndexError:
                continue
            localdata_ids.add(r_id)

            tempbag = []
            for q in querylist_index:
                try:
                    tempbag.extend(wordset(row[q]))
                except IndexError:
                    continue
            bag = []
            for word in tempbag:
                if word not in stop_words and len(word) >= 3:
                    bag.append(word)
            localdata_query[r_id] = bag

            bag = []
            for m in matchlist_index:
                try:
                    bag.extend(wordset(row[m]))
                except IndexError:
                    continue
            localdata_er.append((bag, r_id))
        self.setlocalData(localdata_ids, localdata_query, localdata_er)

    def setLocalPath(self, localpath):
        self.__localPath = localpath

    def getLocalPath(self):
        return self.__localPath

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
