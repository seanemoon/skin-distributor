import json

class Template:
    def __init__(self, values):
        self.id, self.event_id, self.sender, self.subject, \
            self.header, self.body, self.code_types = values
        if len(self.code_types) > 0:
            self.code_types = json.loads(self.code_types)

    @staticmethod
    def create(event_id, sender, subject, header, body, code_types, db):
        values = (None, event_id, sender, subject, header, body, code_types)
        template = Template(values)
        template.add(db)
        return template

    @staticmethod
    def fetch(event_id, account_id, db):
        c = db.cursor()
        c.execute('SELECT \
            T.id, T.event_id, T.sender, T.subject, T.header, T.body, T.code_types \
            FROM template AS T JOIN event AS E ON T.event_id = E.id \
            WHERE E.id = ?  \
            AND E.account_id = ?', (event_id, account_id))
        result = c.fetchone()
        if result is None: return None
        else: return Template(result)

    def add(self, db):
        c = db.cursor()
        values = (self.event_id, self.sender, self.subject, \
            self.header, self.body, json.dumps(self.code_types))
        c.execute('INSERT INTO template \
            (event_id, sender, subject, header, body, code_types) \
            VALUES (?, ?, ?, ?, ?, ?)', values)
        self.id = c.lastrowid
        db.commit()

    def update(self, sender, subject, header, body, code_types, db):
        c = db.cursor()
        self.sender = sender
        self.subject = subject
        self.header = header
        self.body = body
        self.code_types = code_types

        c.execute('UPDATE template \
          SET sender = ?, subject = ?, header = ?, body = ?, code_types = ? \
          WHERE id = ?', (self.sender, self.subject, self.header,  \
          self.body, self.code_types, self.id))
        db.commit()
