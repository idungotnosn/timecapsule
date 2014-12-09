from pymongo import MongoClient
from bson.binary import Binary
from werkzeug.security import generate_password_hash, \
     check_password_hash
import pickle

class MongoDAO:
    def __init__(self, host, port):
        self.client = MongoClient(host,port)
        self.db = self.client['timecapsule']
        self.capsules = self.db['Timecapsules']
        self.users = self.db['users']

    def getCapsuleByIdentifier(self,identifier, password):
        returnedCapsules = self.capsules.find({"identifier":identifier,"password":password})
        for capsule in returnedCapsules:
            return capsule
        return None

    def getAllCapsuleNamesForUser(self, username):
        JSON = {}
        JSON['username'] = username
        userCapsules = self.capsules.find({"username":username})
        str(userCapsules)
        result = []
        for capsule in userCapsules:
            result.append(capsule['identifier'])
        return result

    def insertNewCapsule(self, identifier, password, files, username):
        JSON = {}
        JSON['username'] = username
        JSON['identifier'] = identifier
        JSON['password'] = password
        JSON['files'] = []
        fileList = files.getlist('filesToUpload[]')
        print str(fileList)
        for currentFile in fileList:
            print 'File was '+str(currentFile)
            fileDict = {}
            try:
                theBytes = currentFile.read()
                fileDict['fileName'] = currentFile.filename
                fileDict['fileData'] = Binary(theBytes)
                JSON['files'].append(fileDict)
            finally:
                currentFile.close()
        self.capsules.insert(JSON)

    def insertNewUser(self, email, username, password):
        JSON = {}
        JSON['username'] = username
        JSON['email'] = email
        JSON['password'] = generate_password_hash(password)
        self.users.insert(JSON)

    def userNameAvailable(self, username):
        users = self.users.find({"username":username})
        for user in users:
            return False
        return True

    def checkUserInputs(self, username, unhashedPassword):
        users = self.users.find({"username":username})
        foundUser = None
        for user in users:
            foundUser = user
        if foundUser != None:
            return check_password_hash(foundUser['password'],unhashedPassword)
        else:
            return False
        
        
if __name__ == "__main__":
    mongo = MongoDAO("localhost",27017)
    print mongo.getCapsuleByIdentifier('8325255171')


        #db.Timecapsules.insert({identifier:"identifier1234",password:"password1234",files:[{fileName:"stuff.txt",fileData:"DFOISDSODFIJ"},{fileName:"stuff2.txt",fileData:"FDSOIKFSFDDDFGG"}]})

