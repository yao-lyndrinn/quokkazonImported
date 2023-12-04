import csv

input_cat = '/home/ubuntu/quokkazon/db/data/finished_cat.csv'
input_product = '/home/ubuntu/quokkazon/db/data/Products.csv'
output_file = '/home/ubuntu/quokkazon/db/data/Products_new.csv'

column_to_add = []

with open(input_cat, 'r') as source:
    reader = csv.reader(source)
    for row in reader:
        column_to_add.append(row[0])
        
product_data = []

with open(input_product, 'r') as target:
    reader = csv.reader(target)
    product_data = list(reader)
    
for i, row in enumerate(product_data):
    row.append(column_to_add[i])
    
with open(output_file, 'w', newline='') as destination_file:
    writer = csv.writer(destination_file)
    writer.writerows(product_data)