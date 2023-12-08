from flask import current_app as app
import datetime

class Purchase:
    def __init__(self, uid, sid, pid, order_id, time_purchased, quantity, price, date_fulfilled):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.order_id = order_id
        self.time_purchased = time_purchased
        self.quantity = quantity
        self.price = price
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
        LIMIT 8''')
        top_purchases = []
        for row in rows:
            pid, count = row
            top_purchases.append(pid)
        return top_purchases
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
            
    @staticmethod
    def get_order(uid, order_id):
        rows = app.db.execute('''
        SELECT *
        FROM PURCHASES
        WHERE uid = :uid AND order_id = :order_id
        ''', uid = uid, order_id=order_id)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_total_price_order(uid, order_id): #sums up quantity * price
        rows = app.db.execute("""
        WITH C(total) AS
            (SELECT quantity * price FROM Purchases
            WHERE uid = :uid AND Purchases.order_id = :order_id)
        SELECT SUM(total)
        FROM C
        """,
        uid=uid, order_id=order_id)
        return float(rows[0][0]) if rows and rows[0][0] is not None else 0.0
    
    @staticmethod
    def get_fulfillment_status(uid, order_id):
        fulfilled = True
        #loops through date fulfilled to get overall order status
        rows = app.db.execute('''
        SELECT date_fulfilled
        FROM Purchases
        WHERE uid = :uid AND Purchases.order_id = :order_id
        ''',
                              uid=uid, order_id=order_id)
        for row in rows:
            if row[0] == None:
                fulfilled = False
        if fulfilled:
            return "Fulfilled"
        else:
            return "Not fulfilled"

    @staticmethod
    def get_unique_orders_by_uid(uid):
        #returns orders, list of products, price, fulfillment status
        rows = app.db.execute('''
        SELECT DISTINCT order_id
        FROM Purchases
        WHERE uid = :uid
        ''',
                              uid=uid)
        unique_orders = []
        for row in rows:
            order_id = row[0]
            total_price = Purchase.get_total_price_order(uid, order_id)
            row_as_list = list(row) #make list so we can append results
            row_as_list.append(Purchase.get_order_products(uid, order_id))
            row_as_list.append(total_price)
            row_as_list.append(Purchase.get_fulfillment_status(uid, order_id))
            unique_orders.append(row_as_list)
        return unique_orders

    @staticmethod
    def get_order_products(uid, order_id):
        rows = app.db.execute('''
        SELECT name, Products.pid
        FROM PURCHASES, Products
        WHERE uid = :uid AND order_id = :order_id AND Purchases.pid = Products.pid
        ''', uid = uid, order_id=order_id)
        name_list = []
        for row in rows:
            name_list.append([str(row[0]), row[1]])
        #returns list of lists where inner list[0] is name, list[1] is id
        return name_list