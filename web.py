from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, send_file, Response, make_response
from mongoaccess.MongoDAO import MongoDAO
from io import BytesIO
from werkzeug.security import generate_password_hash, \
     check_password_hash
import glob, os, time
import zipfile

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
        validPassword = mongo.checkUserInputs(username,password)
        if validPassword:
            if 'redirect' in request.cookies.keys() and request.cookies['redirect'] == 'files':
                resp = make_response(redirect('/files'))
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
        mongo = MongoDAO('localhost',27017)
        if not mongo.userNameAvailable(username):
            return render_template('signupfailure.html')
        mongo.insertNewUser(email,username,unhashedPassword)
        if 'redirect' in request.cookies.keys() and request.cookies['redirect'] == 'files':
            resp = make_response(redirect('/files'))
            resp.set_cookie('username',username)
            return resp
        return render_template('signupsuccess.html')
    return render_template('signup.html')

@app.route("/dlcap",methods=['GET','POST'])
def downloadFiles():
    if request.method == 'POST':
        mongo = MongoDAO('localhost',27017)
        identifier = request.form['CapsuleName']
        password = request.form['CapsulePassword']
        result = mongo.getCapsuleByIdentifier(identifier,password)
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
        if 'username' in request.cookies.keys():
            mongo = MongoDAO('localhost',27017)
            identifier = request.form['CapsuleName']
            password = request.form['CapsulePassword']
            username = request.cookies['username']
            #print str(request.files)
            mongo.insertNewCapsule(identifier,password,request.files, username)
            return render_template('success.html')
        else:
            resp = make_response(redirect(url_for('login')))
            resp.set_cookie('redirect','files')
            return resp
    return render_template('files.html')

if __name__ == "__main__":
    app.run(debug=False)
