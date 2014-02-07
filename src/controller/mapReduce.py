import cgitb; cgitb.enable()
import re
import collections

def mapper (fic):
    ''' Do the mapper of text given in parameter.
    :param fic: text to map reduce.
    :returns: a dictionnary of [word=>1]. example of use: data["lol"] = 1
    '''
    data = collections.defaultdict(list)
    with open("./datasettxt/forbiddenWords.txt") as f:
        lines = f.readlines()
    for line in lines :
        listWordForbidden = line.split(' ')
    line = re.sub(r'[^a-zA-Z\s0-1]', "", fic)
    line = line.strip()
    words = line.split()
    for word in words:
        if len(word) > 3 and word not in listWordForbidden :
            word = word.lower()
            data[word].append(1)
    return data

def reducer (strReducer):
    ''' Do the reducer of dictionnary given in parameter
    :param strReducer: a dictionnary of [word=>1]. example of use: data["lol"] = 1
    :returns: a dictionnary of [word=>count]. example of use: data["lol"] = 42
    '''
    data = collections.defaultdict(list)
    for key, value in strReducer.items():
        nbtotal = 0
        for count in value:
            nbtotal += count 
        data[key] = nbtotal

    return data

