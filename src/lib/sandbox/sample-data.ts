/**
 * Sample SQL data for the in-browser SQLite sandbox.
 *
 * These schemas match the tables referenced across the course notes
 * (fact_rental, dim_staff, dim_customer, employees, orders, etc.) so
 * that the query examples in the notes produce meaningful results.
 *
 * All statements are plain SQLite (no PostgreSQL-only syntax).
 */
export const SETUP_SQL = `
-- Employees (referenced in 32-query-performance-and-advanced-sql)
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    salary REAL
);
INSERT INTO employees VALUES
    (123, 'Alice',   'Chen',      'Engineering', 95000),
    (124, 'Bob',     'Martinez',  'Engineering', 88000),
    (125, 'Carol',   'Johnson',   'Sales',       72000),
    (126, 'Diego',   'Silva',     'Sales',       68000),
    (127, 'Emma',    'Williams',  'Marketing',   80000),
    (128, 'Frank',   'Nakamura',  'Engineering', 102000),
    (129, 'Grace',   'Kim',       'Marketing',   75000),
    (130, 'Hassan',  'Ali',       'Finance',     90000);

-- Staff dimension
CREATE TABLE dim_staff (
    staff_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
);
INSERT INTO dim_staff VALUES
    (1, 'Maria',  'Gonzalez'),
    (2, 'James',  'O''Brien'),
    (3, 'Priya',  'Patel'),
    (4, 'Liam',   'Walker');

-- Customer dimension
CREATE TABLE dim_customer (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    country TEXT,
    email TEXT
);
INSERT INTO dim_customer VALUES
    (1, 'John',      'Smith',     'United States', 'john@example.com'),
    (2, 'Jane',      'Doe',       'Canada',        'jane@example.com'),
    (3, 'Wei',       'Zhang',     'China',         'wei@example.com'),
    (4, 'Olivia',    'Brown',     'United States', 'olivia@example.com'),
    (5, 'Mateo',     'Rossi',     'Italy',         'mateo@example.com'),
    (6, 'Sofia',     'Lopez',     'Mexico',        'sofia@example.com'),
    (7, 'Arjun',     'Sharma',    'India',         'arjun@example.com'),
    (8, 'Yuki',      'Tanaka',    'Japan',         'yuki@example.com');

-- Film dimension
CREATE TABLE dim_film (
    film_id INTEGER PRIMARY KEY,
    title TEXT,
    length INTEGER,
    rating TEXT
);
INSERT INTO dim_film VALUES
    (1, 'The Data Engineer',  118, 'PG'),
    (2, 'Shards of Glory',    142, 'PG-13'),
    (3, 'Lakehouse Lovers',    95, 'PG'),
    (4, 'Streaming in Seattle',101, 'R'),
    (5, 'Normal Forms',       128, 'PG-13'),
    (6, 'The Warehouse',      155, 'R'),
    (7, 'A Short Scan',        78, 'G');

-- Category dimension
CREATE TABLE dim_category (
    category_id INTEGER PRIMARY KEY,
    film_id INTEGER,
    name TEXT
);
INSERT INTO dim_category VALUES
    (1, 1, 'Drama'),
    (2, 2, 'Action'),
    (3, 3, 'Romance'),
    (4, 4, 'Thriller'),
    (5, 5, 'Drama'),
    (6, 6, 'Drama'),
    (7, 7, 'Comedy');

-- Rental fact table
CREATE TABLE fact_rental (
    rental_id INTEGER PRIMARY KEY,
    staff_id INTEGER,
    customer_id INTEGER,
    film_id INTEGER,
    rental_date TEXT,
    return_date TEXT,
    payment_date TEXT
);
INSERT INTO fact_rental VALUES
    (100, 1, 1, 1, '2005-05-25', '2005-05-28', '2005-05-27'),
    (101, 2, 2, 2, '2005-06-01', '2005-06-05', '2005-06-06'),
    (102, 1, 3, 3, '2005-06-10', '2005-06-13', '2005-06-12'),
    (103, 3, 1, 4, '2005-06-15', '2005-06-18', '2005-06-19'),
    (104, 2, 4, 5, '2005-07-01', '2005-07-04', '2005-07-03'),
    (105, 4, 5, 6, '2005-07-10', '2005-07-13', '2005-07-14'),
    (106, 1, 2, 7, '2005-07-15', '2005-07-17', '2005-07-16'),
    (107, 3, 6, 1, '2005-07-20', '2005-07-24', '2005-07-23'),
    (108, 2, 7, 2, '2005-07-25', '2005-07-28', '2005-07-27'),
    (109, 4, 8, 3, '2005-07-26', '2005-07-29', '2005-07-30');

-- Orders table (used in 33-joins-aggregations and 34-pyspark-sql)
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    price REAL,
    quantity INTEGER,
    order_date TEXT,
    country TEXT,
    stock_code TEXT
);
INSERT INTO orders VALUES
    (1, 1, 49.99,  2, '2024-01-10', 'United States', 'SKU-001'),
    (2, 2, 12.50,  5, '2024-01-11', 'Canada',        'SKU-002'),
    (3, 1, 199.00, 1, '2024-01-15', 'United States', 'SKU-003'),
    (4, 3, 29.99,  3, '2024-02-01', 'China',         'SKU-001'),
    (5, 4, 9.50,   10,'2024-02-14', 'United States', 'SKU-004'),
    (6, 5, 150.00, 1, '2024-02-20', 'Italy',         'SKU-003'),
    (7, 2, 75.00,  2, '2024-03-05', 'Canada',        'SKU-002'),
    (8, 6, 15.00,  4, '2024-03-10', 'Mexico',        'SKU-005'),
    (9, 7, 249.99, 1, '2024-03-22', 'India',         'SKU-006'),
    (10,8, 19.99,  6, '2024-04-02', 'Japan',         'SKU-001');

-- Items (referenced in 34-pyspark-sql)
CREATE TABLE items (
    sku TEXT PRIMARY KEY,
    name TEXT,
    price REAL,
    category TEXT
);
INSERT INTO items VALUES
    ('SKU-001', 'Wireless Mouse',     24.99, 'Electronics'),
    ('SKU-002', 'USB-C Cable',         9.99, 'Electronics'),
    ('SKU-003', 'Mechanical Keyboard',149.00,'Electronics'),
    ('SKU-004', 'Notebook',            4.99, 'Stationery'),
    ('SKU-005', 'Gel Pens (Pack)',     7.50, 'Stationery'),
    ('SKU-006', 'Standing Desk',     199.99, 'Furniture');

-- Order items (referenced in 13-dimensional-modeling)
CREATE TABLE order_items (
    order_id INTEGER,
    item_sku TEXT,
    quantity INTEGER,
    price REAL
);
INSERT INTO order_items VALUES
    (1, 'SKU-001', 2, 24.99),
    (2, 'SKU-002', 5, 9.99),
    (3, 'SKU-003', 1, 149.00),
    (4, 'SKU-001', 3, 24.99),
    (5, 'SKU-004', 10, 4.99),
    (6, 'SKU-003', 1, 149.00),
    (7, 'SKU-002', 2, 9.99);

-- Payment (referenced in 32-query-performance)
CREATE TABLE payment (
    payment_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    rental_id INTEGER,
    amount REAL,
    payment_date TEXT
);
INSERT INTO payment VALUES
    (1, 1, 100, 4.99, '2005-05-27'),
    (2, 2, 101, 5.99, '2005-06-06'),
    (3, 3, 102, 4.99, '2005-06-12'),
    (4, 1, 103, 3.99, '2005-06-19'),
    (5, 4, 104, 5.99, '2005-07-03'),
    (6, 5, 105, 6.99, '2005-07-14'),
    (7, 2, 106, 2.99, '2005-07-16'),
    (8, 6, 107, 4.99, '2005-07-23'),
    (9, 7, 108, 5.99, '2005-07-27'),
    (10,8, 109, 4.99, '2005-07-30');

-- Stores (referenced in 13-dimensional-modeling)
CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    name TEXT,
    location TEXT
);
INSERT INTO stores VALUES
    (1, 'Downtown',   'New York'),
    (2, 'Westside',   'Los Angeles'),
    (3, 'Uptown',     'Chicago'),
    (4, 'Harbor',     'Seattle');

-- Customers (referenced in 34-pyspark-sql)
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    country TEXT
);
INSERT INTO customers
    SELECT customer_id, first_name || ' ' || last_name, email, country
    FROM dim_customer;

-- Order details (referenced in 32-query-performance)
CREATE TABLE orderdetails (
    order_id INTEGER,
    product_id TEXT,
    quantity INTEGER,
    price REAL
);
INSERT INTO orderdetails SELECT order_id, item_sku, quantity, price FROM order_items;

-- Generic my_table (referenced in 13-storage-in-databases)
CREATE TABLE my_table (
    id INTEGER PRIMARY KEY,
    price REAL,
    name TEXT
);
INSERT INTO my_table VALUES
    (1, 10.00, 'Item A'),
    (2, 25.50, 'Item B'),
    (3, 7.99,  'Item C'),
    (4, 99.00, 'Item D');

-- Fact orders (referenced in 41-serving-data-and-analytics)
CREATE TABLE fact_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id TEXT,
    quantity INTEGER,
    amount REAL,
    order_date TEXT
);
INSERT INTO fact_orders
    SELECT order_id, customer_id, stock_code, quantity, price * quantity, order_date
    FROM orders;
`;

/**
 * Short human-readable summary shown when the SQL sandbox first initializes,
 * so users know what tables are available.
 */
export const SAMPLE_DATA_SUMMARY = [
  "employees (8 rows)",
  "dim_staff (4 rows), dim_customer (8 rows), dim_film (7 rows), dim_category (7 rows)",
  "fact_rental (10 rows), payment (10 rows)",
  "orders (10 rows), order_items (7 rows), items (6 rows), orderdetails (7 rows)",
  "customers (8 rows), stores (4 rows), fact_orders (10 rows), my_table (4 rows)",
].join("\n");
