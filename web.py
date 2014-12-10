from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, send_file, Response, make_response, jsonify
from mongoaccess.MongoDAO import MongoDAO
from io import BytesIO
from werkzeug.security import generate_password_hash, \
     check_password_hash
import glob, os, time
import zipfile

heroku = False
MONGO_URL = 'mongodb://localhost:27017'
if heroku:
    MONGO_URL = 'mongodb://heroku_app32393789:piag5odkk3jg797r836g4u55t7@ds063180.mongolab.com:63180/heroku_app32393789'
    MONGO_URL = 'mongodb://giliusthunderhead:duckduckgoose@ds063140.mongolab.com:63140/timecapsule'

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('mainsite.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        mongo = MongoDAO(MONGO_URL)
        validPassword = mongo.checkUserInputs(username,password)
        if validPassword:
            if 'redirect' in request.cookies.keys() and request.cookies['redirect'] == 'files':
                resp = make_response(redirect('/files'))
                resp.set_cookie('username',username)
                return resp
            if 'redirect' in request.cookies.keys() and request.cookies['redirect'] == 'landing':
                resp = make_response(redirect('/landing'))
                resp.set_cookie('username',username)
                return resp
            return render_template('mainsite.html')
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route("/logout",methods=['GET'])
def logout():
    resp = make_response(render_template('logoutsuccess.html'))
    resp.set_cookie('username', expires=0)
    return resp  

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['Username']
        unhashedPassword = request.form['Password']
        email = request.form['Email']
        mongo = MongoDAO(MONGO_URL)
        if not mongo.userNameAvailable(username):
            return render_template('signupfailure.html')
        mongo.insertNewUser(email,username,unhashedPassword)
        if 'redirect' in request.cookies.keys() and request.cookies['redirect'] == 'files':
            resp = make_response(redirect('/files'))
            resp.set_cookie('username',username)
            return resp
        if 'redirect' in request.cookies.keys() and request.cookies['redirect'] == 'landing':
            resp = make_response(redirect('/landing'))
            resp.set_cookie('username',username)
            return resp
        return render_template('signupsuccess.html')
    return render_template('signup.html')

@app.route("/dlcap",methods=['GET','POST'])
def downloadFiles():
    if request.method == 'POST':
        mongo = MongoDAO(MONGO_URL)
        identifier = request.form['CapsuleName']
        password = request.form['CapsulePassword']
        result = mongo.getCapsuleByIdentifier(identifier,password)
        memory_file = BytesIO()
        if result != None:
            with zipfile.ZipFile(memory_file, 'w') as zf:
                files = result['files']
                for individualFile in files:
                    data = zipfile.ZipInfo(individualFile['fileName'])
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, individualFile['fileData'])
            memory_file.seek(0)
            return send_file(memory_file, attachment_filename='capsule.zip', as_attachment=True)
        else:
            return 'No such capsule with that identifier/password exists'
    return render_template('download.html')

@app.route("/dlcapuser",methods=['GET','POST'])
def downloadFilesUser():
    if request.method == 'POST':
        mongo = MongoDAO(MONGO_URL)
        identifier = request.form['identifier']
        username = request.form['username']
        result = mongo.getCapsuleByIdentifierAndUser(identifier,username)
        memory_file = BytesIO()
        if result != None:
            with zipfile.ZipFile(memory_file, 'w') as zf:
                files = result['files']
                for individualFile in files:
                    data = zipfile.ZipInfo(individualFile['fileName'])
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, individualFile['fileData'])
            memory_file.seek(0)
            return send_file(memory_file, attachment_filename='capsule.zip', as_attachment=True)
        else:
            return 'No such capsule with that identifier/password exists'
    return render_template('download.html')

@app.route("/dlcapuserJSON",methods=['GET'])
def downloadFilesUserJSON():
    if request.method == 'GET':
        mongo = MongoDAO(MONGO_URL)
        identifier = request.args.get('identifier')
        username = request.args.get('username')
        result = mongo.getCapsuleByIdentifierAndUser(identifier,username)
        memory_file = BytesIO()
        if result != None:
            with zipfile.ZipFile(memory_file, 'w') as zf:
                files = result['files']
                for individualFile in files:
                    data = zipfile.ZipInfo(individualFile['fileName'])
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, individualFile['fileData'])
            memory_file.seek(0)
            return send_file(memory_file, attachment_filename='capsule.zip', as_attachment=True)
        else:
            return 'No such capsule with that identifier/password exists'
    else:
        return 'This page was reached in error'

@app.route("/landing",methods=['GET','POST'])
def landing():
    if 'username' in request.cookies.keys():
        username = request.cookies['username']
        mongo = MongoDAO(MONGO_URL)
        capsuleNames = mongo.getAllCapsuleNamesForUser(username)
        return render_template('landing.html',my_list = capsuleNames, user_name = username)
    else:
        resp = make_response(redirect(url_for('login')))
        resp.set_cookie('redirect','landing')
        return resp

@app.route("/jsonexample",methods=['GET'])
def jsonExample():
    return render_template('jsonexample.html')

@app.route("/landingJSON",methods=['GET','POST'])
def landingJSON():
    if request.method == 'POST':
        if 'username' in request.form.keys():
            username = request.form['username']
            mongo = MongoDAO(MONGO_URL)
            capsuleNamesJSON = mongo.getAllCapsuleNamesAndLinksForUserJSON(username)
            print str(capsuleNamesJSON)
            return jsonify(capsuleNamesJSON)
    else:
        result = {'username':'idungotnosn'}
        return jsonify(result)

@app.route("/files",methods=['GET','POST'])
def handleFiles():
    if request.method == 'POST':
        if 'username' in request.cookies.keys():
            mongo = MongoDAO(MONGO_URL)
            identifier = request.form['CapsuleName']
            password = request.form['CapsulePassword']
            username = request.cookies['username']
            mongo.insertNewCapsule(identifier,password,request.files, username)
            return render_template('success.html')
        else:
            resp = make_response(redirect(url_for('login')))
            resp.set_cookie('redirect','files')
            return resp
    return render_template('files.html')

@app.route("/jsonexample")
def json():
    f = {'name':'Mike'}
    return jsonify(**f)

if __name__ == "__main__":
    app.run(debug=True)
