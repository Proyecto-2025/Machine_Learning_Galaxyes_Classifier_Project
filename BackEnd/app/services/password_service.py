from werkzeug.security import generate_password_hash, check_password_hash

class PasswordService:
    @staticmethod
    
    def hash_password(password: str):
        return generate_password_hash(password)
    
    def verify_password(password: str, password_hash: str):
        return check_password_hash(password_hash, password)
    
    def strong_pass(password: str):
        
        if len(password) < 8:
            return False
        if not any(c.islower()for c in password):
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True
        