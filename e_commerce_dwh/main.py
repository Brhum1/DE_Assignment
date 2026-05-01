import sqlite3
import kagglehub
import os
from sqlalchemy import create_engine, text
from src.transform import build_dim_product, generate_dim_date, build_dim_customer, build_fact_order_items, build_fact_payments, build_fact_reviews

def run_pipeline():
    print("1. Downloading Source Data...")
    path = kagglehub.dataset_download("terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database")
    source_db_path = os.path.join(path, "olist.sqlite") 
    
    target_db_url = 'postgresql://postgres:123@localhost:5432/olist_dwh'
    target_engine = create_engine(target_db_url)
    
    print("2. Starting ETL Process...")
    
    try:
        source_conn = sqlite3.connect(source_db_path)
        
        print("Building Dimensions...")
        dim_product = build_dim_product(source_conn)
        dim_customer = build_dim_customer(source_conn)
        dim_date = generate_dim_date('2016-09-01', '2018-10-31') 
        

        print("Building Fact Tables...")
        fact_order_items = build_fact_order_items(source_conn, dim_product, dim_customer)
        fact_payments = build_fact_payments(source_conn, dim_customer)
        fact_reviews = build_fact_reviews(source_conn, dim_customer)
        
        print("Loading data into PostgreSQL DWH...")
        
        # Create Tables with explicit constraints from the SQL file
        with target_engine.connect() as conn:
            with open('sql/dwh_schema.sql', 'r') as file:
                conn.execute(text(file.read()))
            conn.commit()

        # Append data to the created tables
        dim_product.to_sql('dim_product', target_engine, if_exists='append', index=False)
        dim_customer.to_sql('dim_customer', target_engine, if_exists='append', index=False)
        dim_date.to_sql('dim_date', target_engine, if_exists='append', index=False)
        fact_order_items.to_sql('fact_order_items', target_engine, if_exists='append', index=False)
        fact_payments.to_sql('fact_payments', target_engine, if_exists='append', index=False)
        fact_reviews.to_sql('fact_reviews', target_engine, if_exists='append', index=False)
        
        print("ETL Pipeline completed successfully! ALL Data loaded into PostgreSQL.")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
    finally:
        if 'source_conn' in locals():
            source_conn.close()
        target_engine.dispose()

if __name__ == "__main__":
    run_pipeline()