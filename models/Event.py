class Event:
    def __init__(self, values):
        self.id, self.name, self.account_id = values

    def add(self, db):
        c = db.cursor()
        values = (self.name, self.account_id)
        c.execute('INSERT INTO account \
            (name, account_id), \
            VALUES (?, ?)', values)
        self.id = c.lastrowid
        db.commit()

    @staticmethod
    def retrieve(user_id, db):
        c = db.cursor()
        c.execute('SELECT FROM event \
            WHERE id = ?', user_id)
        return [Event(row) for row in c.fetchall()]

    def delete(self, db):
        c = db.cursor()
        # Might need to make self.id a tuple (self.id,))
        c.execute('DELETE FROM account \
            WHERE id = ?' , self.id)
