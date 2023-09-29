INSERT INTO Users VALUES
  (1), (2), (3), (4);

INSERT INTO Seller VALUES 
  (2),(4);

INSERT INTO Product VALUES 
    (9), (10), (11), (12);

INSERT INTO Purchases VALUES 
    (1,2,9,1),
    (1,2,10,2),
    (1,2,11,3),
    (1,2,12,4),
    (3,2,9,5),
    (3,2,10,6),
    (3,2,11,7),
    (3,2,12,8),
    (1,4,9,9),
    (1,4,10,10),
    (1,4,11,11),
    (1,4,12,12);

INSERT INTO SellerFeedback VALUES 
    (1,2,4,'test1','2023-09-29 6:40:03'), 
    (1,4,4,'test2','2023-09-29 6:42:05'),
    (3,2,3,'test3','2023-09-29 6:43:08');

INSERT INTO ProductFeedback VALUES 
    (1,9,4,'test1','2023-09-29 6:40:03'), 
    (1,10,4,'test2','2023-09-29 6:42:05'),
    (1,11,3,'test3','2023-09-29 6:43:08'),
    (1,12,2,'test4','2023-09-29 6:45:12'),
    (3,9,5,'test5','2023-09-29 6:46:15'),
    (3,10,3,'test6','2023-09-29 6:48:23');

-- dropdb quokkazon; createdb quokkazon; psql quokkazon -af create.sql
-- psql quokkazon -af dummy_load.sql

-- select date_time, pid, rating, review from ProductFeedback where uid = 1 order by date_time DESC;
-- select pid, avg(rating), count(rating) from ProductFeedback group by pid order by avg(rating) DESC; 
-- select uid, rating, review, date_time from ProductFeedback where pid = 9 order by rating DESC; 
-- select uid, rating, review, date_time from ProductFeedback where pid = 9 order by date_time DESC; 