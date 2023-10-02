from flask import current_app as app

class SellerFeedback:
    def __init__(self,uid,sid,rating,review,date_time):
        self.uid = uid
        self.sid = sid
        self.rating = rating
        self.review = review
        self.date_time = date_time

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT *
        FROM SellerFeedback
        WHERE uid = :uid
        AND date_time >= :since
        ORDER BY date_time DESC
        ''',
        uid=uid,
        since=since)
        return [SellerFeedback(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_sort_rating(uid):
        rows = app.db.execute('''
        SELECT *
        FROM SellerFeedback
        WHERE uid = :uid
        ORDER BY rating DESC
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_sid_since(sid, since):
        rows = app.db.execute('''
        SELECT *
        FROM SellerFeedback
        WHERE sid = :sid
        AND date_time >= :since
        ORDER BY date_time DESC
        ''',
        sid=sid,
        since=since)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM SellerFeedback
        ''')
        return [SellerFeedback(*row) for row in rows]
