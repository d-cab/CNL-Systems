from flask import Flask, render_template, request

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "123"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            return render_template("dashboard.html", username=username, password=password)
        else:
            return render_template("login.html", error="Incorrect credentials")

    else:
        return render_template("login.html")

# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)