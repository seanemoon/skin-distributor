from Event import *

class Recipient:
    def __init__(self, values): pass

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
    def upload(event_id, account_id, recipients, db):
        if Event.belongs_to(event_id, account_id, db):
            c = db.cursor()
            for recipient in recipients:
                c.execute('\
                    INSERT INTO recipient\
                    (event_id, email)\
                    VALUES (?, ?)', (event_id, recipient))
            db.commit() 

    @staticmethod
    def clear(event_id, account_id, db):
        print "Clearing..."
        c = db.cursor()
        c.execute('\
          DELETE FROM recipient\
          WHERE recipient.id IN (\
              SELECT R.id\
              FROM recipient AS R\
              JOIN event AS E ON E.id = R.event_id\
              WHERE E.id = ? AND E.account_id = ?\
          )', (event_id, account_id))
        db.commit()
