from flask import current_app as app

class ProductFeedback:
    def __init__(self,uid,pid,rating,review,date_time):
        self.uid = uid
        self.pid = pid
        self.rating = rating
        self.review = review
        self.date_time = date_time

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT *
        FROM ProductFeedback
        WHERE uid = :uid
        AND date_time >= :since
        ORDER BY date_time DESC
        ''',
        uid=uid,
        since=since)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_n_most_recent_by_uid(uid, n):
        rows = app.db.execute('''
        SELECT *
        FROM ProductFeedback
        WHERE uid = :uid
        ORDER BY date_time DESC
        ''',
        uid=uid)
        n_recent = []
        count = 0
        for row in rows: 
            count += 1 
            n_recent.append(ProductFeedback(*row))
            if count == n: break
        return n_recent
    
    def get_by_uid_filter_by_rating(uid, rating):
        rows = app.db.execute('''
        SELECT *
        FROM ProductFeedback
        WHERE uid = :uid
        AND rating = :rating
        ORDER BY date_time DESC
        ''',
        uid=uid, rating=rating)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_uid_sort_rating(uid):
        rows = app.db.execute('''
        SELECT *
        FROM ProductFeedback
        WHERE uid = :uid
        ORDER BY rating DESC
        ''',
        uid=uid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_pid_since(pid, since):
        rows = app.db.execute('''
        SELECT *
        FROM ProductFeedback
        WHERE pid = :pid
        AND date_time >= :since
        ORDER BY date_time DESC
        ''',
        pid=pid,
        since=since)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_pid_sort_rating(pid):
        rows = app.db.execute('''
        SELECT *
        FROM ProductFeedback
        WHERE pid = :pid
        ORDER BY rating DESC
        ''',
        sid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM SellerFeedback
        ''')
        return [ProductFeedback(*row) for row in rows]
