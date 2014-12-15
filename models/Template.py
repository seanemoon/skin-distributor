class Template:
    def __init__(self, values):
        self.id, self.event_id, self.sender, self.subject, \
            self.header, self.body, self.code_types = values

    @staticmethod
    def create(event_id, sender, subject, header, body, code_types, db):
        values = (None, event_id, sender, subject, header, body, code_types)
        template = Template(values)
        template.add(db)
        return template

    def add(self, db):
        c = db.cursor()
        values = (self.event_id, self.sender, self.subject, \
            self.header, self.body, self.code_types)
        c.execute('INSERT INTO template \
            (event_id, sender, subject, header, body, code_types) \
            VALUES (?, ?, ?, ?, ?, ?)', values)
        self.id = c.lastrowid
        db.commit()

