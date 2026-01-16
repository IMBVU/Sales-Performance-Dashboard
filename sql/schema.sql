-- Optional: minimal table for Superstore cleaned data
DROP TABLE IF EXISTS fact_orders;

CREATE TABLE fact_orders (
  order_id TEXT,
  order_date TEXT,
  ship_date TEXT,
  region TEXT,
  state TEXT,
  segment TEXT,
  category TEXT,
  sub_category TEXT,
  sales REAL,
  profit REAL,
  discount REAL,
  quantity INTEGER
);
