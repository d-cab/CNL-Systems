from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    passwordHash = db.Column(db.String(30), nullable=False)

    def setPasswordHash(self,password):
        self.passwordHash = generate_password_hash(password)

    def checkPasswordHash(self, password):
        return check_password_hash(self.passwordHash, password)

user = User(username="admin")
user.setPasswordHash("123")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        user.setPasswordHash(password)
        if user and user.checkPasswordHash(password):
            session['username'] = username
            return render_template("dashboard.html", username=username, password=password)
        else:
             return render_template("login.html", error="Incorrect credentials")

    else:
        return render_template("login.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)