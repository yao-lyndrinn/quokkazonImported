Team: Query Quokkas

Team members:
- Phillip Ding (User Guru) --> Main designer of user and purchases tables. For milestone 3, Phillip wrote app/allpurchases.py and app/templates/allpurchases.html which allows someone to enter a uid and receive a table of all purchases by that user. Phillip also updated app/__init__.py to include this additional page as well as app/templates/index.html to include a button widget to access the allpurchases page. Features that have been added since the last milestone: Users now have a dedicatde profile page, users can now check their profile information, users can now register as sellers and gain access to all seller functionalities.

- Jonathan Shi (Seller Guru) --> Main designer of seller and inventory tables. For milestone 3, Jonathan wrote app/inventory.py, app/models/inventory.py, app/template/inventory.html, and updated index.html, and app/models/seller.py. Users registered as sellers in the database have access to an inventory button which shows their personal inventory, while signed out users or non-seller users will not have access to such a page.

- Amy Weng (Social Guru) --> Main designer of feedback and messages tables. For milestone 3, Amy wrote the app/feedback.py, models/feedback.py, allfeedback.html, and myfeedback.html files, and she put the corresponding links into index.html. For milestone 4, Amy expanded her app/feedback.py and model/feedback.py files, wrote db/data/feedback.py to generate the two feedback CSV files, wrote the functions to generate users and purchases (gen_users and gen_purchases) in db/generated/gen.py, and modified the app/products.py and productDetail.html file to incorporate feedback details onto individual product pages. Moreover, she updated index.html to place buttons to add or edit feedback next to each purchased product. 

- Lyndrinn Yao (Carts Guru) --> Main designer of carts table. For Milestone 3, Lyndrinn updated app/cart.py, app/models/cart.py, app/templates/cart.html, index.html, app/purchases.py, and wrote app/templates/sellerselection.html and app/templates/buyerorder.html. Features that have been added since the last milestone are the ability to view all sellers selling a product, add a product to the cart from a seller, update the quantity of an item in the cart, removing an item from the cart, displaying a calculated total price of items in the cart, and being able to submit the cart as an order, emptying the cart, updating the Purchases table and updating user balances accordingly.

- Elise Zhang (Products Guru) --> Main designer of products, tags, and categories table. For milestone 3, Elise wrote the app/products.py, app/models/stock.py, app/templates/products.html, app/templates/topProducts.html files, and put corresponding links into index.html.

Everyone worked together to customize the website. 
https://gitlab.oit.duke.edu/query-quokkas/quokkazon 

Link to Video Demo: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/Demo.mp4?ref_type=heads
Link to Addendum: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/Addendum.mp4?ref_type=heads
