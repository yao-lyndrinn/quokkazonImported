from flask import current_app as app

class Stock:
    def __init__(self, pid, name, description, image, altTxt, createdAt, updatedAt, cid, price):
        self.pid = pid
        self.name = name
        self.description = description
        self.image = image
        self.altTxt = altTxt
        self.CreatedAt = createdAt
        self.UpdatedAt = updatedAt
        self.cid = cid
        self.price = price

    @staticmethod
    def get_all_in_stock():
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid, MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ''')
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_stock_desc():
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid,MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ORDER BY Inventory.price DESC
        ''')
        return [Stock(*row) for row in rows]
   
    @staticmethod
    def get_stock_asc():
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid, MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ORDER BY Inventory.price 
        ''')
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_stock_by_cat(cid):
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid, MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        WHERE cid = :cid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ''', cid = cid)
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_stock_by_cat_asc(cid):
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid, MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        WHERE cid = :cid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ORDER BY Inventory.price 
        ''', cid = cid)
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_stock_by_cat_dec(cid):
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid, MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        WHERE cid = :cid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ORDER BY Inventory.price DESC
        ''', cid = cid)
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_az():
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid, MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ORDER BY Products.name 
        ''')
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_za():
        rows = app.db.execute('''
        SELECT DISTINCT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, MIN(Products.createdAt) AS firstCreatedAt, Products.updatedAt, Products.cid, MIN(Inventory.price) as price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        GROUP BY Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.updatedAt, Products.cid
        ORDER BY Products.name DESC
        ''')
        return [Stock(*row) for row in rows]
    