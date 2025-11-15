from ..db import db

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password_hash = db.Column(db.String(100), nullable = False)
    
    info = db.relationship("UserInfo", back_populates = "user", uselist = False)
    