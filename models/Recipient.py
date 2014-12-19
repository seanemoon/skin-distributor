from Event import *
from Code import *

class Recipient:
    def __init__(self, values):
        self.id = values[0]
        self.event_id = values[1]
        self.email = values[2]
        self.success = values[3]
        self.should_send = values[4]
        self.time_sent = values[5]

    @staticmethod
    def num_recipients(event_id, db):
        c = db.cursor()
        c.execute("SELECT COUNT(*) \
            FROM recipient \
            WHERE event_id = ?", (event_id,))
        result = c.fetchone()
        if result == 0: return None
        return result[0]

    @staticmethod
    def upload(event_id, recipients, db):
        c = db.cursor()
        for recipient in recipients:
            c.execute('\
                INSERT INTO recipient\
                (event_id, email)\
                VALUES (?, ?)', (event_id, recipient))
        db.commit() 

    @staticmethod
    def fetch(event_id, db):
        c = db.cursor()
        c.execute('\
            SELECT * from recipient\
            WHERE event_id = ?', (event_id,))
        result = c.fetchall()
        if result is None: return None
        parsed = [Recipient(row) for row in result]
        return parsed
        
    @staticmethod
    def send(event_id, db):
        def generate_assignments():
            codes = Code.fetch(event_id, db)
            recipients = Recipient.fetch(event_id, db)
            assignments = []
            for i, r in enumerate(recipients):
                for code_type in codes:
                    if i > len(codes[code_type]): continue
                    code_id = codes[code_type][i].id
                    assignments.append({'code_id': code_id, 'recipient_id': r.id})
            return assignments

        def insert_assignments():
            assignments = generate_assignments()
            c = db.cursor()
            for a in assignments:
                c.execute('\
                    INSERT INTO code_assignment (recipient_id, code_id)\
                    VALUES (?, ?)', (a['recipient_id'], a['code_id']))
        insert_assignments()

        c = db.cursor()
        c.execute('\
            UPDATE event\
            SET has_sent = 1\
            WHERE id = ?', (event_id,))
        c.execute('\
            UPDATE recipient\
            SET should_send = 1\
            WHERE event_id = ?', (event_id,))
        db.commit()

    @staticmethod
    def get_status(event_id, db):
        c = db.cursor()
        c.execute('\
            SELECT R.email, C.name, C.code, R.time_sent, R.success\
            FROM recipient as R\
            JOIN code_assignment as A on R.id = A.recipient_id\
            JOIN code as C on C.id = A.code_id\
            WHERE R.event_id = ?\
            ORDER BY C.name', (event_id,))
        result = c.fetchall()
        parsed = []
        if result is None: return None
        for row in result:
            entry = {
                'email': row[0],
                'code_name': row[1],
                'code_value': row[2],
                'time_sent': row[3],
                'success': row[4]
            }
            parsed.append(entry)
        return parsed

    @staticmethod
    def clear(event_id, db):
        c = db.cursor()
        c.execute('\
          DELETE FROM recipient\
          WHERE event_id = ?', (event_id,))
        db.commit()
