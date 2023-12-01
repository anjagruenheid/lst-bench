DELETE FROM ${catalog}.${database}.store_sales
WHERE ss_item_sk = ${ss_item_sk} AND ss_ticket_number = ${ss_ticket_number};
