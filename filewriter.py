import json

class FileWriter:
    def __init__(self, filename):
        self.FILE = filename
    
    def writeToFile(self, json_data ):
        f = open(self.FILE, 'w')
        json.dump(json_data, f)
        f.close()
        return
    
    def readFromFile(self):
        f = open(self.FILE, 'r')
        data = json.load(f)
        f.close() 
        return data