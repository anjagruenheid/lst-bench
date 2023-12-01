DELETE FROM ${catalog}.${database}.web_sales
WHERE ws_item_sk = ${ws_item_sk} AND ws_order_number = ${ws_order_number};
