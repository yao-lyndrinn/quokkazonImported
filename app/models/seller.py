from flask import current_app as app

class Seller:
    def __init__(self, sid):
        self.sid = sid

    @staticmethod
    def get(sid):
        rows = app.db.execute('''
        SELECT *
        FROM Seller
        WHERE sid = :sid
        ''',
        sid=sid)
        return Seller(*(rows[0])) if rows else None
        
    @staticmethod
    def is_seller(user):
        if hasattr(user,"id"):
            return Seller.get(user.id) != None
        return False
