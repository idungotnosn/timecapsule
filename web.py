from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, send_file, Response
from mongoaccess.MongoDAO import MongoDAO
from io import BytesIO
from werkzeug.security import generate_password_hash, \
     check_password_hash
import glob, os, time
import zipfile
#import logging
#logging.basicConfig(filename='example.log',level=logging.ERROR)
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('mainsite.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        mongo = MongoDAO('localhost',27017)
        print mongo.checkUserInputs(username,password)
    return render_template('login.html')

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['Username']
        unhashedPassword = request.form['Password']
        email = request.form['Email']
        mongo = MongoDAO('localhost',27017)
        if not mongo.userNameAvailable(username):
            return render_template('signupfailure.html')
        mongo.insertNewUser(email,username,unhashedPassword)
        return render_template('signupsuccess.html')
    return render_template('signup.html')

@app.route("/dlcap",methods=['POST'])
def downloadFiles():
    if request.method == 'POST':
        mongo = MongoDAO('localhost',27017)
        identifier = request.form['CapsuleName']
        password = request.form['CapsulePassword']
        result = mongo.getCapsuleByIdentifier(identifier,password)
        files = result['files']
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            files = result['files']
            for individualFile in files:
                data = zipfile.ZipInfo(individualFile['fileName'])
                data.date_time = time.localtime(time.time())[:6]
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, individualFile['fileData'])
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='capsule.zip', as_attachment=True)
    return render_template('download.html')


@app.route("/files",methods=['GET','POST'])
def handleFiles():
    if request.method == 'POST':
        mongo = MongoDAO('localhost',27017)
        identifier = request.form['CapsuleName']
        password = request.form['CapsulePassword']
        mongo.insertNewCapsule(identifier,password,request.files);
        '''
        for fileName in request.files:
            print fileName
            currentFile = request.files[fileName]
            try:
                for line in currentFile:
                    print line
            finally:
                currentFile.close()'''
        return render_template('success.html')
    return render_template('files.html')

if __name__ == "__main__":
    app.run(debug=False)
