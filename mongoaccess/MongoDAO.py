from pymongo import MongoClient
from bson.binary import Binary
import pickle

class MongoDAO:
    def __init__(self, host, port):
        self.client = MongoClient(host,port)
        self.db = self.client['timecapsule']
        self.capsules = self.db['Timecapsules']

    def getCapsuleByIdentifier(self,identifier):
        returnedCapsules = self.capsules.find({"identifier":identifier})
        for capsule in self.capsules.find({"identifier":identifier}):
            return capsule

    def insertNewCapsule(self, identifier, password, files):
        #print 'identifier was '+identifier
        #print 'password was '+password
        #print 'files were '+str(files)
        JSON = {}
        JSON['identifier'] = identifier
        JSON['password'] = password
        JSON['files'] = []
        #db.Timecapsules.insert({identifier:"identifier1234",password:"password1234",files:[{fileName:"stuff.txt",fileData:"DFOISDSODFIJ"},{fileName:"stuff2.txt",fileData:"FDSOIKFSFDDDFGG"}]})
        for fileName in files:
            currentFile = files[fileName]
            fileDict = {}
            try:
                theBytes = currentFile.read()
                #print str(currentFile)
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

