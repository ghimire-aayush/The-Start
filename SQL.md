# SQL Exercises - DVD Rental Database

After taking the Database course, I decided to apply some of the concepts I learned, particularly on the practical side. This exercise showcases my current familiarity with PostgreSQL query formulation. While this is not a full-fledged project, it demonstrates basic proficiency in data loading and formulating simple SQL queries.

## Dataset Information

The dataset used is called **dvdrental**, downloaded from the following link:
[PostgreSQL Sample Database](https://neon.tech/postgresql/postgresql-getting-started/postgresql-sample-database)

The DVD rental database models the business processes of a DVD rental store. It contains 15 tables:

- **actor** – Stores actor data including first and last names.
- **film** – Stores film data such as title, release year, length, rating, etc.
- **film_actor** – Stores the relationships between films and actors.
- **category** – Stores film categories data.
- **film_category** – Stores the relationships between films and categories.
- **store** – Contains store data, including manager staff and address.
- **inventory** – Stores inventory data.
- **rental** – Stores rental data.
- **payment** – Stores customer payments.
- **staff** – Stores staff data.
- **customer** – Stores customer data.
- **address** – Stores address data for staff and customers.
- **city** – Stores city names.
- **country** – Stores country names.

---

## Part I: Using GROUP BY and Grouping Sets

### Query 1: Customers Spending More than 190.00
Find the customer IDs who spent a total amount greater than 190.00:
```sql
SELECT customer_id
FROM payment
GROUP BY customer_id
HAVING SUM(amount) > 190.00;

```

### Query 2: Customers Spending Less than 3.00 on Average
Find customers' full names who spent an average amount less than 3.00:
```sql
SELECT c.first_name, c.last_name
FROM payment AS p
JOIN customer AS c
ON p.customer_id = c.customer_id
GROUP BY p.customer_id, c.first_name, c.last_name
HAVING AVG(p.amount) < 3.00;

```

### Query 3: Customers with Total Payments
Find customer IDs whose total amount is more than 200.00 or less than 40.00:
```sql
SELECT customer_id
FROM payment
GROUP BY customer_id
HAVING SUM(amount) > 200.00 OR SUM(amount) < 40.00;

```

### Query 4: Customers with Conditional Payment Records
Find customers' IDs who spent more than 90.00 but have fewer than 20 payment records:
```sql
SELECT customer_id
FROM payment
GROUP BY customer_id
HAVING SUM(amount) > 90.00 AND COUNT(amount) < 20;

```

### Query 5: Sum of Payments by Customer and Staff
Using the payment table, return the sum of amounts grouped by customer_id and staff_id:
```sql
SELECT customer_id, staff_id, SUM(amount)
FROM payment
GROUP BY GOUPING SETS ((customer_id), (staff_id), (customer_id, staff_id), ());

```

### Query 6: Top 10 Customers by Total Payments
Find the first 10 customer IDs whose total payments exceed the average total payment:
```sql
SELECT customer_id
FROM payment
GROUP BY customer_id
HAVING SUM(amount) > (
    SELECT AVG(total_amount)
    FROM (
        SELECT SUM(amount) AS total_amount
        FROM payment
        GROUP BY customer_id
    )
)
ORDER BY SUM(amount) DESC
LIMIT 10;

```

---

## Part II: Subqueries and Common Table Expressions (CTEs)

### Query 1: Films with Maximum Length per Category
For each category, find films with lengths greater than or equal to the maximum length of that category:
```sql
SELECT title, length
FROM film
WHERE length >= (
    SELECT MIN(max_length)
    FROM (
        SELECT MAX(length) AS max_length
        FROM film
        INNER JOIN film_category USING(film_id)
        GROUP BY category_id
    )
)
LIMIT 10;

```

### Query 2: Customers from Specific Countries
Use a CTE to select first_name, last_name, city, and country of customers from "Finland" or "Sweden":
```sql
WITH ctl AS (
    SELECT 
        cu.first_name,
        cu.last_name,
        ci.city,
        co.country
    FROM 
        CUSTOMER AS cu
    JOIN 
        ADDRESS AS a ON cu.address_id = a.address_id
    JOIN 
        CITY AS ci ON a.city_id = ci.city_id
    JOIN 
        COUNTRY AS co ON ci.country_id = co.country_id
)
SELECT *
FROM ctl
WHERE country = 'Finland' OR country = 'Sweden';
```

### Query 3: Grouping Sets with Language and Country
Define two CTEs:
1. A table showing customer_id and the language name of their rented DVDs.
2. A table showing customer_id and their country.

Use these tables to count the total number of customers grouped by language name and country:
```sql
WITH CustomerLanguages AS (
    SELECT 
        p.customer_id, 
        l.name AS language_name 
    FROM 
        rental AS r 
    JOIN 
        inventory AS i ON r.inventory_id = i.inventory_id 
    JOIN 
        film AS f ON i.film_id = f.film_id 
    JOIN 
        language AS l ON f.language_id = l.language_id 
    JOIN 
        payment AS p ON r.rental_id = p.rental_id
),
CustomerCountries AS (
    SELECT 
        c.customer_id, 
        co.country 
    FROM 
        customer AS c 
    JOIN 
        address AS a ON c.address_id = a.address_id 
    JOIN 
        city AS ci ON a.city_id = ci.city_id 
    JOIN 
        country AS co ON ci.country_id = co.country_id 
)

SELECT 
    COUNT(DISTINCT cl.customer_id) AS total_customers, 
    cl.language_name, 
    cc.country
FROM 
    CustomerLanguages AS cl 
FULL OUTER JOIN 
    CustomerCountries AS cc ON cl.customer_id = cc.customer_id
GROUP BY 
    GROUPING SETS (
        (cl.language_name, cc.country),  
        (cl.language_name),               
        (cc.country),                     
        ()  
    );
```

---

## Notes
- This project is intended as a learning exercise.
- All queries were tested on the **dvdrental** database.
