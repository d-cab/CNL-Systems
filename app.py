from flask import Flask, render_template, request, session
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
    passwordHash = db.Column(db.String(200), nullable=False)  # lengthened

    def setPasswordHash(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPasswordHash(self, password):
        return check_password_hash(self.passwordHash, password)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.checkPasswordHash(password):
            session['username'] = username
            return render_template("dashboard.html", username=username, password=password)
        else:
            return render_template("login.html", error="Incorrect credentials")
    return render_template("login.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Add a default admin user if not exists
        if not User.query.filter_by(username="admin").first():
            user = User(username="admin")
            user.setPasswordHash("123")
            db.session.add(user)
            db.session.commit()
            print("Admin user created: username='admin', password='123'")
    app.run(debug=True)
