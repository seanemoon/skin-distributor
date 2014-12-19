from Event import *

class Code:
    def __init__(self, values):
        self.id = values[0]
        self.event_id = values[1]
        self.name = values[2]
        self.code = values[3]

    @staticmethod
    def fetch(event_id, db):
        c = db.cursor()
        c.execute('\
            SELECT * FROM code\
            WHERE event_id = ?', (event_id,))
        result = c.fetchall()
        if result is None: return None
        parsed = [Code(row) for row in result]
        grouped = {}
        for entry in parsed:
            print entry
            group = grouped.get(entry.name, [])
            group.append(entry)
            grouped[entry.name] = group
        return grouped

    @staticmethod
    def fetch_info(event_id, account_id, db):
        c = db.cursor()
        c.execute("\
            SELECT C.name, COUNT(C.name)\
            FROM code as C\
            JOIN event as E ON E.id = C.event_id\
            WHERE E.id = ? and E.account_id = ?\
            GROUP BY C.name", (event_id, account_id))
        result = c.fetchall()
        if result is None: return None
        parsed = [{'name': row[0], 'count': row[1]} for row in result]
        return parsed

    @staticmethod
    def upload(event_id, account_id, codes, db):
        if Event.belongs_to(event_id, account_id, db):
            c = db.cursor()
            for code in codes:
                c.execute('\
                    INSERT INTO code\
                    (event_id, name, code)\
                    VALUES (?, ?, ?)', (event_id, "TEST", code))
            db.commit()

    @staticmethod
    def fetch_assigned_info(event_id, account_id, db):
        c = db.cursor()
        c.execute("\
            SELECT C.name, COUNT(C.name)\
            FROM recipient as R\
            JOIN code_assignment as A on A.recipient_id = R.id\
            JOIN code as C ON C.id = A.code_id\
            JOIN event as E ON E.id = R.event_id\
            WHERE E.id = ? and E.account_id = ? \
            GROUP BY C.name", (event_id, account_id))
        result = c.fetchall()
        if result is None: return None
        parsed = [{'name': row[0], 'count': row[1]} for row in result]
        return parsed
    
    @staticmethod
    def clear(event_id, account_id, db):
        c = db.cursor()
        c.execute('\
            DELETE FROM code\
            WHERE code.id in (\
                SELECT C.id\
                FROM code AS C\
                JOIN event AS E ON E.id = C.event_id\
                WHERE E.id = ? AND E.account_id = ?\
            )', (event_id, account_id))
        db.commit()
