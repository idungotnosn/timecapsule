from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('mainsite.html')

if __name__ == "__main__":
    app.run()
