from flask import current_app as app

class ProductFeedback:
    def __init__(self,uid,name,pid,rating,review,date_time):
        self.uid = uid
        self.name = name
        self.pid = pid
        self.rating = rating
        self.review = review
        self.date_time = date_time

    @staticmethod
    def get_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        AND f.date_time >= :since
        ORDER BY f.date_time DESC
        ''',
        uid=uid,
        since=since)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_sort_rating(uid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        ORDER BY f.rating DESC
        ''',
        uid=uid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE p.pid = f.pid
        ORDER BY f.rating DESC
        ''')
        return [ProductFeedback(*row) for row in rows]

class SellerFeedback:
    def __init__(self,uid,firstname,lastname,sid,rating,review,date_time):
        self.uid = uid
        self.sid = sid
        self.firstname = firstname
        self.lastname = lastname
        self.rating = rating
        self.review = review
        self.date_time = date_time

    @staticmethod
    def get_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT f.uid, s.firstname, s.lastname, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        AND f.date_time >= :since
        ORDER BY f.date_time DESC
        ''',
        uid=uid,
        since=since)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_sort_rating(uid):
        rows = app.db.execute('''
        SELECT f.uid, s.firstname, s.lastname, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        ORDER BY f.rating DESC
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT f.uid, s.firstname, s.lastname, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE s.id = f.sid
        ''')
        return [SellerFeedback(*row) for row in rows]
