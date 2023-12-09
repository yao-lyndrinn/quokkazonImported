CREATE TABLE Users(
	id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, 
	email VARCHAR(100) UNIQUE NOT NULL, 
  firstname VARCHAR(150) NOT NULL,
  lastname VARCHAR(150) NOT NULL,
	address TEXT NOT NULL,
	password VARCHAR(256) NOT NULL,
  phone_number VARCHAR(10) NOT NULL, 
	balance DECIMAL(10, 2) DEFAULT 0 
);

CREATE TABLE Seller (
	sid INTEGER PRIMARY KEY NOT NULL REFERENCES Users(id)   -- Seller id just references existing User id, all other Seller values can be taken from User table
);

CREATE TABLE Category (
  cid INTEGER PRIMARY KEY NOT NULL GENERATED BY DEFAULT AS IDENTITY, 
	name VARCHAR(400)NOT NULL,
  image VARCHAR(400)
);

CREATE TABLE Products (
  pid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
	name VARCHAR(400)NOT NULL,
  description VARCHAR(4096),
  image VARCHAR(400),
  altTxt VARCHAR(4096),
  CreatedAt timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
  UpdatedAt timestamp without time zone,
  cid INTEGER NOT NULL REFERENCES Category(cid),
  sid INTEGER NOT NULL REFERENCES Seller(sid)
);

CREATE TABLE Tag (
  pid INTEGER PRIMARY KEY NOT NULL REFERENCES Products(pid),
  name VARCHAR(400)NOT NULL
);

CREATE TABLE Purchases(   -- Contains all individual purchases, which are grouped by orders (a set of purchases made by one user at a point in time)
  uid INTEGER NOT NULL REFERENCES Users(id),
	sid INTEGER NOT NULL REFERENCES Seller(sid),
  pid INTEGER NOT NULL REFERENCES Products(pid), 
	order_id INTEGER NOT NULL,
  time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
	quantity INTEGER NOT NULL,
  price DECIMAL(6,2) NOT NULL,    -- price at time of purchase, not necessarily the same as the current price of the product
	date_fulfilled timestamp without time zone,   -- can be null of purchase has not yet be fulfilled by the seller
	PRIMARY KEY (sid, pid, uid, order_id)
);

CREATE TABLE Wishes (
  id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  uid INT NOT NULL REFERENCES Users(id),
  pid INT NOT NULL REFERENCES Products(pid),
  time_added timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Inventory (
	sid INTEGER NOT NULL REFERENCES Seller(sid),
	pid INTEGER NOT NULL REFERENCES Products(pid),
	quantity INTEGER NOT NULL,	
	num_for_sale INTEGER NOT NULL,
	price DECIMAL(6,2) NOT NULL,
	PRIMARY KEY (sid, pid)
);

CREATE TABLE SellerFeedback(
	uid INTEGER NOT NULL REFERENCES Users(id), 
	sid INTEGER NOT NULL REFERENCES Seller(sid),
	rating INTEGER NOT NULL CHECK(rating BETWEEN 1 and 5), -- should a user leave any feedback, they must leave a rating 
  review VARCHAR(4096), -- can be null because leaving a review is optional 
  date_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'), -- YYYY-MM-DD hh:mm:ss
  PRIMARY KEY (uid, sid)  
);

CREATE TABLE ProductFeedback(
	uid INTEGER NOT NULL REFERENCES Users(id), 
	pid INTEGER NOT NULL REFERENCES Products(pid),
	rating INTEGER NOT NULL CHECK(rating BETWEEN 1 and 5), -- should a user leave any feedback, they must leave a rating 
	review VARCHAR(4096), -- can be null because leaving a review is optional 
  date_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
  image VARCHAR(400),
  PRIMARY KEY (uid, pid) 	
);


CREATE TABLE UpvoteProductReview(
  uid INTEGER NOT NULL REFERENCES Users(id),
	reviewer INTEGER NOT NULL, 
	product INTEGER NOT NULL,
  PRIMARY KEY (uid, reviewer, product),
  FOREIGN KEY (reviewer,product) REFERENCES ProductFeedback(uid,pid)	
);

CREATE TABLE UpvoteSellerReview(
  uid INTEGER NOT NULL REFERENCES Users(id),
	reviewer INTEGER NOT NULL, 
	seller INTEGER NOT NULL,
  PRIMARY KEY (uid, reviewer, seller),	
  FOREIGN KEY (reviewer,seller) REFERENCES SellerFeedback(uid,sid)
);

CREATE TABLE Messages(
	sender INTEGER NOT NULL REFERENCES Users(id), 
	receiver INTEGER NOT NULL REFERENCES Users(id),
  date_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
	msg VARCHAR(4096) NOT NULL, -- cannot be null because a message must occur in order for it be recorded in this table  
  PRIMARY KEY (sender, receiver, date_time) 
);

CREATE TABLE Cart(
	uid INTEGER NOT NULL REFERENCES Users(id), 
	sid INTEGER NOT NULL REFERENCES Seller(sid),
  pid INTEGER NOT NULL REFERENCES Products(pid),
  quantity INTEGER NOT NULL,
  saved_for_later BIT,
  PRIMARY KEY (uid, sid, pid) 
  -- total price is quantity x price of item
  -- saved for later vs in cart (default)
  -- one line is identified by user, seller, and product which is for one quantity of item in that user’s cart
);

----------------------------------------------------------------------
-- user constraints

CREATE FUNCTION UserConstraints() RETURNS TRIGGER AS $$
BEGIN
  -- ensures that new messages have later timestamps 
  IF NEW.balance < 0 THEN
    RAISE EXCEPTION 'User balance must be nonnegative!';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER UserConstraints
  BEFORE INSERT OR UPDATE ON Users  -- deletions are ok
  FOR EACH ROW
  EXECUTE PROCEDURE UserConstraints();
----------------------------------------------------------------------
-- feedback constraints

CREATE FUNCTION FeedbackConstraints() RETURNS TRIGGER AS $$
BEGIN

  IF TG_TABLE_NAME = 'sellerfeedback' THEN 
    IF NEW.sid NOT IN (SELECT p.sid FROM Purchases as p where p.uid = NEW.uid) THEN 
    -- constraint that no user can leave any feedback for a seller they have not ordered from 
      RAISE EXCEPTION 'A user cannot leave any feedback for a seller they have not purchased from.';
    END IF; 
    -- the prior constraint applies to both insert and update statements
    -- the next constraint applies only to insertions 
    IF TG_OP = 'INSERT' THEN
        IF NEW.sid IN (SELECT f.sid from SellerFeedback as f where f.uid = NEW.uid) THEN
        -- constraint that each user can submit only one rating/review for a seller 
          RAISE EXCEPTION 'A user can leave at most one rating and review for each seller they have purchased from.'; 
        END IF; 
    END IF; 
  END IF;

  IF TG_TABLE_NAME = 'productfeedback' THEN 
    IF NEW.pid NOT IN (SELECT p.pid from Purchases as p where p.pid = NEW.pid) THEN 
    -- constraint that no user can leave any feedback for a product they have never purchased  
      RAISE EXCEPTION 'A user cannot leave any feedback for a product they have never purchased.';
    END IF;     
    -- the prior constraint applies to both insert and update statements
    -- the next constraint applies only to insertions 
    IF TG_OP = 'INSERT' THEN
        IF NEW.pid IN (SELECT f.pid from ProductFeedback as f where f.uid = NEW.uid) THEN
        -- constraint that each user can submit only one rating/review for a product 
            RAISE EXCEPTION 'A user can leave at most one rating and review for each product purchased.'; 
        END IF; 
    END IF; 
  END IF;
  RETURN NEW;

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER SellerFeedbackConstraints
  BEFORE INSERT OR UPDATE ON SellerFeedback -- deletions are ok 
  FOR EACH ROW
  EXECUTE PROCEDURE FeedbackConstraints();

CREATE TRIGGER ProductFeedbackConstraints
  BEFORE INSERT OR UPDATE ON ProductFeedback -- deletions are ok 
  FOR EACH ROW
  EXECUTE PROCEDURE FeedbackConstraints();

----------------------------------------------------------------------
-- inventory constraints

CREATE FUNCTION InventoryConstraints() RETURNS TRIGGER AS $$
BEGIN
  -- constraints the numeric values in quantity, price, and num_for_sale
  IF NEW.quantity < 0 THEN
    RAISE EXCEPTION 'Quantity of an product cannot be less than 0.';
  END IF;
  IF NEW.price < 0 THEN
    RAISE EXCEPTION 'Price of a product cannot be less than 0.';
  END IF;
  IF NEW.num_for_sale < 0 OR NEW.num_for_sale > NEW.quantity THEN
    RAISE EXCEPTION 'Number of product for sale cannot be less than 0 or exceed the quantity of the product.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER InventoryConstraints
  BEFORE INSERT OR UPDATE ON Inventory
  FOR EACH ROW
  EXECUTE PROCEDURE InventoryConstraints();

----------------------------------------------------------------------
-- purchase constraints

CREATE FUNCTION PurchaseConstraints() RETURNS TRIGGER AS $$
BEGIN
  -- constraints the values in date_fulfilled, quantity, and price at time of purchase
  IF NEW.date_fulfilled IS NOT NULL AND NEW.date_fulfilled < NEW.time_purchased THEN
    RAISE EXCEPTION 'Fulfillment date cannot be before time of purchase';
  END IF;
  IF NEW.quantity < 0 THEN
    RAISE EXCEPTION 'Quantity of an purchase cannot be less than 0.';
  END IF;
  IF NEW.price < 0 THEN
    RAISE EXCEPTION 'Price of a purchase cannot be less than 0.';
  END IF;
  IF EXISTS (SELECT * from Purchases AS p WHERE p.order_id = NEW.order_id AND NEW.uid <> p.uid) THEN
    RAISE EXCEPTION 'Different users cannot make the same order';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER PurchaseConstraints
  BEFORE INSERT OR UPDATE ON Purchases    -- deletions are ok
  FOR EACH ROW
  EXECUTE PROCEDURE PurchaseConstraints();

----------------------------------------------------------------------
-- messages constraints

CREATE FUNCTION MessageConstraints() RETURNS TRIGGER AS $$
BEGIN
  -- ensures that new messages have later timestamps 
  IF NEW.date_time <= (SELECT MAX(date_time) FROM Messages WHERE sender = NEW.sender and receiver = NEW.receiver) THEN
    RAISE EXCEPTION 'New messages in this thread must be dated at a later time than all existing messages between this user and seller.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER MessageConstraints
  BEFORE INSERT OR UPDATE ON Messages
  FOR EACH ROW
  EXECUTE PROCEDURE MessageConstraints();