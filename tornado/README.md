Initial goal: See how many requests per second a tornado server can do. 

The service should have to connect to query a database server before generating the response.

Django is used just for creating/populating the database (for consistency).

Open questions:
+ Parameters - The database server should respond fast/slow over the network
+ Parameters - The database server should run a fast/slow query (regardless of network time)
