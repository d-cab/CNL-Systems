from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passwordHash = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True)
    
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False, nullable=False)

    def setPasswordHash(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPasswordHash(self, password):
        return check_password_hash(self.passwordHash, password)


# routes

@app.route("/")
def home():
    return render_template("dilligence.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["POST", "GET"])
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

@app.route("/register", methods=["GET", "POST"])
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

        return redirect(url_for("login"))

    return render_template("register.html")
  

def registerPassword():
    password = request.form.get("password")
    if not password or len(password) < 8:
        return None, "Password must be at least 8 characters long."
    return password, None


def registerEmail():
    email = request.form.get("email")
    if not email:
        return None, "Email is required."
    if db.session.query(User).filter_by(email=email).first():
        return None, "This email is already in use."
    return email, None


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Add a default admin user if not exists
        if not User.query.filter_by(email="diegocabral209@gmail.com").first():
            user = User(email="diegocabral209@gmail.com")
            user.setPasswordHash("123")
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)
