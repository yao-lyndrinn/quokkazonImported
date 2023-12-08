from flask import current_app as app

class Product:
    def __init__(self, pid, name, description, image, altTxt, createdAt, updatedAt, cid):
        self.pid = pid
        self.name = name
        self.description = description
        self.image = image
        self.altTxt = altTxt
        self.CreatedAt = createdAt
        self.UpdatedAt = updatedAt
        self.cid = cid

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
        
    def newPID():
        rows = app.db.execute("""
        SELECT MAX(pid)
        FROM Products
        """)
        return rows
        
    @staticmethod 
    def add_product(pid, name, description, image, altTxt, createdAt, updatedAt, cid):
        app.db.execute("""
        INSERT INTO Products(pid, name, description, image, altTxt, createdAt, updatedAt, cid)
        VALUES(:pid, :name, :description, :image, :altTxt, :createdAt, :updatedAt, :cid)
        """, 
        pid = pid, 
        name=name, 
        description=description, 
        image=image, altTxt=altTxt, 
        createdAt=createdAt, 
        updatedAt=updatedAt,
        cid=cid
        )
        return
    
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