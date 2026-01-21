# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 15:45:45 2025

@author: sgarcia
"""

import psycopg2
from sqlalchemy import create_engine

#Connect to Railway DB, change data accordingly. 
conn_low_vol_vol_reversal = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=,
    dbname="",
    user="",
    password=""
)

engine_low_vol_vol_reversal = create_engine("postgresql://user_place_holder:password_place_holder@tramway.proxy.rlwy.net:port_place_holder/dbname", 
                       connect_args = {"sslmode": "require"})
