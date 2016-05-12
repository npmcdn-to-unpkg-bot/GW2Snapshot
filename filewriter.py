import json

FILE = 'writefile.txt'

def writeToFile( json_data ):
    f = open(FILE, 'w')
    json.dump(json_data, f)
    f.close()
    return

def readFromFile():
    f = open(FILE, 'r')
    data = json.load(f)
    f.close() 
    return data