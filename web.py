from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, send_file
from mongoaccess.MongoDAO import MongoDAO
from io import BytesIO
#import logging
#logging.basicConfig(filename='example.log',level=logging.ERROR)
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('mainsite.html')

@app.route("/getcaps",methods=['GET','POST'])
def downloadFiles():
    if request.method == 'POST':
        mongo = MongoDAO('localhost',27017)
        identifier = request.form['CapsuleName']
        password = request.form['CapsulePassword']
        result = mongo.getCapsuleByIdentifier(identifier)
        #print str(result)
        files = result['files']
        bytes = files[0]['fileData']
        return send_file(BytesIO(bytes), attachment_filename=files[0]['fileName'], as_attachment=True)
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
