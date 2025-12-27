from flask import request
from app.extensions import db
from app.models import User

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