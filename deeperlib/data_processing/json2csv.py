import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import random
import codecs
import csv
import copy


class Json2csv:
    """
    Convert data in json format to csv.
    """

    def __init__(self, jsondata, csv_path):
        self.__header = []
        self.__jsondata = jsondata
        self.__getHeader(jsondata[random.randint(0, len(jsondata) - 1)])

        with open(csv_path, "wb") as csvfile:
            csvfile = file(csv_path, 'wb')
            csvfile.write(codecs.BOM_UTF8)
            writer = csv.writer(csvfile)
            # write header
            writer.writerow(self.__header)
            # write row
            for row in self.__jsondata:
                temprow = []
                for h in self.__header:
                    temprow.append(self.__getElement(h.split('.'), row))
                writer.writerow(temprow)

    def __getHeader(self, row, parentNode=''):
        """
        Get header by iteration and define them in special way for the next getElement method.

        :param row: One of jsondata's rows
        :param parentNode: prefix
        """
        if not isinstance(row, list):
            for q, v in row.iteritems():
                if isinstance(v, dict):
                    self.__getHeader(v, parentNode + str(q) + '.')
                elif isinstance(v, list):
                    self.__getHeader(v, parentNode + str(q) + '.*.')
                else:
                    self.__header.append(parentNode + str(q))
        else:
            if len(row) > 0 and isinstance(row[0], dict):
                self.__getHeader(row[0], parentNode)
            else:
                self.__header.append(parentNode[:-1])

    def __getElement(self, node_list, data):
        """
        Get the specified element according to the node path provided by users.

        :param node_list: node path
        :param data: data in dictionary
        :return: specified element
        """
        temp = copy.deepcopy(data)
        result = ''
        try:
            for i, node in enumerate(node_list):
                if node.isdigit():
                    temp = temp[int(node)]
                elif node == '*':
                    if i == len(node_list) - 1:
                        for ele in temp:
                            result += str(ele) + ' '
                    else:
                        for ele in temp:
                            result += str(self.__getElement(node_list[i + 1:], ele)) + ' '
                    return result.lstrip()
                else:
                    temp = temp[node]
            result = temp
        except (KeyError, TypeError, IndexError):
            pass
        return result
