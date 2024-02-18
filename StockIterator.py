import itertools
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

# Create a cursor object
cursor = conn.cursor()

# Generate permutations of 3 alphabetic characters with repetition allowed
permutations = itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=4)

# Print the permutations
for perm in permutations:
    value = ''.join(perm)
    print(value)
    data = (value, None,  None, None, None, None, None, None, 'false')
    # Execute SQL INSERT statement
    cursor.execute("INSERT INTO track_it.stock_master (ticker_name, stock_name, stock_industry, stock_sector, dummy1, dummy2,dummy3, available_date, is_available) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",data)
    conn.commit()
cursor.close()
conn.close()