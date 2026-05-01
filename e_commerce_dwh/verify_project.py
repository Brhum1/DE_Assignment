import pandas as pd
from sqlalchemy import create_engine, inspect

engine = create_engine("postgresql://postgres:123@localhost:5432/olist_dwh")

def verify():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("--- Project Verification Status ---")
    expected_tables = ['dim_product', 'dim_customer', 'dim_date', 'fact_order_items']
    
    for table in expected_tables:
        if table in tables:
            count = pd.read_sql(f"SELECT COUNT(*) FROM {table}", engine).iloc[0,0]
            print(f"✅ Table '{table}': FOUND ({count} rows)")
        else:
            print(f"❌ Table '{table}': NOT FOUND")

if __name__ == "__main__":
    verify()