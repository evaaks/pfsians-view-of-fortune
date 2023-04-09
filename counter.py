import re


def counter(fname):
    count = 0
    with open(fname, 'r') as f:
        for line in f:
            count += len(re.findall('XYZYX', line))
    return count
