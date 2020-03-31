from flask import Flask, render_template, request, session, redirect, url_for
import pyrebase
from config import api_key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'covid_19'

config = {
    "apiKey": api_key,
    "authDomain": "verkefni5-49d08.firebaseapp.com",
    "databaseURL": "https://verkefni5-49d08.firebaseio.com",
    "projectId": "verkefni5-49d08",
    "storageBucket": "verkefni5-49d08.appspot.com",
    "messagingSenderId": "917292550423",
    "appId": "1:917292550423:web:cea8311171c957200acf52",
    "measurementId": "G-V0KWD32QZ6"
}

fb = pyrebase.initialize_app(config)
db = fb.database()


@app.route('/')
def index():
    db.child("user").push({"usr": "dsg", "pwd": "1234"})
    return render_template('index.html')


@app.route('/login', methods=['Get', 'Post'])
def login():
    login = False
    if request.method == 'POST':

        usr = request.form['user']
        pwd = request.form['psw']

        u = db.child('user').get().val()
        lst = list(u.items())
        for i in lst:
            if usr == i[1]['usr'] and pwd == i[1]['pwd']:
                login = True
                break

        if login:
            session['logged_in'] = usr
            return redirect("/topsecret")
        else:
            return render_template("nologin.html")
    else:
        return render_template("no_method.html")

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/doregister', methods=['GET', 'POST'])
def doregister():
    usernames = []
    if request.method == 'POST':

        usr = request.form['user']
        pwd = request.form['psw']

        u = db.child('user').get().val()
        lst = list(u.items())
        for i in lst:
            usernames.append(i[1]['usr'])

        if usr not in usernames:
            db.child('user').push({"usr": usr, "pwd": pwd})
            return render_template("registered.html")
        else:
            return render_template("userexists.html")
    else:
        render_template("no_method.html")


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return render_template("index.html")


@app.route("/topsecret")
def topsecret():
    if 'logged_in' in session:
        return render_template("topsecret.html")
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

#skrifum nýjan í grunn hnútur sem heitir notandi
# db.child("notandi").push({"notendanafn":"dsg", "lykilorð":1234})

# # förum í grunn og sækjum allar raðir ( öll gögn )
# u = db.child("notandi").get().val()
# lst = list(u.items())
