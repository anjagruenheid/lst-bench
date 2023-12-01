DELETE FROM ${catalog}.${database}.catalog_sales
WHERE cs_item_sk = ${cs_item_sk} AND cs_order_number = ${cs_order_number};
