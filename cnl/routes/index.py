from flask import Blueprint, render_template, request, redirect, url_for, session
from cnl.models import User
from cnl.extensions import db
from cnl.utils import registerEmail, registerPassword

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def home():
    return render_template("index.html")

@index_bp.route("/about")
def about():
    return render_template("about.html")

@index_bp.route("/contact")
def contact():
    return render_template("contact.html")

@index_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.checkPasswordHash(password):
            session['email'] = email
            return render_template("dashboard.html", email=email, password=password)
        else:
            return render_template("login.html", error="Incorrect credentials")
    return render_template("login.html")

@index_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        errors = []

        # Email check
        email, email_error = registerEmail()
        if email_error:
            errors.append(email_error)

        # Password check
        password, pw_error = registerPassword()
        if pw_error:
            errors.append(pw_error)

        if errors:
            return render_template("register.html", errors=errors)

        # ✅ Only create user after passing all checks
        newUser = User(email=email)
        newUser.setPasswordHash(password)
        db.session.add(newUser)
        db.session.commit()

        return redirect(url_for("index.login"))

    return render_template("register.html")
  