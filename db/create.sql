-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

-- CREATE TABLE Users (
--     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     email VARCHAR UNIQUE NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     firstname VARCHAR(255) NOT NULL,
--     lastname VARCHAR(255) NOT NULL
-- );

-- CREATE TABLE Products (
--     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     name VARCHAR(255) UNIQUE NOT NULL,
--     price DECIMAL(12,2) NOT NULL,
--     available BOOLEAN DEFAULT TRUE
-- );

-- CREATE TABLE Purchases (
--     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     uid INT NOT NULL REFERENCES Users(id),
--     pid INT NOT NULL REFERENCES Products(id),
--     time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
-- );

CREATE TABLE Users(
	uid INTEGER PRIMARY KEY NOT NULL
);

CREATE TABLE Seller (
	sid INTEGER PRIMARY KEY NOT NULL REFERENCES Users(uid)
);

CREATE TABLE Product (
    pid INTEGER PRIMARY KEY NOT NULL
);

CREATE TABLE Purchases(
    uid INTEGER NOT NULL REFERENCES Users(uid),
	sid INTEGER NOT NULL REFERENCES Seller(sid),
    pid INTEGER NOT NULL REFERENCES Product(pid), 
	order_id INTEGER NOT NULL,
	PRIMARY KEY (sid, pid, uid, order_id)
);

CREATE TABLE SellerFeedback(
	uid INTEGER NOT NULL REFERENCES Users(uid), 
	sid INTEGER NOT NULL REFERENCES Seller(sid),
	rating INTEGER NOT NULL CHECK(rating BETWEEN 1 and 5), -- should a user leave any feedback, they must leave a rating 
    review VARCHAR(4096), -- can be null because leaving a review is optional 
    date_time TIMESTAMP NOT NULL, -- YYYY-MM-DD hh:mm:ss
    PRIMARY KEY (uid, sid)  
);

CREATE TABLE ProductFeedback(
	uid INTEGER NOT NULL REFERENCES Users(uid), 
	pid INTEGER NOT NULL REFERENCES Product(pid),
	rating INTEGER NOT NULL CHECK(rating BETWEEN 1 and 5), -- should a user leave any feedback, they must leave a rating 
	review VARCHAR(4096), -- can be null because leaving a review is optional 
    date_time TIMESTAMP NOT NULL, -- YYYY-MM-DD hh:mm:ss
    PRIMARY KEY (uid, pid) 	
);

CREATE TABLE Message(
	sender_id INTEGER NOT NULL REFERENCES Users(uid),
	receiver_id INTEGER NOT NULL REFERENCES Users(uid),
    date_time TIMESTAMP NOT NULL, -- YYYY-MM-DD hh:mm:ss
	msg VARCHAR(4096) NOT NULL, -- cannot be null because a message must occur in order for it be recorded in this table  
    PRIMARY KEY (sender_id, receiver_id, date_time) 
);


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
    -- the next constraint applies only with insert statements 
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
    -- the next constraint applies only with insert statements 
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