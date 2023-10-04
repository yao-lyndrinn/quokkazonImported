from flask import current_app as app

class CartItem:
    def __init__(self, uid, sid, pid, quantity, saved_for_later):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.saved_for_later = saved_for_later

    @staticmethod
    def get(uid, sid, pid):
        rows = app.db.execute('''
SELECT *
FROM Cart
WHERE uid = :uid AND sid = :sid AND pid = :pid
''',
                              uid=uid,
                              sid = sid,
                              pid = pid)
        return CartItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT *
FROM Cart
WHERE uid = :uid
''', uid = uid)
        return [CartItem(*row) for row in rows]
    
    @staticmethod
    def add_item(uid, sid, pid, quantity, saved_for_later):
        rows = app.db.execute("""
        INSERT INTO CART(uid, sid, pid, quantity, saved_for_later)
        VALUES(:uid, :sid, :pid, :quantity, :saved_for_later)
        """,
        uid=uid,
        sid = sid,
        pid = pid,
        quantity = 1,
        saved_for_later = 0)
        return CartItem.get(uid, sid, pid)

