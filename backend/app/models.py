# models.py
from app import db, bcrypt

class User(db.Model):
    __tablename__ = "users"   # Safe table name
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "manager" or "analyst"

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")
    
    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)
