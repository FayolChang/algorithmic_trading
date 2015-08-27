#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import pandas.io.sql as psql
import MySQLdb as mdb


# Connect to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

# Select all of the historic Google adjusted close data
sql = """SELECT dp.price_date, dp.adj_close_price
         FROM symbol AS sym
         INNER JOIN daily_price AS dp
         ON dp.symbol_id = sym.id
         WHERE sym.ticker = 'GOOG'
         ORDER BY dp.price_date ASC;"""

# Create a pandas dataframe from the SQL query
goog = psql.frame_query(sql, con=con, index_col='price_date')    

# Output the dataframe tail
print goog.tail()
