from flask import current_app as app

class Messages:
    def __init__(self,sender,sname,receiver,rname,date_time,msg):
        self.sender = sender
        self.sname = sname 
        self.receiver = receiver,
        self.rname = rname
        self.date_time = date_time
        self.msg = msg 
        
    @staticmethod
    def get_by_sender_receiver(sender, receiver):
        # sorted in chronological order 
        rows = app.db.execute('''
        SELECT s.id, (s.firstname || ' ' || s.lastname), r.id, (r.firstname || ' ' || r.lastname), m.msg 
        FROM Users as s, Users as r, Messages as m  
        WHERE s.id = :sender 
        AND r.id = :receiver
        AND m.sender = :sender
        AND m.receiver = :receiver
        ORDER BY f.date_time 
        ''',
        sender=sender,
        receiver=receiver)
        return [Messages(*row) for row in rows]

    @staticmethod 
    def get_by_sender(sender):
        rows = app.db.execute('''
        SELECT s.id, (s.firstname || ' ' || s.lastname), r.id, (r.firstname || ' ' || r.lastname), m.msg 
        FROM Users as s, Messages as m  
        WHERE s.id = :sender 
        AND m.sender = :sender
        ORDER BY f.date_time 
        ''',
        sender=sender)
        return [Messages(*row) for row in rows]