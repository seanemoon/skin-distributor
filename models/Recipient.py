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
    def clear(event_id, account_id, db):
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
