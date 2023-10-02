from flask import current_app as app

class Inventory:
    def __init__(self, sid, pid, quantity, num_for_sale, price):
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.num_for_sale = num_for_sale
        self.price = price

    @staticmethod
    def get_all_by_sid(sid):
        print("SID:",sid)
        rows = app.db.execute('''
        SELECT *
        FROM Inventory
        WHERE sid = :sid
        ''', sid=sid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM Inventory
        ''')
        return [Inventory(*row) for row in rows]
