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
    
    @staticmethod
    def get_by_uid_pid(uid, pid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        AND f.pid = :pid
        ORDER BY f.date_time DESC
        ''',
        uid=uid,
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def edit_rating(uid,pid,rating,time_updated):
        app.db.execute("""
        UPDATE ProductFeedback 
        SET rating = :rating, date_time = :time_updated                       
        WHERE uid = :uid 
        AND pid = :pid 
        """,
        uid=uid,
        pid=pid,
        rating=rating,
        time_updated = time_updated)
    
    @staticmethod
    def edit_review(uid,pid,review,time_updated):
        app.db.execute("""
        UPDATE ProductFeedback 
        SET review = :review, date_time = :time_updated                       
        WHERE uid = :uid 
        AND pid = :pid 
        """,
        uid=uid,
        pid=pid,
        review=review,
        time_updated = time_updated)
    
    @staticmethod
    def remove_feedback(uid,pid):
        app.db.execute("""
        DELETE from ProductFeedback 
        WHERE uid = :uid 
        AND pid = :pid 
        """,
        uid=uid,
        pid=pid)
    


class SellerFeedback:
    def __init__(self,uid,name,sid,rating,review,date_time):
        self.uid = uid
        self.sid = sid
        self.name = name
        self.rating = rating
        self.review = review
        self.date_time = date_time

    @staticmethod
    def get_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
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
    def get_by_uid_sid(uid, sid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        AND f.sid = :sid
        ORDER BY f.date_time DESC
        ''',
        uid=uid,
        sid=sid)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_sort_rating(uid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
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
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE s.id = f.sid
        ''')
        return [SellerFeedback(*row) for row in rows]

    @staticmethod
    def edit_rating(uid,sid,rating,time_updated):
        app.db.execute("""
        UPDATE SellerFeedback 
        SET rating = :rating, date_time = :time_updated                       
        WHERE uid = :uid 
        AND sid = :sid 
        """,
        uid=uid,
        sid=sid,
        rating=rating,
        time_updated = time_updated)
    
    @staticmethod
    def edit_review(uid,sid,review,time_updated):
        app.db.execute("""
        UPDATE SellerFeedback 
        SET review = :review, date_time = :time_updated                       
        WHERE uid = :uid 
        AND sid = :sid 
        """,
        uid=uid,
        sid=sid,
        review=review,
        time_updated = time_updated)

    @staticmethod
    def remove_feedback(uid,sid):
        app.db.execute("""
        DELETE from SellerFeedback 
        WHERE uid = :uid 
        AND sid = :sid 
        """,
        uid=uid,
        sid=sid)
