import csv,random
from collections import defaultdict 
from faker import Faker
Faker.seed(0)
fake = Faker()

purchases = {}
with open("Purchases.csv",newline='') as file: 
    reader = csv.reader(file, delimiter=',')
    for row in reader: 
        uid,sid,pid = row[:3]
        if uid not in purchases: purchases[uid] = {}
        if sid not in purchases[uid]: purchases[uid][sid] = []
        purchases[uid][sid].append(pid)

sample_product_reviews = defaultdict(dict)
with open("Sample Reviews.csv",newline='') as file: 
    reader = csv.reader(file, delimiter=',')
    for row in reader: 
        pid,rating,review = row[0],row[1],row[3]
        sample_product_reviews[pid][int(rating)] = review


'''Generate feedback'''
def get_csv_writer(f):
    return csv.writer(f, dialect='unix')
# uid, pid/sid, rating, review, date_time 
product_file = open("ProductFeedback.csv","w")
seller_file = open("SellerFeedback.csv","w")
product_writer = get_csv_writer(product_file)
seller_writer = get_csv_writer(seller_file)

default_times = ["2023-11-01 13:12:58","2023-11-02 13:12:58","2023-11-03 13:12:58",
                "2023-11-04 13:12:58","2023-11-05 13:12:58","2023-11-06 13:12:58"]

users, seller_reviews, product_reviews = [],[],[]
for uid,info in purchases.items():
    users.append(uid)
    product_ratings = {}
    seller_ratings = {}
    seller_product_ratings = defaultdict(list)
    for sid, pid_list in info.items(): 
        for pid in pid_list:
            default_time = random.choice(default_times)
            # make sure that the user has not left a review for this product already 
            if pid in product_ratings: 
                seller_product_ratings[sid].append(product_ratings[pid])
                continue 
            # generate product rating and review (if applicable)
            p_rating = random.randint(1,5)
            # if random.choice([True,False]) and p_rating < 5: p_rating += 0.5
            seller_product_ratings[sid].append(p_rating)
            product_ratings[pid] = p_rating 
            # leave_p_review = random.choice([True,False])
            leave_p_review = True
            if leave_p_review: 
                length = random.randint(6,10)
                product_reviews.append((uid,pid))
                review = fake.sentence(nb_words=length)[:-1] + ". " + sample_product_reviews[pid][int(p_rating)] + " " + fake.sentence(nb_words=length)[:-1] + "." 
                product_writer.writerow([uid,pid,p_rating,review,default_time])
            else: 
                product_writer.writerow([uid,pid,p_rating,"",default_time])
        # make sure that the user has not left a review for this seller already 
        if sid in seller_ratings: continue 
        # rating for seller is the average of the ratings left for the products bought from that seller 
        s_rating = int(sum(seller_product_ratings[sid])/len(seller_product_ratings[sid]))
        seller_ratings[sid] = s_rating
        # if random.choice([True,False]) and s_rating < 5: s_rating += 0.5
        default_time = random.choice(default_times)
        # leave_s_review = random.choice([True,False])
        leave_s_review = True
        if leave_s_review: 
            length = random.randint(10,20)
            seller_reviews.append((uid,sid))
            seller_writer.writerow([uid,sid,s_rating,fake.sentence(nb_words=length)[:-1],default_time])
        else: 
            seller_writer.writerow([uid,sid,s_rating,"",default_time])
seller_file.close()
product_file.close()

seller_file = open("SellerReviewUpvotes.csv","w")
product_file = open("ProductReviewUpvotes.csv","w")
seller_upvotes = get_csv_writer(seller_file)
product_upvotes = get_csv_writer(product_file)
s_cap, p_cap = 100, 500
for user in users: 
    s_count, p_count = 0,0
    for uid, sid in seller_reviews: 
        # a user cannot upvote their own reviews 
        if user == uid: continue
        # make sure that upvotes are slightly uncommon 
        if random.choice([True,False,False,False,False]) == True: 
            seller_upvotes.writerow([user,uid,sid])
            s_count += 1 
        if s_count == s_cap: break
    for uid, pid in product_reviews: 
        # a user cannot upvote their own reviews 
        if user == uid: continue
        if random.choice([True,False,False,False]) == True: 
            product_upvotes.writerow([user,uid,pid])
            p_count += 1 
        if p_count == p_cap: break
seller_file.close()
product_file.close()