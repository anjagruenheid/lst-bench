DELETE FROM ${catalog}.${database}.web_returns
WHERE wr_item_sk = ${wr_item_sk} AND wr_order_number = ${wr_order_number};
