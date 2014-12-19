from Template import *

class Event:
    def __init__(self, values):
        self.id, self.name, self.account_id, self.has_sent = values

    def add(self, db):
        c = db.cursor()
        values = (self.name, self.account_id)
        c.execute('INSERT INTO account \
            (name, account_id), \
            VALUES (?, ?)', values)
        self.id = c.lastrowid
        db.commit()

    @staticmethod
    def has_enough_codes(event_id, account_id, num_recipients, code_info,  db):
        for entry in code_info:
            if entry['count'] < num_recipients:
                return False
        return len(Template.code_types(event_id, db)) == len(code_info)


        
    @staticmethod
    def has_sent(event_id, db):
        c = db.cursor()
        c.execute('\
            SELECT has_sent\
            FROM event\
            WHERE id = ?', (event_id,))
        result = c.fetchone()
        if result is None: return 0
        return result[0]

    @staticmethod
    def belongs_to(event_id, account_id, db):
        c = db.cursor()
        c.execute('\
            SELECT account_id\
            FROM event\
            WHERE id = ?', (event_id,))
        result = c.fetchone()
        return result[0] == account_id
        
    @staticmethod
    def create(name, account_id, db):
        values = (None, name, account_id, False)
        event = Event(values)
        event.add(db)
        return event

    def add(self, db):
        c = db.cursor()
        values = (self.name, self.account_id, self.has_sent)
        c.execute('INSERT INTO event \
            (name, account_id, has_sent) \
            VALUES (?, ?, ?)', values)
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
