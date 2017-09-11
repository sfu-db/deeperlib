import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re


def alphnum(s):
    """
    fdsaffafsdafa
    :param s:
    :return: fsdafsafsaf
    """
    sep = re.compile(r"[\W]")
    items = sep.split(s)
    return " ".join([item for item in items if item.strip() != ""])


def wordset(s, lower_case=True, alphanum_only=True):
    if lower_case:
        s = s.lower()
    if alphanum_only:
        s = alphnum(s)
    return s.split()
