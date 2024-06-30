--Q1 . How is the senior most employee based on the job title ?
	Select * from employee
    order by levels desc
	limit 1

--Q2 . which countries have the most invoices?

select count(*) as num ,billing_country
from invoice
group by billing_country
order by num desc 
	
--Q3 . what are the top 3 values of total invoice 

select total from invoice
order by total desc
limit 3
	
--Q4 . Which city has the best customers?We would like to throw promotional music festivals in the city we made the most money . write a query that returns one city that has the highest sum of  invoices total .return both the city name and sum of all inovices totals

SELECT sum(total) as total , billing_city 
FROM invoice
group by billing_city
order by total desc
	
--Q5 . Who is the best customer? the customer who has spend the most money will be declared as a best customer. Write thee query that returns the person who has spend the most of the money ?

select c.customer_id , c.first_name , c.last_name , sum(i.total) as amount
from customer as c 
join invoice as i on c.customer_id = i.customer_id
group by c.customer_id
order by amount desc
limit 1

--Q6 . Q1: Write query to return the email, first name, last name, & Genre of all Rock Music listeners. Return your list ordered alphabetically by email starting with A.

SELECT DISTINCT email AS Email,first_name AS FirstName, last_name AS LastName , genre.name AS Name
FROM customer
JOIN invoice ON invoice.customer_id = customer.customer_id
JOIN invoice_line ON invoice_line.invoice_id = invoice.invoice_id
JOIN track ON track.track_id = invoice_line.track_id
JOIN genre ON genre.genre_id = track.genre_id
WHERE genre.name LIKE 'Rock'
ORDER BY email;


--Q7 . Let's invite the artists who have written the most rock music in our dataset. 
--Write a query that returns the Artist name and total track count of the top 10 rock bands. 