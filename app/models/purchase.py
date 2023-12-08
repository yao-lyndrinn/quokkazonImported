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
    def get_order_counts_by_sid(sid):
        rows = app.db.execute('''
        WITH ProductNames(pid, pname) AS
        (SELECT pid, name FROM Products)
        SELECT pid, pname, SUM(quantity) AS sum
        FROM Purchases NATURAL JOIN ProductNames
        WHERE sid = :sid
        GROUP BY pid, pname
        ORDER BY sum DESC
        ''',
                              sid=sid)
        return rows
    
    @staticmethod
    def get_num_orders_per_month(sid, pid=None):
        today = datetime.date.today()
        current_year = today.year
        current_month = today.month
        year_range = 3
        if not pid:
            rows = app.db.execute('''
            WITH RECURSIVE months AS (
                SELECT 1 AS month
                UNION ALL
                SELECT month+1 FROM months WHERE month+1 <= 12
            ),
            years AS (
                SELECT :current_year-:year_range+1 AS year
                UNION ALL
                SELECT year+1 FROM years WHERE year+1 <= :current_year               
            )
            SELECT monthYears.month, monthYears.year, COALESCE(count,0)
            FROM (
                SELECT month, year, COUNT(order_id) AS count
                FROM (
                    SELECT sid, order_id, EXTRACT(MONTH FROM time_purchased) AS month, EXTRACT(YEAR FROM time_purchased) AS year
                    FROM Purchases
                ) AS OrderMonths
                WHERE sid = :sid
                GROUP BY month, year
            ) AS OrderMonths
            RIGHT JOIN (
                SELECT month, year
                FROM months CROSS JOIN years
                ORDER BY year, month
            ) AS monthYears
            ON monthYears.month = OrderMonths.month
            AND monthYears.year = OrderMonths.year
            WHERE (monthYears.year = :current_year AND monthYears.month <= :current_month)
            OR (monthYears.year = :current_year-:year_range AND monthYears.month > :current_month)
            OR (monthYears.year < :current_year AND monthYears.year > :current_year-:year_range)
            ORDER BY monthYears.year, monthYears.month
            ''',
                                sid=sid,
                                current_year=current_year,
                                current_month=current_month,
                                year_range=year_range)
        else:
            rows = app.db.execute('''
            WITH RECURSIVE months AS (
                SELECT 1 AS month
                UNION ALL
                SELECT month+1 FROM months WHERE month+1 <= 12
            ),
            years AS (
                SELECT :current_year-:year_range+1 AS year
                UNION ALL
                SELECT year+1 FROM years WHERE year+1 <= :current_year               
            )
            SELECT monthYears.month, monthYears.year, COALESCE(count,0)
            FROM (
                SELECT month, year, COUNT(order_id) AS count
                FROM (
                    SELECT sid, pid, order_id, EXTRACT(MONTH FROM time_purchased) AS month, EXTRACT(YEAR FROM time_purchased) AS year
                    FROM Purchases
                ) AS OrderMonths
                WHERE sid = :sid
                AND pid = :pid
                GROUP BY month, year
            ) AS OrderMonths
            RIGHT JOIN (
                SELECT month, year
                FROM months CROSS JOIN years
                ORDER BY year, month
            ) AS monthYears
            ON monthYears.month = OrderMonths.month
            AND monthYears.year = OrderMonths.year
            WHERE (monthYears.year = :current_year AND monthYears.month <= :current_month)
            OR (monthYears.year = :current_year-:year_range AND monthYears.month > :current_month)
            OR (monthYears.year < :current_year AND monthYears.year > :current_year-:year_range)
            ORDER BY monthYears.year, monthYears.month
            ''',
                                sid=sid,
                                pid=pid,
                                current_year=current_year,
                                current_month=current_month,
                                year_range=year_range)
        return rows

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
    def get_total_price_order(uid, order_id):
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
    def get_unique_orders_by_uid(uid):
        rows = app.db.execute('''
        SELECT DISTINCT order_id
        FROM Purchases
        WHERE uid = :uid
        ''',
                              uid=uid)
        return [row[0] for row in rows]