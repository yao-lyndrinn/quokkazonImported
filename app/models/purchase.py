from flask import current_app as app

class Purchase:
    def __init__(self, uid, sid, pid, order_id, time_purchased, quantity, date_fulfilled):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.order_id = order_id
        self.time_purchased = time_purchased
        self.quantity = quantity
        self.date_fulfilled = date_fulfilled

    @staticmethod
    def get(uid,pid,sid,order_id):
        rows = app.db.execute('''
        SELECT uid, sid, pid, order_id, time_purchased, quantity, date_fulfilled
        FROM Purchases
        WHERE uid = :uid AND pid = :pid AND sid =:sid AND order_id = :order_id
        ''',
        uid=uid, pid=pid, sid =sid, order_id = order_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE uid = :uid
        AND time_purchased >= :since
        ORDER BY time_purchased DESC
        LIMIT 10
        ''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    def get_top_ten():
        rows = app.db.execute('''
        SELECT pid, COUNT(*)
        FROM Purchases
        GROUP BY pid
        ORDER BY COUNT(*) DESC
        LIMIT 10''')
        top_purchases = []
        for row in rows:
            pid, count = row
            top_purchases.append(pid)
        return top_purchases
