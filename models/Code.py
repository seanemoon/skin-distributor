class Code:
    def __init__(self, values): pass

    @staticmethod
    def fetch_info(event_id, account_id, db):
        c = db.cursor()
        c.execute("\
            SELECT C.name, COUNT(C.name)\
            FROM recipient as R\
            JOIN code as C ON R.id = C.recipient_id\
            JOIN event as E ON E.id = R.event_id\
            WHERE E.id = ? and E.account_id = ? \
            GROUP BY C.name", (event_id, account_id))
        result = c.fetchall()
        print "Event id: %s\n Account id: %s" % (event_id, account_id)
        if result is None: return None
        parsed = [{'name': row[0], 'count': row[1]} for row in result]
        print "INFO:"
        for e in parsed:
            print e
        return parsed
    
    @staticmethod
    def clear(event_id, account_id, db):
        c = db.cursor()
        c.execute('\
            DELETE FROM code\
            WHERE code.id in (\
                SELECT C.id\
                FROM code AS C\
                JOIN recipient AS R ON R.id = C.recipient_id\
                JOIN event AS E ON E.id = R.event_id\
                WHERE E.id = ? AND E.account_id = ?\
            )', (event_id, account_id))
        db.commit()





