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
product_writer = get_csv_writer(open("ProductFeedback.csv","w"))
seller_writer = get_csv_writer(open("SellerFeedback.csv","w"))

default_time = "2023-11-01 13:12:58"
for uid,info in purchases.items(): 
    for sid, pid_list in info.items(): 
        p_ratings = []
        for pid in pid_list: 
            p_rating = random.randint(1,5)
            p_ratings.append(p_rating)
            # leave_p_review = random.choice([True,False])
            leave_p_review = True
            if leave_p_review: 
                product_writer.writerow([uid,pid,p_rating,sample_product_reviews[pid][p_rating],default_time])
            else: 
                product_writer.writerow([uid,pid,p_rating,"",default_time])
        # rating for seller is the average of the ratings left for the products bought from that seller 
        s_rating = int(sum(p_ratings)/len(p_ratings))
        # leave_s_review = random.choice([True,False])
        leave_s_review = True
        if leave_s_review: 
            length = random.randint(10,20)
            seller_writer.writerow([uid,sid,s_rating,fake.sentence(nb_words=length)[:-1],default_time])
        else: 
            seller_writer.writerow([uid,sid,s_rating,"",default_time])
        