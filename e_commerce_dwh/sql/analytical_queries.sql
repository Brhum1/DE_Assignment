SELECT 
    d.year,
    d.month,
    SUM(f.price) AS Total_Revenue,
    COUNT(DISTINCT f.order_id) AS Total_Orders
FROM 
    Fact_Order_Items f
JOIN 
    Dim_Date d ON f.Order_Date_Key = d.Date_Key
GROUP BY 
    d.year, d.month
ORDER BY 
    d.year, d.month;

SELECT 
    c.customer_unique_id,
    c.customer_city,
    SUM(f.price + f.freight_value) AS Lifetime_Value,
    COUNT(f.order_id) AS Items_Purchased
FROM 
    Fact_Order_Items f
JOIN 
    Dim_Customer c ON f.Customer_Key = c.Customer_Key
GROUP BY 
    c.customer_unique_id, c.customer_city
ORDER BY 
    Lifetime_Value DESC
LIMIT 10;

SELECT 
    p.category_name_english,
    SUM(f.price) AS Total_Revenue,
    COUNT(f.Order_Item_Key) AS Units_Sold
FROM 
    Fact_Order_Items f
JOIN 
    Dim_Product p ON f.Product_Key = p.Product_Key
WHERE 
    p.category_name_english != 'Unknown'
GROUP BY 
    p.category_name_english
ORDER BY 
    Total_Revenue DESC
LIMIT 5;