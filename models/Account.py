import hashlib, uuid, re

def generate_random_salt():
    return uuid.uuid4().hex

def salted_hash(value, salt):
    return hashlib.sha512(value + salt).hexdigest()

def is_valid_email(email):
    # RE taken from http://www.regular-expressions.info/email.html
    valid_email = re.compile("\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b")
    return valid_email.match(self.email) is not None

def is_valid_password(password):
    return len(password) >= 6 and len(password) <= 360

class Account:
    def __init__(self, email, password):
        self.email = email;
        self.salt = generate_random_salt()
        self.pass_hash = salted_hash(password, self.salt)

    def is_valid(self):
        return is_valid_email(email) and is_valid_password(password)

    def add(self, db):
        c = db.cursor()
        values = (self.email, self.salt, self.pass_hash)
        c.execute('INSERT INTO account \
            (email, salt, pass_hash) \
            VALUES (?, ?, ?)', values)
        db.commit()
