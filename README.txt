kaneria:Mahekkumar Kaneria   
"I declare that we did not collaborate with anyone outside our own group in this assignment"

In this assignment, we were provided with a database from which we derived three databases
of different sizes in order to benchmark the performance of different queries with and without
indices and different database settings. 

***DISCLAIMER***
->TO RUN THE PYTHON FILE ADD ALL THREE DATABASES IN Group36A3 FOLDER 
	WHERE ALL .PY FILES ARE LOCATED  


Report for indices we created for the “User Optimized” scenarios are as follows:-
For each of the 4 queries, we can create two indices to optimize it. One index can be created on 
the "customer_postal_code" column in the "Customers" table and another on the "order_id" column in 
the "Order_items" table.


The index on the "customer_postal_code" column in the "Customers" table will allow the query to quickly 
filter out the customers with the given postal code. This will reduce the number of records that need to 
be checked in the "Orders" table.


The index on the "order_id" column in the "Order_items" table will speed up the subquery that checks for 
orders with more than one item. The subquery groups the records by order_id and then checks the count, so 
having an index on this column will allow the database to quickly group and count the records.


With these two indices in place, the query will be able to quickly filter and count the records needed, leading 
to better performance.

