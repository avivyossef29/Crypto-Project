from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import ssl
import threading

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    bak_accnount = db.Column(db.String(250), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    if (request.method == "POST"):
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"),
                     bank_account=request.form.get("bank_account"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user and user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    if current_user.is_authenticated:
        return f"Logged in as {current_user.username} with ID {current_user.id} and bank account {current_user.bank_account}"
    return "You are not logged in"

def run_http():
    app.run(host="0.0.0.0", port=80)

def run_https():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile='/app/cert.pem', keyfile='/app/key.pem')
    app.run(host="0.0.0.0", port=443, ssl_context=context)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # Start HTTP and HTTPS servers in separate threads
    threading.Thread(target=run_http).start()
    threading.Thread(target=run_https).start()
