from flask import current_app as app
import datetime

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
        ''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE sid = :sid
        ORDER BY time_purchased DESC
        ''',
                              sid=sid)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def fulfill(uid, sid, pid, order_id, date_fulfilled):
        try:
            rows = app.db.execute("""
            UPDATE Purchases
            SET date_fulfilled=:date_fulfilled
            WHERE uid=:uid AND sid=:sid AND pid=:pid AND order_id=:order_id
            """,
                                  uid=uid,
                                  sid=sid,
                                  pid=pid,
                                  order_id=order_id,
                                  date_fulfilled=date_fulfilled
                                )
            print("YESSS")
            return date_fulfilled
        except Exception as e:
            print(str(e))
