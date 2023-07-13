import sqlite3
import time
import matplotlib.pyplot as plt
import numpy as np
from random import choice


# Function to execute the query and return the execution time
def execute_query(cursor, query):
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time

query = '''
SELECT COUNT(*) 
FROM Orders 
WHERE customer_id IN (SELECT customer_id FROM Customers WHERE customer_postal_code={0}) 
AND order_id IN (SELECT order_id FROM Order_items GROUP BY order_id HAVING COUNT(*) > 1)
'''

# Create list to store the time
results = {"Uninformed": [0 for i in range(3)], "Self": [0 for i in range(3)], "User": [0 for i in range(3)]}

# Connect to all 3 database and execute Q1 50 times for each scenario
for num, database_name in enumerate(['A3small.db', 'A3medium.db', 'A3large.db']):
    for scenario in results:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        
        if scenario == "Uninformed":
            cursor.execute("ALTER TABLE Customers RENAME TO old_Customers")
            cursor.execute("ALTER TABLE Orders RENAME TO old_Orders")
            cursor.execute("ALTER TABLE Order_items RENAME TO old_Order_items")
            cursor.execute("""CREATE TABLE "Customers" (
            "customer_id" TEXT,
            "customer_postal_code" INTEGER)""")
            cursor.execute("""CREATE TABLE "Orders" (
            "order_id" TEXT,
            "customer_id" TEXT)""")
            cursor.execute("""CREATE TABLE "Order_items" (
            "order_id" TEXT,
            "order_item_id" INTEGER,
            "product_id" TEXT,
            "seller_id" TEXT)""")
            cursor.execute("INSERT INTO Customers SELECT * FROM old_Customers")
            cursor.execute("INSERT INTO Orders SELECT * FROM old_Orders")
            cursor.execute("INSERT INTO Order_items SELECT * FROM old_Order_items")
            cursor.execute('PRAGMA foreign_keys = OFF')
            cursor.execute('PRAGMA automatic_index = OFF')
            connection.commit()
        
        else:
            cursor.execute('PRAGMA foreign_keys = ON')
            cursor.execute('PRAGMA automatic_index = ON')
            connection.commit()
        
        if scenario == "User":
            cursor.execute('CREATE INDEX idx_customers_customer_postal_code ON Customers(customer_postal_code)')
            cursor.execute('CREATE INDEX idx_order_items_order_id ON Order_items(order_id)')
            connection.commit()
        random_values = cursor.execute("SELECT customer_postal_code FROM Customers").fetchall()
        for i in range(50):
            random_value = choice(random_values)[0]
            execution_time = execute_query(cursor, query.format(random_value))
            results.get(scenario)[num] += execution_time * 1000
        results.get(scenario)[num] /= 50
        
        if scenario == "Uninformed":
            cursor.execute("DROP TABLE Customers")
            cursor.execute("ALTER TABLE old_Customers RENAME TO Customers")
            cursor.execute("DROP TABLE Orders")
            cursor.execute("ALTER TABLE old_Orders RENAME TO Orders")
            cursor.execute("DROP TABLE Order_items")
            cursor.execute("ALTER TABLE old_Order_items RENAME TO Order_items")
            connection.commit()
        
        elif scenario == "User":
            cursor.execute('DROP INDEX idx_customers_customer_postal_code')
            cursor.execute('DROP INDEX idx_order_items_order_id')
            connection.commit()
        connection.close()

################################################################################
# Plot the results
species = (
    "SmallDB",
    "MediumDB",
    "LargeDB",
)
weight_counts = {
    "Uninformed": results.get("Uninformed"),
    "Self-Optimized": results.get("Self"),
    "User-Optimized": results.get("User")
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    print(boolean, weight_count)
    p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Query 1 (Runtime in ms)")
ax.legend(loc="upper left")

plt.savefig("Q1A3chart.png")
#################################################################################
