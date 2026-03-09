from flask import g
import sqlite3 as sql

def get_db(db) -> sql.Connection:
    if 'db' not in g:
        g.db = sql.connect(db)
        g.db.row_factory = sql.Row #Access through row name
        
    return g.db

def init_db(db_path, query):
    db = get_db(db_path)
    db.execute(query)
    db.commit()