Team: Query Quokkas

Team members:
- Phillip Ding (User Guru) --> Main designer of user and purchases tables. 
For the final project, Phillip created a user lookup page for looking up any user based on their name or components of their name. The user search results page is also paginated and redirects to a user's public profile. Phillip also added features to the user profile page that allows users to top-up their balance and edit their information (following the constraints for registration) .
For milestone 3, Phillip wrote app/allpurchases.py and app/templates/allpurchases.html which allows someone to enter a uid and receive a table of all purchases by that user. Phillip also updated app/__init__.py to include this additional page as well as app/templates/index.html to include a button widget to access the allpurchases page. Features that have been added since the last milestone: Users now have a dedicated profile page, users can now check their profile information, users can now register as sellers and gain access to all seller functionalities.

- Jonathan Shi (Seller Guru) --> Main designer of seller and inventory tables. For milestone 4, Jonathan wrote app/templates/editInventory.html, app/templates/orders.html and modified app/allpurchases.py, app/inventory.py, app/models/inventory.py, app/models/purchase.py. The inventory display has been updated to exclude product ID, sellers can now add, edit, and remove items from their inventory, as well as view and fulfill their orders plus add existing products to their inventory from the products page. Also updated some miscellaneous html template files to allow sellers to add existing products and improve flow between pages.

- Amy Weng (Social Guru) --> Main designer of feedback, upvotes, and messages tables. 
    For the final project, Amy changed all feedback tables to DataTables with sorted in reverse chronological order by default, implemented an upvote functionality, pinned the top three upvoted reviews for sellers and products, and incorporated appropriate links to add or edit feedback on the detailed order page, the detailed product page, and sellers’ public profile pages if the constraints are satisfied (i.e., the user has purchased from that seller before). Moreover, Amy implemented the messages inbox and private threads, and she revised the product feedback relation in the database to also include the file path to an image uploaded by the reviewer. Amy also revised db/data/feedback.py to generate sample product feedback data with image file paths and messages between users. 
    For milestone 4, Amy created myfeedback_edit.html and myfeedback_add.html, and she expanded the my_feedback.html, app/feedback.py and model/feedback.py files that she had created for the third milestone. She also wrote db/data/feedback.py to generate the two feedback CSV files, wrote the functions to generate users and purchases (gen_users and gen_purchases) in db/generated/gen.py, and modified the app/products.py and productDetail.html files to incorporate feedback details into individual product pages. Moreover, she updated index.html to place buttons to add or edit feedback next to each purchased product. 

- Lyndrinn Yao (Carts Guru) --> Main designer of carts table. For Milestone 4, Lyndrinn updated app/cart.py, app/models/cart.py, app/templates/cart.html, index.html, app/purchases.py, and wrote app/templates/sellerselection.html and app/templates/buyerorder.html. Features that have been added since the last milestone are the ability to view all sellers selling a product, add a product to the cart from a seller, update the quantity of an item in the cart, removing an item from the cart, displaying a calculated total price of items in the cart, and being able to submit the cart as an order, emptying the cart, updating the Purchases table and updating user balances accordingly.
    -Since the last milestone, features added include:
        -Adjusting Purchases table to include a stored price, so that prices in order history do not change when sellers update item prices
        -Adjusting buyerOrder.html, app/models/purchase.py, where fulfillment status can be seen for the order and final price is now taken from purchases table instead of inventory
        -Adding viewOrders.html, where users can find summaries of past orders and order fulfillment status
        -Updating cart.html, app/cart.py, app/models/cart.py
            -Prices on cart submission now directly stored in Purchases
            -Inventory now properly decrements items in stock on cart submission
            -Inventory checks inventories on submission as well, in case stock has decreased since last cart view
            -Now includes "save for later" and promotional code "QUOLIDAY25" bonus functionality
                -Save for later removes item from price calculation and excludes it from submission
                -promotional code allows for 25% discount on all items, which is taken into account during balance adjustment
                -items can be moved between saved for later and fully in the cart at will
            -Links to product and seller info instead of just displaying IDs
        -Updating productDetail.html
            -Save for later option in addition to adding to cart
        -Fixed many bugs
            -User is no longer allowed to:
                -Add duplicate items to cart
                -Put more items into cart than are in stock
                -Make orders that would put their balance at a negative value
                -Add items with no value for quantity from product details page
                -Change quantity of item in the cart to nothing
        -Retired wishlist page, widget, and all related references.
        -Retired sellerselection page, as this info is now included on productDetails.

- Elise Zhang (Products Guru) --> 
    - Main designer of products, and categories table. For milestone 3, Elise wrote the app/products.py, app/models/stock.py, app/templates/products.html, app/templates/topProducts.html files, and put corresponding links into index.html.
    - For milestone 4 Elise has:
        - Created or updated: app/models/category.py, app/categories.py, app/products.py, app/carts.py, app/models/purchase.py, app/models/stock.py, app/static/css/main.css, app/templates/index.html, app/templates/productDetail.html, app/templates/products2.html, app/templates/searchResults2.html
        - Added a top products display on the home page,
        - Added a search bar to the header that searches through product names and description
        - Added a "add product" button on the inventory page that will allow users to add new products
        - Allowed pagination on the products pages
        - Allowed users to view certain categories
        - Allowed users to sort products by price
        - Made a product details page that displays product and seller information
        - Users can choose a seller to buy from and add the product to their cart
    For final:
        - Fixed all filtering and sorting functionalities
        - Added a recently viewed section on the home page
        - Finished allowing users to sort by category and filter/sort on top of that
        - Added an edit products button for sellers that crated a product
        - Contributed to the overall aesthetics of the site including form css, product cards, footer, and promotional sale banner
        - Fixed pagination errors
        - Fixed some card display errors
        - worked with others on some of their guru features


Everyone worked together to customize the website, debug, and verify the functionality of features. 
https://gitlab.oit.duke.edu/query-quokkas/quokkazon 

We populate the database through the gen.py script: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/db/generated/gen.py?ref_type=heads
NOTE: We also used ChatGPT to create quokka themed products

Link to 316 Quokkazon video: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/316%20Quokkazon%20-%20SD%20480p.mov?ref_type=heads
Or use this link: https://www.youtube.com/watch?v=Sg1VDMfSGR0&ab_channel=EliseZhang

