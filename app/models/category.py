from flask import current_app as app

class Category:
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM Category
        ''')
        return [Category(*row) for row in rows]
    
    def get_all_by_pid(pid):
        rows = app.db.execute('''
        SELECT *
        FROM Category
        WHERE pid = :pid
        ''', pid=pid)
        return [Category(*row) for row in rows]

    def get_all_categories():
        rows = app.db.execute('''
        SELECT DISTINCT name
        FROM Category;
        ''')
        return rows