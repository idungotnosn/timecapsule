from pymongo import MongoClient
from bson.binary import Binary
import pickle

class MongoDAO:
    def __init__(self, host, port):
        self.client = MongoClient(host,port)
        self.db = self.client['timecapsule']
        self.capsules = self.db['Timecapsules']

    def getCapsuleByIdentifier(self,identifier, password):
        returnedCapsules = self.capsules.find({"identifier":identifier,"password":password})
        for capsule in returnedCapsules:
            return capsule
        return None

    def insertNewCapsule(self, identifier, password, files):
        JSON = {}
        JSON['identifier'] = identifier
        JSON['password'] = password
        JSON['files'] = []
        for fileName in files:
            currentFile = files[fileName]
            fileDict = {}
            try:
                theBytes = currentFile.read()
                fileDict['fileName'] = currentFile.filename
                fileDict['fileData'] = Binary(theBytes)
                JSON['files'].append(fileDict)
            finally:
                currentFile.close()
        #print JSON
        self.capsules.insert(JSON)
        
if __name__ == "__main__":
    mongo = MongoDAO("localhost",27017)
    print mongo.getCapsuleByIdentifier('8325255171')


        #db.Timecapsules.insert({identifier:"identifier1234",password:"password1234",files:[{fileName:"stuff.txt",fileData:"DFOISDSODFIJ"},{fileName:"stuff2.txt",fileData:"FDSOIKFSFDDDFGG"}]})

