from flask import current_app as app

class Product:
    def __init__(self, pid, name, description, image, altTxt, createdAt, updatedAt, cid, sid):
        self.pid = pid
        self.name = name
        self.description = description
        self.image = image
        self.altTxt = altTxt
        self.CreatedAt = createdAt
        self.UpdatedAt = updatedAt
        self.cid = cid
        self.sid = sid

    @staticmethod
    def get(pid):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE pid = :pid
        ''', pid=pid)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM Products
        ''')
        return [Product(*row) for row in rows]
    @staticmethod
    def get_az():
        rows = app.db.execute('''
        SELECT *
        FROM Products
        ORDER BY Products.name
        ''')
        return [Product(*row) for row in rows]
    @staticmethod
    def get_za():
        rows = app.db.execute('''
        SELECT *
        FROM Products
        ORDER BY Products.name DESC
        ''')
        return [Product(*row) for row in rows]
    @staticmethod
    def get_all_by_cat(cid):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE cid = :cid
        ''', cid=cid)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_name(pid):
        product = Product.get(pid)
        if product != None:
            return product.name
        else:
            return None
    @staticmethod
    def newPID():
        rows = app.db.execute("""
        SELECT MAX(pid)
        FROM Products
        """)
        return rows
        
    @staticmethod 
    def add_product(pid, name, description, image, altTxt, createdAt, updatedAt, cid, sid):
        app.db.execute("""
        INSERT INTO Products(pid, name, description, image, altTxt, createdAt, updatedAt, cid, sid)
        VALUES(:pid, :name, :description, :image, :altTxt, :createdAt, :updatedAt, :cid, :sid)
        """, 
        pid = pid, 
        name=name, 
        description=description, 
        image=image, altTxt=altTxt, 
        createdAt=createdAt, 
        updatedAt=updatedAt,
        cid=cid,
        sid=sid
        )
        return 
    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
        SELECT pid
        FROM Products
        WHERE sid = :sid
        ''', sid=sid)
        return [row[0] for row in rows]
    
    @staticmethod
    def edit(pid, name, description, image, altTxt, updatedAt, cid, sid):
        try:
            rows = app.db.execute("""
            UPDATE Products
            SET name=:name, description=:description, image=:image, altTxt=:altTxt, updatedAt=:updatedAt, cid=:cid
            WHERE pid=:pid AND sid=:sid
            """,
            pid = pid, 
            name=name, 
            description=description, 
            image=image, altTxt=altTxt, 
            updatedAt=updatedAt,
            cid=cid,
            sid=sid)
        except Exception as e:
            print(str(e))
    
class ProductRating:
    def __init__(self, pid, name, description, image, altTxt, createdAt, updatedAt, cid, rating):
        self.pid = pid
        self.name = name
        self.description = description
        self.image = image
        self.altTxt = altTxt
        self.CreatedAt = createdAt
        self.UpdatedAt = updatedAt
        self.cid = cid
        self.rating = rating
        
    def all_ratings():
        rows = app.db.execute('''
        SELECT p.pid, p.name, p.description, p.image, p.altTxt, p.createdAt, p.updatedAt, p.cid, AVG(f.rating) as avg_rating
        FROM Products as p
        JOIN ProductFeedback as f ON p.pid = f.pid
        GROUP BY p.pid, p.name, p.description, p.image, p.altTxt, p.createdAt, p.updatedAt, p.cid
        ORDER BY avg_rating DESC;
        ''')
        return [ProductRating(*row) for row in rows]
    
    def all_ratings_cid(cid):
        rows = app.db.execute('''
        SELECT p.pid, p.name, p.description, p.image, p.altTxt, p.createdAt, p.updatedAt, p.cid, AVG(f.rating) as avg_rating
        FROM Products as p
        JOIN ProductFeedback as f ON p.pid = f.pid
        WHERE p.cid = :cid
        GROUP BY p.pid, p.name, p.description, p.image, p.altTxt, p.createdAt, p.updatedAt, p.cid
        ORDER BY avg_rating DESC;
        ''', cid=cid)
        return [ProductRating(*row) for row in rows]