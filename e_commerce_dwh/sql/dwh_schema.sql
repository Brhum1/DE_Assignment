DROP TABLE IF EXISTS fact_payments CASCADE;
DROP TABLE IF EXISTS fact_reviews CASCADE;
DROP TABLE IF EXISTS fact_order_items CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;

-- 1. Dimension: Products
CREATE TABLE dim_product (
    "Product_Key" INTEGER PRIMARY KEY,
    product_id TEXT NOT NULL,
    category_name_english TEXT,
    product_weight_g REAL,
    product_length_cm REAL,
    product_height_cm REAL,
    product_width_cm REAL
);

-- 2. Dimension: Customers
CREATE TABLE dim_customer (
    "Customer_Key" INTEGER PRIMARY KEY,
    customer_id TEXT NOT NULL,
    customer_unique_id TEXT NOT NULL,
    customer_city TEXT,
    customer_state TEXT
);

-- 3. Dimension: Date (Generated Dimension)
CREATE TABLE dim_date (
    "Date_Key" INTEGER PRIMARY KEY, -- Format: YYYYMMDD
    full_date DATE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

-- 4. Fact: Order Items (Sales)
CREATE TABLE fact_order_items (
    "Order_Item_Key" INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    "Product_Key" INTEGER,
    "Customer_Key" INTEGER,
    "Order_Date_Key" INTEGER,
    price REAL,
    freight_value REAL,
    FOREIGN KEY ("Product_Key") REFERENCES dim_product("Product_Key"),
    FOREIGN KEY ("Customer_Key") REFERENCES dim_customer("Customer_Key"),
    FOREIGN KEY ("Order_Date_Key") REFERENCES dim_date("Date_Key")
);

-- 5. Fact: Payments
CREATE TABLE fact_payments (
    "Payment_Key" INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    "Customer_Key" INTEGER,
    "Payment_Date_Key" INTEGER,
    payment_sequential INTEGER,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value REAL,
    FOREIGN KEY ("Customer_Key") REFERENCES dim_customer("Customer_Key"),
    FOREIGN KEY ("Payment_Date_Key") REFERENCES dim_date("Date_Key")
);

-- 6. Fact: Reviews
CREATE TABLE fact_reviews (
    "Review_Key" INTEGER PRIMARY KEY,
    review_id TEXT NOT NULL,
    order_id TEXT NOT NULL,
    "Customer_Key" INTEGER,
    "Review_Date_Key" INTEGER,
    review_score INTEGER,
    FOREIGN KEY ("Customer_Key") REFERENCES dim_customer("Customer_Key"),
    FOREIGN KEY ("Review_Date_Key") REFERENCES dim_date("Date_Key")
);

-- تحسين الأداء
-- فهرس لتسريع الاستعلامات الزمنية
CREATE INDEX idx_fact_date ON fact_order_items("Order_Date_Key");

-- فهارس لتسريع عمليات الربط (Joins) مع جداول الأبعاد
CREATE INDEX idx_fact_product ON fact_order_items("Product_Key");
CREATE INDEX idx_fact_customer ON fact_order_items("Customer_Key");

-- فهرس على الفئة لتسريع تقارير المنتجات المحركة للإيرادات
CREATE INDEX idx_dim_product_category ON dim_product(category_name_english);

-- فهارس جدول المدفوعات
CREATE INDEX idx_fact_payments_customer ON fact_payments("Customer_Key");
CREATE INDEX idx_fact_payments_date ON fact_payments("Payment_Date_Key");

-- فهارس جدول التقييمات
CREATE INDEX idx_fact_reviews_customer ON fact_reviews("Customer_Key");
CREATE INDEX idx_fact_reviews_date ON fact_reviews("Review_Date_Key");