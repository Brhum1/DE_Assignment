import pandas as pd

def build_dim_product(source_conn) -> pd.DataFrame:
    """
    استخراج وتحويل بيانات المنتجات لبناء بُعد المنتج (Dim_Product).
    """
    query_products = "SELECT * FROM products;"
    query_translation = "SELECT * FROM product_category_name_translation;"
    
    df_products = pd.read_sql(query_products, source_conn)
    df_translation = pd.read_sql(query_translation, source_conn)
    
    dim_product = pd.merge(
        df_products, 
        df_translation, 
        on='product_category_name', 
        how='left'
    )
    
    dim_product['product_category_name_english'] = dim_product['product_category_name_english'].fillna('Unknown')
    
    numeric_columns = ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
    dim_product[numeric_columns] = dim_product[numeric_columns].fillna(0)
    
    columns_to_keep = [
        'product_id', 'product_category_name_english', 'product_weight_g', 
        'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    dim_product = dim_product[columns_to_keep]
    
    dim_product.rename(columns={'product_category_name_english': 'category_name_english'}, inplace=True)
    dim_product.insert(0, 'Product_Key', range(1, 1 + len(dim_product)))
    
    return dim_product

def generate_dim_date(start_date: str, end_date: str) -> pd.DataFrame:

    date_range = pd.date_range(start=start_date, end=end_date)
    dim_date = pd.DataFrame({'full_date': date_range})
    
    dim_date['Date_Key'] = dim_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['quarter'] = dim_date['full_date'].dt.quarter
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['day_of_week'] = dim_date['full_date'].dt.dayofweek
    dim_date['is_weekend'] = dim_date['day_of_week'].isin([5, 6])
    
    cols = ['Date_Key', 'full_date', 'year', 'quarter', 'month', 'day_of_week', 'is_weekend']
    return dim_date[cols]

def build_dim_customer(source_conn) -> pd.DataFrame:
    """
    بناء بُعد العميل.
    """
    df_customers = pd.read_sql("SELECT * FROM customers;", source_conn)
    

    columns_to_keep = ['customer_id', 'customer_unique_id', 'customer_city', 'customer_state']
    dim_customer = df_customers[columns_to_keep].copy()
    
    dim_customer.insert(0, 'Customer_Key', range(1, 1 + len(dim_customer)))
    
    return dim_customer

def build_fact_order_items(source_conn, dim_product, dim_customer) -> pd.DataFrame:
    """
    بناء جدول الحقائق الرئيسي (المبيعات).
    """
    df_orders = pd.read_sql("SELECT order_id, customer_id, order_purchase_timestamp FROM orders;", source_conn)
    df_items = pd.read_sql("SELECT order_id, product_id, price, freight_value FROM order_items;", source_conn)
    
    fact = pd.merge(df_items, df_orders, on='order_id', how='inner')
    

    fact = pd.merge(fact, dim_product[['product_id', 'Product_Key']], on='product_id', how='left')
    
    fact = pd.merge(fact, dim_customer[['customer_id', 'Customer_Key']], on='customer_id', how='left')
    
    fact['order_purchase_timestamp'] = pd.to_datetime(fact['order_purchase_timestamp'])
    fact['Order_Date_Key'] = fact['order_purchase_timestamp'].dt.strftime('%Y%m%d').astype(int)
    
    fact.dropna(subset=['Product_Key', 'Customer_Key'], inplace=True)
    fact['Product_Key'] = fact['Product_Key'].astype(int)
    fact['Customer_Key'] = fact['Customer_Key'].astype(int)
    
    columns_to_keep = ['order_id', 'Product_Key', 'Customer_Key', 'Order_Date_Key', 'price', 'freight_value']
    fact = fact[columns_to_keep]
    
    fact.insert(0, 'Order_Item_Key', range(1, 1 + len(fact)))
    
    return fact

def build_fact_payments(source_conn, dim_customer) -> pd.DataFrame:
    """
    بناء جدول الحقائق للمدفوعات.
    """
    df_orders = pd.read_sql("SELECT order_id, customer_id, order_purchase_timestamp FROM orders;", source_conn)
    df_payments = pd.read_sql("SELECT order_id, payment_sequential, payment_type, payment_installments, payment_value FROM order_payments;", source_conn)
    
    fact = pd.merge(df_payments, df_orders, on='order_id', how='inner')
    fact = pd.merge(fact, dim_customer[['customer_id', 'Customer_Key']], on='customer_id', how='left')
    
    fact['order_purchase_timestamp'] = pd.to_datetime(fact['order_purchase_timestamp'])
    fact['Payment_Date_Key'] = fact['order_purchase_timestamp'].dt.strftime('%Y%m%d').astype(int)
    
    fact.dropna(subset=['Customer_Key'], inplace=True)
    fact['Customer_Key'] = fact['Customer_Key'].astype(int)
    
    columns_to_keep = ['order_id', 'Customer_Key', 'Payment_Date_Key', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']
    fact = fact[columns_to_keep]
    
    fact.insert(0, 'Payment_Key', range(1, 1 + len(fact)))
    return fact

def build_fact_reviews(source_conn, dim_customer) -> pd.DataFrame:
    """
    بناء جدول الحقائق للتقييمات.
    """
    df_orders = pd.read_sql("SELECT order_id, customer_id FROM orders;", source_conn)
    df_reviews = pd.read_sql("SELECT review_id, order_id, review_score, review_creation_date FROM order_reviews;", source_conn)
    
    fact = pd.merge(df_reviews, df_orders, on='order_id', how='inner')
    fact = pd.merge(fact, dim_customer[['customer_id', 'Customer_Key']], on='customer_id', how='left')
    
    # Handle potentially bad dates
    fact['review_creation_date'] = pd.to_datetime(fact['review_creation_date'], errors='coerce')
    # Fill missing dates with a default or drop (here we drop NaT)
    fact.dropna(subset=['review_creation_date', 'Customer_Key'], inplace=True)
    
    fact['Review_Date_Key'] = fact['review_creation_date'].dt.strftime('%Y%m%d').astype(int)
    
    fact['Customer_Key'] = fact['Customer_Key'].astype(int)
    
    columns_to_keep = ['review_id', 'order_id', 'Customer_Key', 'Review_Date_Key', 'review_score']
    fact = fact[columns_to_keep]
    
    fact.insert(0, 'Review_Key', range(1, 1 + len(fact)))
    return fact