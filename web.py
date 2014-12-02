from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('mainsite.html')

@app.route("/files",methods=['GET','POST'])
def handleFiles():
    if request.method == 'GET':
        print 'Method was GET'
    if request.method == 'POST':
        print 'Method was POST'
        print 'There were '+str(len(request.files))+' files'
        for fileName in request.files:
            print fileName
            currentFile = request.files[fileName]
            try:
                for line in currentFile:
                    print line
            finally:
                currentFile.close()
        return render_template('success.html')
    return render_template('files.html')

if __name__ == "__main__":
    app.run()
