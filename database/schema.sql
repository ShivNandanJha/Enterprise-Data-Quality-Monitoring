USE enterprise_quality;

drop table if exists bronze_orders;

create table bronze_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,

    Order_ID VARCHAR(50),

    Customer_ID VARCHAR(50),

    Order_Date DATE,

    Year SMALLINT,

    Month TINYINT,

    Day TINYINT,

    Day_Of_Week VARCHAR(20),

    Quarter TINYINT,

    Customer_Age INT,

    Customer_Gender VARCHAR(20),

    Country VARCHAR(100),

    City VARCHAR(100),

    Customer_Segment VARCHAR(100),

    Product_ID VARCHAR(50),

    Product_Category VARCHAR(100),

    Product_Subcategory VARCHAR(100),

    Brand VARCHAR(100),

    Unit_Price DECIMAL(10,2),

    Quantity INT,

    Discount_Percent DECIMAL(5,2),

    Discount_Amount DECIMAL(10,2),

    Coupon_Used VARCHAR(10),

    Shipping_Cost DECIMAL(10,2),

    Tax_Amount DECIMAL(10,2),

    Order_Amount DECIMAL(12,2),

    Payment_Method VARCHAR(50),

    Device_Type VARCHAR(50),

    Traffic_Source VARCHAR(50),

    Membership_Status VARCHAR(50),

    Shipping_Method VARCHAR(50),

    Warehouse_Region VARCHAR(50),

    Delivery_Days INT,

    Order_Status VARCHAR(50),

    Returned VARCHAR(10),

    Review_Rating INT,

    Customer_Lifetime_Value DECIMAL(12,2),

    Profit_Margin_Percent DECIMAL(6,2),

    Profit_Amount DECIMAL(12,2),

    Season VARCHAR(20),

    Holiday_Season VARCHAR(10),

    High_Value_Order VARCHAR(10),

    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
