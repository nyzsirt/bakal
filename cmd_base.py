#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.sql import text
engine = create_engine('postgresql://app:112233@192.168.0.24:5432/temp')
with engine.connect() as conn:
    s = text("""
    CREATE TABLE weather (
    city            varchar(80),
    temp_lo         int,           -- low temperature
    temp_hi         int,           -- high temperature
    prcp            real,          -- precipitation
    date            date
    );
    """)
    conn.execute(s)
