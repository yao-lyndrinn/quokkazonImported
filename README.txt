Team: Query Quokkas

Team members:
- Phillip Ding (User Guru) --> Main designer of user and purchases tables. For milestone 3, Phillip wrote app/allpurchases.py and app/templates/allpurchases.html which allows someone to enter a uid and receive a table of all purchases by that user. Phillip also updated app/__init__.py to include this additional page as well as app/templates/index.html to include a button widget to access the allpurchases page.

- Jonathan Shi (Seller Guru) --> Main designer of seller and inventory tables. For milestone 3, Jonathan wrote app/inventory.py, app/models/inventory.py, app/template/inventory.html, and updated index.html, and app/models/seller.py. Users registered as sellers in the database have access to an inventory button which shows their personal inventory, while signed out users or non-seller users will not have access to such a page.

- Amy Weng (Social Guru) --> Main designer of feedback and messages tables. For milestone 3, Amy wrote the app/feedback.py, models/feedback.py, allfeedback.html, and myfeedback.html files, and she put the corresponding links into index.html. 
IMPORTANT: Since recording the demo video, Amy has improved her endpoints for this milestone by allowing a user to view all feedback on the site. On this all_feedback page, users can query for the top 5 most recent feedback any user has left. Moreover, a logged-in user can view and sort both product and seller feedback on their own specific feedback record. The team's repository currently does not include the code for the older endpoints showed in the demo video. For the newest feedback endpoints, please see the Addendum (linked below) for a short video demonstration. These revisions were made so that the endpoints address the given instructions better.

- Lyndrinn Yao (Carts Guru) --> Main designer of carts table. For Milestone 3, Lyndrinn wrote app/cart.py, app/models/cart.py, app/templates/cart.html, and updated index.html accordingly. This allows for a Cart button that appears for signed in users that starts a query for items in the Cart table by the user ID of the logged in user. Currently, the files contain incomplete code for an Add to Cart feature that is commented out.

- Elise Zhang (Products Guru) --> Main designer of products, tags, and categories table. For milestone 3, Elise wrote the app/products.py, app/models/stock.py, app/templates/products.html, app/templates/topProducts.html files, and put corresponding links into index.html.

Everyone worked together to customize the website. 
https://gitlab.oit.duke.edu/query-quokkas/quokkazon 

Link to Video Demo: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/Demo.mp4?ref_type=heads
Link to Addendum: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/Addendum.mp4?ref_type=heads
