from flask import current_app as app

class CartItem:
    def __init__(self, uid, sid, pid, quantity, price, saved_for_later):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.price = price
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
SELECT uid, Cart.sid, Cart.pid, Cart.quantity, price, saved_for_later
FROM Cart, Inventory
WHERE uid = :uid AND Cart.sid = Inventory.sid AND Cart.pid = Inventory.pid
''', uid = uid)
        return [CartItem(*row) for row in rows]
    
    @staticmethod
    def get_total_price(uid):
        rows = app.db.execute("""
        WITH C(total) AS
            (SELECT Cart.quantity * price FROM Cart, Inventory
            WHERE uid = :uid AND Cart.sid = Inventory.sid AND Cart.pid = Inventory.pid)
        SELECT SUM(total)
        FROM C
        """,
        uid=uid)
        return float(rows[0][0]) if rows and rows[0][0] is not None else 0.0
    
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
        saved_for_later = '0')
        return
    
    @staticmethod
    def remove_item(uid, sid, pid):
        rows = app.db.execute("""
        DELETE FROM CART
        WHERE uid = :uid AND sid = :sid AND pid = :pid
        """,
        uid=uid,
        sid=sid,
        pid=pid)
        return
    
    @staticmethod
    def update_quantity(uid, sid, pid, quantity):
        rows = app.db.execute("""
        UPDATE CART
        SET quantity = :quantity
        WHERE uid = :uid AND sid = :sid AND pid = :pid
        """,
        uid=uid,
        sid=sid,
        pid=pid,
        quantity=quantity)
        return

