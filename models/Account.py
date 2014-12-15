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
    # Used for creating a new account from a form.
    def __init__(self, values):
        self.id, self.email, self.salt, self.pass_hash = values

    @staticmethod
    def login(email, password, db):
      account = Account.fetch(email, db)
      if account and salted_hash(password, account.salt) == account.pass_hash:
          return account
      else:
          return None

    @staticmethod
    def create(email, password, db):
        salt = generate_random_salt()
        pass_hash = salted_hash(password, salt)
        values = (None, email, salt, pass_hash)
        account = Account(values)
        account.add(db)
        return account

    @staticmethod
    def fetch(email, db):
        c = db.cursor()
        c.execute('SELECT * FROM account \
            WHERE email=?', (email,))
        result = c.fetchone()
        if result is None:
            return None
        return Account(result)

    def is_valid(self):
        return is_valid_email(email) and is_valid_password(password)

    def add(self, db):
        c = db.cursor()
        values = (self.email, self.salt, self.pass_hash)
        c.execute('INSERT INTO account \
            (email, salt, pass_hash) \
            VALUES (?, ?, ?)', values)
        self.id = c.lastrowid
        db.commit()

