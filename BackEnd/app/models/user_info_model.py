from ..db import db

class UserInfo(db.Model):
    __tablename__ ="users_info"
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True)
    username = db.Column(db.String(120))
    
    user = db.relationship("User", back_populates = "info")



