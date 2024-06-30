import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Database connection parameters
host = 'localhost'
dbname = 'Music_Database'
user = 'postgres'
password = 'ABCD'  # Replace with your actual password
port = '5432'

# Function to execute a query and return a DataFrame
def execute_query(query):
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        print("Connection successful")
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

# Query 1: Countries with the Most Invoices
query1 = """
SELECT billing_country, COUNT(*) AS total_invoices
FROM invoice
GROUP BY billing_country
ORDER BY total_invoices DESC
"""
df1 = execute_query(query1)
if df1 is not None:
    df1.plot(kind='bar', x='billing_country', y='total_invoices')
    plt.title('Total Invoices by Country')
    plt.xlabel('Country')
    plt.ylabel('Total Invoices')
    plt.show()

# Query 2: Top 3 Values of Total Invoice
query2 = """
SELECT total
FROM invoice
ORDER BY total DESC
LIMIT 3
"""
df2 = execute_query(query2)
if df2 is not None:
    df2.plot(kind='bar', y='total', legend=False)
    plt.title('Top 3 Invoice Totals')
    plt.xlabel('Invoice Rank')
    plt.ylabel('Total Amount')
    plt.show()

# Query 3: City with the Best Customers (Highest Sum of Invoice Totals)
query3 = """
SELECT billing_city, SUM(total) AS invoice_total
FROM invoice
GROUP BY billing_city
ORDER BY invoice_total DESC
LIMIT 1
"""
df3 = execute_query(query3)
if df3 is not None:
    df3.plot(kind='bar', x='billing_city', y='invoice_total', legend=False)
    plt.title('City with the Best Customers')
    plt.xlabel('City')
    plt.ylabel('Total Invoice Amount')
    plt.show()

# Query 4: Best Customer (Highest Total Spending)
query4 = """
SELECT customer.customer_id, first_name, last_name, SUM(total) AS total_spending
FROM customer
JOIN invoice ON customer.customer_id = invoice.customer_id
GROUP BY customer.customer_id, first_name, last_name
ORDER BY total_spending DESC
LIMIT 1
"""
df4 = execute_query(query4)
if df4 is not None:
    df4.plot(kind='bar', x='customer_id', y='total_spending', legend=False)
    plt.title('Best Customer by Total Spending')
    plt.xlabel('Customer ID')
    plt.ylabel('Total Spending')
    plt.show()

# Query 5: Rock Music Listeners
query5 = """
SELECT DISTINCT email, first_name, last_name, genre.name AS genre
FROM customer
JOIN invoice ON customer.customer_id = invoice.customer_id
JOIN invoiceline ON invoice.invoice_id = invoiceline.invoice_id
JOIN track ON track.track_id = invoiceline.track_id
JOIN genre ON genre.genre_id = track.genre_id
WHERE genre.name LIKE 'Rock'
ORDER BY email
"""
df5 = execute_query(query5)
if df5 is not None:
    print(df5)  # Just print this dataframe since it's a list of customers

# Query 6: Top 10 Rock Bands by Track Count
query6 = """
SELECT artist.artist_id, artist.name, COUNT(artist.artist_id) AS number_of_songs
FROM track
JOIN album ON album.album_id = track.album_id
JOIN artist ON artist.artist_id = album.artist_id
JOIN genre ON genre.genre_id = track.genre_id
WHERE genre.name LIKE 'Rock'
GROUP BY artist.artist_id, artist.name
ORDER BY number_of_songs DESC
LIMIT 10
"""
df6 = execute_query(query6)
if df6 is not None:
    df6.plot(kind='bar', x='name', y='number_of_songs')
    plt.title('Top 10 Rock Bands by Track Count')
    plt.xlabel('Artist')
    plt.ylabel('Number of Songs')
    plt.show()

# Query 7: Tracks Longer than Average Length
query7 = """
SELECT name, milliseconds
FROM track
WHERE milliseconds > (
    SELECT AVG(milliseconds)
    FROM track
)
ORDER BY milliseconds DESC
"""
df7 = execute_query(query7)
if df7 is not None:
    df7.plot(kind='bar', x='name', y='milliseconds')
    plt.title('Tracks Longer than Average Length')
    plt.xlabel('Track Name')
    plt.ylabel('Milliseconds')
    plt.show()

# Query 8: Amount Spent by Each Customer on Artists
query8 = """
WITH best_selling_artist AS (
    SELECT artist.artist_id AS artist_id, artist.name AS artist_name, SUM(invoice_line.unit_price*invoice_line.quantity) AS total_sales
    FROM invoice_line
    JOIN track ON track.track_id = invoice_line.track_id
    JOIN album ON album.album_id = track.album_id
    JOIN artist ON artist.artist_id = album.artist_id
    GROUP BY 1, artist.artist_id, artist.name
    ORDER BY 3 DESC
    LIMIT 1
)
SELECT c.customer_id, c.first_name, c.last_name, bsa.artist_name, SUM(il.unit_price*il.quantity) AS amount_spent
FROM invoice i
JOIN customer c ON c.customer_id = i.customer_id
JOIN invoice_line il ON il.invoice_id = i.invoice_id
JOIN track t ON t.track_id = il.track_id
JOIN album alb ON alb.album_id = t.album_id
JOIN best_selling_artist bsa ON bsa.artist_id = alb.artist_id
GROUP BY c.customer_id, c.first_name, c.last_name, bsa.artist_name
ORDER BY 5 DESC
"""
df8 = execute_query(query8)
if df8 is not None:
    df8.plot(kind='bar', x='customer_id', y='amount_spent')
    plt.title('Amount Spent by Each Customer on Artists')
    plt.xlabel('Customer ID')
    plt.ylabel('Amount Spent')
    plt.show()

# Query 9: Most Popular Music Genre for Each Country
query9 = """
WITH popular_genre AS (
    SELECT COUNT(invoice_line.quantity) AS purchases, customer.country, genre.name, genre.genre_id, 
    ROW_NUMBER() OVER(PARTITION BY customer.country ORDER BY COUNT(invoice_line.quantity) DESC) AS RowNo 
    FROM invoice_line 
    JOIN invoice ON invoice.invoice_id = invoice_line.invoice_id
    JOIN customer ON customer.customer_id = invoice.customer_id
    JOIN track ON track.track_id = invoice_line.track_id
    JOIN genre ON genre.genre_id = track.genre_id
    GROUP BY customer.country, genre.name, genre.genre_id
)
SELECT * FROM popular_genre WHERE RowNo <= 1
"""
df9 = execute_query(query9)
if df9 is not None:
    df9.plot(kind='bar', x='country', y='purchases')
    plt.title('Most Popular Music Genre for Each Country')
    plt.xlabel('Country')
    plt.ylabel('Purchases')
    plt.show()

# Query 10: Customer Spending by Country
query10 = """
WITH customer_spending AS (
    SELECT customer.customer_id, customer.first_name, customer.last_name, invoice.billing_country, SUM(invoice.total) AS total_spent,
    ROW_NUMBER() OVER(PARTITION BY invoice.billing_country ORDER BY SUM(invoice.total) DESC) AS row_number
    FROM invoice
    JOIN customer ON customer.customer_id = invoice.customer_id
    GROUP BY customer.customer_id, customer.first_name, customer.last_name, invoice.billing_country
)
SELECT * FROM customer_spending WHERE row_number = 1
"""
df10 = execute_query(query10)
if df10 is not None:
    df10.plot(kind='bar', x='billing_country', y='total_spent')
    plt.title('Top Customer Spending by Country')
    plt.xlabel('Country')
    plt.ylabel('Total Spent')
    plt.show()

