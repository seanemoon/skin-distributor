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
    def create(name, account_id, db):
        values = (None, name, account_id)
        event = Event(values)
        event.add(db)
        return event

    def add(self, db):
        c = db.cursor()
        values = (self.name, self.account_id)
        c.execute('INSERT INTO event \
            (name, account_id) \
            VALUES (?, ?)', values)
        self.id = c.lastrowid
        db.commit()

    @staticmethod
    def get_events_for(account_id, db):
        c = db.cursor()
        c.execute('SELECT * FROM event \
            WHERE account_id = ?', (account_id,))
        return [Event(row) for row in c.fetchall()]

    @staticmethod
    def fetch(account_id, event_id, db):
        c = db.cursor()
        c.execute('SELECT * from event \
            WHERE account_id = ? AND id = ?', (account_id, event_id))
        result = c.fetchone()
        if result is None:
            return result
        else:
            return Event(result)

    @staticmethod
    def delete(id, db):
        c = db.cursor()
        c.execute('DELETE FROM event \
            WHERE id = ?' , (id,))
        db.commit()
