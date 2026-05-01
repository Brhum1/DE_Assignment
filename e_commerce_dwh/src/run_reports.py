import pandas as pd
from sqlalchemy import create_engine

def run_analytical_queries():
    print("--- E-Commerce DWH Reports ---")
    

    engine = create_engine("postgresql://postgres:123@localhost:5432/olist_dwh")
    
    print("\n1. Most Valuable Customers (Top 5):")
    query_customers = """
    SELECT 
        c.customer_unique_id,
        c.customer_city,
        SUM(f.price) AS Lifetime_Value,
        COUNT(f."Order_Item_Key") AS Items_Purchased
    FROM 
        fact_order_items f
    JOIN 
        dim_customer c ON f."Customer_Key" = c."Customer_Key"
    GROUP BY 
        c.customer_unique_id, c.customer_city
    ORDER BY 
        Lifetime_Value DESC
    LIMIT 5;
    """
    df_customers = pd.read_sql(query_customers, engine)
    print(df_customers.to_string(index=False))


    print("\n2. Top Categories Driving Revenue:")
    query_categories = """
    SELECT 
        p.category_name_english,
        SUM(f.price) AS Total_Revenue,
        COUNT(f."Order_Item_Key") AS Units_Sold
    FROM 
        fact_order_items f
    JOIN 
        dim_product p ON f."Product_Key" = p."Product_Key"
    WHERE 
        p.category_name_english != 'Unknown'
    GROUP BY 
        p.category_name_english
    ORDER BY 
        Total_Revenue DESC
    LIMIT 5;
    """
    df_categories = pd.read_sql(query_categories, engine)
    print(df_categories.to_string(index=False))

if __name__ == "__main__":
    run_analytical_queries()