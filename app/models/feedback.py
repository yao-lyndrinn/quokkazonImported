from flask import current_app as app

class ProductFeedback:
    def __init__(self,uid,name,pid,rating,review,date_time):
        self.uid = uid
        self.name = name
        self.pid = pid
        self.rating = rating
        self.review = review
        self.date_time = date_time

    def summary_ratings(pid): 
        info = app.db.execute('''
        SELECT COUNT(f.rating), AVG(f.rating)
        FROM ProductFeedback as f
        WHERE f.pid = :pid
        ''', pid=pid)
        if info[0][1] is None:
            return (None,0)
        num = info[0][0]
        avg = round(info[0][1],1)
        return (avg,num)
    
    def user_summary_ratings(uid): 
        info = app.db.execute('''
        SELECT COUNT(f.rating), AVG(f.rating)
        FROM ProductFeedback as f
        WHERE f.uid = :uid
        ''', uid=uid)
        if info[0][1] is None:
            return (None,0)
        avg = round(info[0][1],1)
        return (avg,info[0][0])
    
    def all_pids(): 
        info = app.db.execute('SELECT pid FROM ProductFeedback')
        return info
    
    # current user's ratings and reviews for products 
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        ORDER BY f.date_time DESC, p.name
        ''',
        uid=uid)
        return [ProductFeedback(*row) for row in rows]
    
    # get all feedback for a given product 
    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u
        WHERE f.pid = :pid
        AND f.uid = u.id
        ORDER BY f.date_time DESC, (u.firstname || ' ' || u.lastname)
        ''',
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE p.pid = f.pid
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
        ORDER BY f.date_time DESC, p.name
        ''',
        uid=uid,
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def sorted_by_upvotes(pid):
        rows = app.db.execute('''
        WITH upvotes AS (
            SELECT reviewer, Count(reviewer) AS votes
            FROM UpvoteProductReview 
            WHERE product = :pid 
            GROUP BY reviewer  
        )
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u, upvotes as up 
        WHERE f.pid = :pid
        AND f.uid = u.id
        AND up.reviewer = f.uid
        ORDER BY up.votes DESC
        ''',
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

    @staticmethod 
    def remove_upvotes(reviewer,product):
        # delete upvotes for this review 
        app.db.execute("""
        DELETE from UpvoteProductReview 
        WHERE reviewer = :reviewer 
        AND product = :product 
        """,
        reviewer=reviewer,
        product=product)

    @staticmethod 
    def my_upvote(uid,reviewer,product):
        upvoted = app.db.execute("""
        SELECT Count(*)
        FROM UpvoteProductReview 
        WHERE uid = :uid 
        AND reviewer = :reviewer
        AND product = :product 
        """,
        uid=uid,
        reviewer=reviewer,
        product=product)
        return upvoted
    
    @staticmethod 
    def remove_my_upvote(user,reviewer,product):
        app.db.execute("""
        DELETE from UpvoteProductReview 
        WHERE reviewer = :reviewer 
        AND product = :product 
        AND uid = :user
        """,
        user=user,
        reviewer=reviewer,
        product=product)

    @staticmethod 
    def add_my_upvote(user,reviewer,product):
        app.db.execute("""
        INSERT INTO UpvoteProductReview VALUES (:user,:reviewer,:product)
        """,
        user=user,
        reviewer=reviewer,
        product=product)

    @staticmethod 
    def upvote_count(reviewer,product):
        rows = app.db.execute("""
        SELECT Count(*)
        FROM UpvoteProductReview 
        WHERE reviewer = :reviewer 
        AND product = :product 
        """,
        reviewer=reviewer,
        product=product)
        return rows

    @staticmethod
    def feedback_exists(uid,pid): 
        exists = app.db.execute("""
        SELECT f.uid
        FROM ProductFeedback f                         
        WHERE f.uid = :uid
        AND f.pid = :pid 
        """,
        uid=uid,
        pid=pid)
        return exists 
    
    @staticmethod
    def has_purchased(uid,pid): 
        purchased = app.db.execute("""
        SELECT Purchases.time_purchased
        FROM Purchases, Products, Users u
        WHERE Purchases.uid = :uid
        AND Purchases.uid = u.id
        AND Purchases.pid = :pid
        AND Purchases.pid = Products.pid 
        ORDER BY Purchases.time_purchased
        """,
        uid=uid,
        pid=pid)
        return purchased 

    @staticmethod 
    def add_feedback(uid,pid,rating,review,time): 
        app.db.execute("""
        INSERT INTO ProductFeedback VALUES (:uid,:pid,:rating,:review,:date_time)
        """,
        uid=uid,
        pid=pid,
        rating=rating,
        review=review,
        date_time=time)
    
    @staticmethod 
    def get_product_name(pid): 
        name = app.db.execute("""
        SELECT name 
        FROM Products
        WHERE pid = :pid
        """,
        pid=pid)
        return name 


class SellerFeedback:
    def __init__(self,uid,name,sid,rating,review,date_time):
        self.uid = uid
        self.sid = sid
        self.name = name
        self.rating = rating
        self.review = review
        self.date_time = date_time

    def summary_ratings(sid): 
        info = app.db.execute('''
        SELECT COUNT(f.rating), AVG(f.rating)
        FROM SellerFeedback as f
        WHERE f.sid = :sid
        ''', sid=sid)
        num = info[0][0]
        avg = round(info[0][1],1)
        return (avg,num)
    
    def user_summary_ratings(uid): 
        info = app.db.execute('''
        SELECT COUNT(f.rating), AVG(f.rating)
        FROM SellerFeedback as f
        WHERE f.uid = :uid
        ''', uid=uid)
        if info[0][1] is None:
            return (None,0)
        avg = round(info[0][1],1)
        return (avg,info[0][0])
    
    # current user's ratings and reviews 
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        ORDER BY f.date_time DESC, (s.firstname || ' ' || s.lastname)
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_sid(uid, sid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        AND f.sid = :sid
        ORDER BY f.date_time DESC, (s.firstname || ' ' || s.lastname)
        ''',
        uid=uid,
        sid=sid)
        return [SellerFeedback(*row) for row in rows]
    
    # get all feedback for a given seller 
    @staticmethod
    def get_by_sid(sid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as u
        WHERE f.sid = :sid
        AND f.uid = u.id
        ORDER BY f.date_time DESC, (u.firstname || ' ' || u.lastname)
        ''',
        sid=sid)
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
    
    @staticmethod
    def sorted_by_upvotes(sid):
        rows = app.db.execute('''
        WITH upvotes AS (
            SELECT reviewer, Count(reviewer) AS votes
            FROM UpvoteSellerReview 
            WHERE seller = :sid 
            GROUP BY reviewer  
        )
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as u, upvotes as up 
        WHERE f.sid = :sid
        AND f.uid = u.id
        AND up.reviewer = f.uid
        ORDER BY up.votes DESC
        ''',
        sid=sid)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod 
    def remove_upvotes(reviewer,seller):
        # delete upvotes for this review 
        app.db.execute("""
        DELETE from UpvoteSellerReview 
        WHERE reviewer = :reviewer 
        AND seller = :seller 
        """,
        reviewer=reviewer,
        seller=seller)
    
    @staticmethod 
    def remove_my_upvote(user,reviewer,seller):
        app.db.execute("""
        DELETE from UpvoteSellerReview 
        WHERE reviewer = :reviewer 
        AND seller = :seller 
        AND uid = :user
        """,
        user=user,
        reviewer=reviewer,
        seller=seller)

    @staticmethod 
    def add_my_upvote(user,reviewer,seller):
        app.db.execute("""
        INSERT INTO UpvoteSellerReview VALUES (:user,:reviewer,:seller)
        """,
        user=user,
        reviewer=reviewer,
        seller=seller)

    @staticmethod 
    def upvote_count(reviewer,seller):
        rows = app.db.execute("""
        SELECT Count(*)
        FROM UpvoteSellerReview 
        WHERE reviewer = :reviewer 
        AND seller = :seller 
        """,
        reviewer=reviewer,
        seller=seller)
        return rows 

    @staticmethod 
    def my_upvote(uid,reviewer,seller):
        upvoted = app.db.execute("""
        SELECT Count(*)
        FROM UpvoteSellerReview 
        WHERE uid = :uid 
        AND reviewer = :reviewer
        AND seller = :seller 
        """,
        uid=uid,
        reviewer=reviewer,
        seller=seller)
        return upvoted


    @staticmethod 
    def add_feedback(uid,sid,rating,review,time): 
        app.db.execute("""
        INSERT INTO SellerFeedback VALUES (:uid,:sid,:rating,:review,:date_time)
        """,
        uid=uid,
        sid=sid,
        rating=rating,
        review=review,
        date_time=time)

    @staticmethod 
    def get_name(sid): 
        name = app.db.execute("""
        SELECT (firstname || ' ' || lastname) AS name 
        FROM Users
        WHERE id = :sid
        """,
        sid=sid)
        return name[0][0] 
   
    @staticmethod
    def feedback_exists(uid,sid): 
        exists = app.db.execute("""
        SELECT f.uid
        FROM SellerFeedback f                         
        WHERE f.uid = :uid
        AND f.sid = :sid 
        """,
        uid=uid,
        sid=sid)
        return exists 
    @staticmethod 
    def has_purchased(uid,sid):
        if uid == sid: 
            # a seller cannot leave a self-review
            return None
        
        # find the products the user with the given uid has bought from the seller with the given sid
        rows = app.db.execute("""
        SELECT Products.pid, Products.name, Purchases.time_purchased
        FROM Purchases, Products, Users u
        WHERE Purchases.uid = :uid
        AND Purchases.sid = :sid
        AND Purchases.uid = u.id
        AND Purchases.pid = Products.pid 
        """,
        sid=sid,
        uid=uid)

        if len(rows) > 0: 
            return rows 
        else: 
            return rows

