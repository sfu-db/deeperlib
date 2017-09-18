import copy
import re


def alphnum(s):
    """
    Filter letters and numbers from raw string

    :param s: a raw string of different kinds of characters
    :return: a new string of letters and numbers
    """
    sep = re.compile(r"[\W]")
    items = sep.split(s)
    return " ".join([item for item in items if item.strip() != ""])


def wordset(s, lower_case=True, alphanum_only=True):
    """
    Split raw string into a list of words

    :param s: a raw string of different kinds of characters
    :param lower_case: a boolean value that denotes whether convert the raw string to lower case
    :param alphanum_only: a boolean value that denotes whether filter letters and numbers from raw string
    :return: a list of words
    """
    if lower_case:
        s = s.lower()
    if alphanum_only:
        s = alphnum(s)
    return s.split()


def getElement(node_list, data):
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
                        result += str(getElement(node_list[i + 1:], ele)) + ' '
                return result.lstrip()
            else:
                temp = temp[node]
        result = temp
    except (KeyError, TypeError, IndexError):
        pass
    return result
