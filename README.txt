Team: Query Quokkas

Team members:
- Phillip Ding (User Guru) --> Main designer of user and purchases tables. For milestone 3, Phillip wrote app/allpurchases.py and app/templates/allpurchases.html which allows someone to enter a uid and receive a table of all purchases by that user. Phillip also updated app/__init__.py to include this additional page as well as app/templates/index.html to include a button widget to access the allpurchases page. Features that have been added since the last milestone: Users now have a dedicatde profile page, users can now check their profile information, users can now register as sellers and gain access to all seller functionalities.

- Jonathan Shi (Seller Guru) --> Main designer of seller and inventory tables. For milestone 3, Jonathan wrote app/inventory.py, app/models/inventory.py, app/template/inventory.html, and updated index.html, and app/models/seller.py. Users registered as sellers in the database have access to an inventory button which shows their personal inventory, while signed out users or non-seller users will not have access to such a page.

- Amy Weng (Social Guru) --> Main designer of feedback and messages tables. For milestone 3, Amy wrote the app/feedback.py, models/feedback.py, allfeedback.html, and myfeedback.html files, and she put the corresponding links into index.html. 
IMPORTANT: Since recording the demo video, Amy has improved her endpoints for this milestone by allowing a user to view all feedback on the site. On this all_feedback page, users can query for the top 5 most recent feedback any user has left. Moreover, a logged-in user can view and sort both product and seller feedback on their own specific feedback record. The team's repository currently does not include the code for the older endpoints showed in the demo video. For the newest feedback endpoints, please see the Addendum (linked below) for a short video demonstration. These revisions were made so that the endpoints address the given instructions better.

- Lyndrinn Yao (Carts Guru) --> Main designer of carts table. For Milestone 3, Lyndrinn updated app/cart.py, app/models/cart.py, app/templates/cart.html, index.html, app/purchases.py, and wrote app/templates/sellerselection.html and app/templates/buyerorder.html. Features that have been added since the last milestone are the ability to view all sellers selling a product, add a product to the cart from a seller, update the quantity of an item in the cart, removing an item from the cart, displaying a calculated total price of items in the cart, and being able to submit the cart as an order, emptying the cart, updating the Purchases table and updating user balances accordingly.

- Elise Zhang (Products Guru) --> 
    - Main designer of products, tags, and categories table. For milestone 3, Elise wrote the app/products.py, app/models/stock.py, app/templates/products.html, app/templates/topProducts.html files, and put corresponding links into index.html.
    - For milestone 4 Elise has:
        - Added a top products display on the home page,
        - Added a search bar to the header that searches through product names and description
        - Added a "add product" button on the inventory page that will allow users to add new products
        - Allowed pagination on the products pages
        - Allowed users to view certain categories
        - Allowed users to sort products by price
        - Made a product details page that displays product and seller information
        - Users can choose a seller to buy from and add the product to their cart

Everyone worked together to customize the website. 
https://gitlab.oit.duke.edu/query-quokkas/quokkazon 

We populate the database through the gen.py script: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/db/generated/gen.py?ref_type=heads
Link to Video Demo: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/Demo.mp4?ref_type=heads
Link to Addendum: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/Addendum.mp4?ref_type=heads
