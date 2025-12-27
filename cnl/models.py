from werkzeug.security import generate_password_hash, check_password_hash
from cnl.extensions import db

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
