from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
from collections import defaultdict
from datetime import datetime

num_users = 100
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['address']
            phone_number=fake.phone_number().replace(".","").split("x")[0]
            # print([uid,email,firstname,lastname,address,password,phone_number,0])
            writer.writerow([int(uid),email,firstname,lastname,address,password,phone_number,0])
        print(f'{num_users} generated')
    return

def get_available_products(file):
    available = defaultdict(list)
    with open(file,"r") as f: 
        info = f.readlines()
        for line in info: 
            # (sid, pid)
            sid = line.split(',')[0]
            pid = line.split(',')[1]
            available[pid].append(sid)
    return available 

# uid, sid, pid, order_id, time_purchased, quantity, date_fulfilled 
def gen_purchases(num_purchases, available):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available.keys())
            sid = random.choice(available[pid])
            quantity_available = len(available[pid])
            # ensure that items cannot be re-purchased 
            available[pid].remove(sid)
            if len(available[pid]) == 0: 
                del available[pid]

            time_purchased = fake.date_this_month().strftime("%Y-%m-%d %H:%M:%S")
            
            quantity = fake.random_int(min=0,max=quantity_available)
            # print([uid, sid, pid, time_purchased,quantity])
            writer.writerow([uid, sid, pid, time_purchased,quantity])
        print(f'{num_purchases} generated')
    return

if __name__ == "__main__": 
    # gen_users(num_users)
    available = get_available_products("/home/ubuntu/quokkazon/db/data/Inventory.csv")
    gen_purchases(2, available)



def gen_sellers(num_users):
    with open('Sellers.csv','w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        random.seed('quokka')
        num_sellers = 0
        for id in range(num_users):
            if random() < 0.2:
                writer.writerow([id])
                num_sellers += 1
        print(f'{num_sellers} users designated as sellers')
    return

def get_sellers(file):
    with open(file,'r') as f:
        return [int(sid) for sid in f.readlines()]

"""def gen_inventory():
    with open('Inventory.csv','w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        random.seed('quokka')
        rows_added = 0
        for sid in get_sellers('/home/ubuntu/quokkazozn/db/data/Sellers.csv'):
            num_items = randint(1,10)
            products = random.sample(get_pids('/home/ubuntu/quokkazon/db/data/Products.csv',num_items)
            for product in products:
                quantity = randint(0,1000)
                num_for_sale = randint(0,quantity)
                price = randint(0,30) + 0.99
                writer.writerow([sid, pid, quantity, num_for_sale, price])
                rows_added += 1
        print(f'{rows_added} enntries added to Inventory')
    return   """


