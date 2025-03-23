#!/bin/bash
echo "Importing CSV into MySQL..."

mysql -u root -p"$MYSQL_ROOT_PASSWORD" -D $MYSQL_DATABASE -e "
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(100) PRIMARY KEY,
    customer_id VARCHAR(100),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME
);
LOAD DATA INFILE '/var/lib/mysql-files/olist_orders_dataset.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    order_id,
    customer_id,
    order_status,
    @order_purchase_timestamp,
    @order_approved_at,
    @order_delivered_carrier_date,
    @order_delivered_customer_date,
    @order_estimated_delivery_date
)
SET order_purchase_timestamp = NULLIF(@order_purchase_timestamp, '')
    , order_approved_at = NULLIF(@order_approved_at, '')
    , order_delivered_carrier_date = NULLIF(@order_delivered_carrier_date, '')
    , order_delivered_customer_date = NULLIF(@order_delivered_customer_date, '')
    , order_estimated_delivery_date = NULLIF(@order_estimated_delivery_date, '')
;
"

echo "CSV import completed."

