#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Zella Zhong
Date: 2022-08-26 15:50:06
LastEditors: Zella Zhong
LastEditTime: 2022-08-26 18:34:58
FilePath: /databricks-loader/opensea_dataloader.py
Description: 
'''
import pyodbc


if __name__ == '__main__':
    # Replace <table-name> with the name of the database table to query.
    table_name = "ethereum_opensea.wyvern_exchange_call_owner"

    # Connect to the SQL warehouse by using the
    # Data Source Name (DSN) that you created earlier.
    conn = pyodbc.connect("Driver=/Library/simba/spark/lib/libsparkodbc_sbu.dylib;" +
                        "HOST=dbc-84dcfc53-984e.cloud.databricks.com;" +
                        "PORT=443;" +
                        "Schema=default;" +
                        "SparkServerType=3;" +
                        "AuthMech=3;" +
                        "UID=token;" +
                        "PWD=dapi55a0a9d5fe78e99bac1a9f6b1f357038;" +
                        "ThriftTransport=2;" +
                        "SSL=1;" +
                        "HTTPPath=/sql/1.0/endpoints/8bca9626fdc2d951",
                        autocommit=True)

    # Run a SQL query by using the preceding connection.
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")

    # Print the rows retrieved from the query.
    print(f"Query output: SELECT * FROM {table_name} LIMIT 2\n")
    for row in cursor.fetchall():
        print(row)
