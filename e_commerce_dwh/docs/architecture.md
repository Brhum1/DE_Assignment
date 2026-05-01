# E-Commerce Data Warehouse (Olist Dataset)

## 🎯 Objective

This project implements a production-ready Data Warehouse (DWH) solution for the Olist E-commerce dataset. The goal is to enable scalable, high-performance analytical reporting to answer key business questions regarding sales trends, customer lifetime value, and delivery performance.

## 🧠 1. Architecture & Design Decisions

**Architecture Chosen:** Hybrid (Medallion Concept + Kimball Dimensional Modeling).

* **Why?** I utilized a Python-based ETL pipeline to extract and transform data in memory (acting as Bronze/Silver layers) and loaded the refined data into a PostgreSQL database designed following a **Kimball Bus Architecture (Fact Constellation Schema)**. This architecture is heavily optimized for fast read-heavy analytical queries and perfectly aligns with the requirement to support multiple interconnected business processes.

## 🧩 2. Data Modeling (Kimball Bus Architecture)

The Data Warehouse models three distinct business processes, fulfilling the requirement to handle multiple processes via separate fact tables.

**1. The Sales Process (Fact Table: `fact_order_items`)**
* **Grain:** One row per individual product item within an order.
* **Why this grain?** An order can contain multiple items from different categories or sellers. Tracking metrics at the item level ensures maximum flexibility and prevents data loss or incorrect aggregations when drilling down into product performance.

**2. The Payments Process (Fact Table: `fact_payments`)**
* **Grain:** One row per payment artifact (e.g., credit card installment or voucher) applied to an order.
* **Why?** Customers can pay for a single order using multiple payment methods or installments. This fact table tracks the financial lifecycle of the order.

**3. The Customer Satisfaction Process (Fact Table: `fact_reviews`)**
* **Grain:** One row per customer review.
* **Why?** Tracks post-purchase customer satisfaction through review scores, independent of the actual shipping or payment process.

**Dimension Tables:**

* `dim_product`: Denormalized by joining with the translation table during ETL to provide English category names directly, eliminating the need for complex joins during querying.
* `dim_customer`: Contains geographical data.
* `dim_date`: A generated date dimension to enable robust time-series analysis (e.g., Sales trending over time).

## ⚙️ 3. Engineering: The ETL Pipeline

The pipeline is built using **Python (Pandas)** and **SQLAlchemy**.

* **Reproducibility:** The pipeline automatically downloads the latest SQLite dataset via `kagglehub`, ensuring the process can be run from scratch on any machine.
* **Data Quality Handling:** * Addressed missing values in physical dimensions by filling them with `0`.
  * Filled missing English category translations with `'Unknown'` to ensure no facts are orphaned or dropped during aggregation.
* **Surrogate Keys:** Instead of using long, complex string IDs (`customer_id`, `product_id`), the pipeline generates sequential integer Surrogate Keys (`Customer_Key`, `Product_Key`). This significantly improves database join performance.

## 🚀 4. Performance Optimization

* **Indexing:** PostgreSQL indexes (B-Tree) are applied to all Foreign Keys across all Fact tables (e.g., `Product_Key`, `Customer_Key`, `Order_Date_Key`, `Payment_Date_Key`) to significantly speed up complex join operations across the data warehouse.
* **Engine Choice:** Transitioned from SQLite to **PostgreSQL** to leverage better concurrency, advanced query planning, and readiness for future scaling.

## ⚖️ 5. Trade-offs & Assumptions (Preventing Over-engineering)

* **Batch vs. Streaming:** I chose a Batch ETL approach rather than real-time streaming (e.g., Kafka). E-commerce analytical questions like "sales trends over time" typically require daily or hourly aggregates, making real-time processing an unnecessary overhead.
* **Pandas vs. Spark:** Given the dataset size (~100k rows), Pandas processes the data in-memory within seconds. Introducing Apache Spark would have been severe over-engineering, increasing infrastructure costs and complexity without tangible benefits.
* **Assumption:** Orders without matching products or customers in the dimension tables are considered data anomalies and are dropped during the ETL process to maintain data integrity.
* **Degenerate Dimensions:** Kept operational IDs like `order_id`, `payment_type`, and `review_id` directly inside the Fact Tables (as Degenerate Dimensions) instead of spinning off tiny, unnecessary dimension tables. This prevents schema bloat and speeds up queries.

## 📦 How to Run

1. Ensure PostgreSQL is running and update the connection string in `main.py`.
2. Run `python3 main.py` to execute the ETL pipeline.
3. Run `python3 verify_project.py` to check data integrity.
4. Run `python3 src/run_reports.py` to view business insights.
