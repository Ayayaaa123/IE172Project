import psycopg2
import pandas as pd

# Remove comment on your database, comment the rest

# def getdblocation():
#     db = psycopg2.connect(
#         host='localhost',
#         database='IE172Project',
#         user='postgres',
#         port=5433,
#         password='36442901'
#     )
#     return db

# def getdblocation():
#     db = psycopg2.connect(
#         host='localhost',
#         database='IE172Project',
#         user='postgres',
#         port=5432,
#         password='quick126'
#     )
#     return db

def modifydatabase(sql,values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql,values)
    db.commit()
    db.close()

def querydatafromdatabase(sql, values, dfcolumns=None):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    if dfcolumns is None:
        rows = pd.DataFrame(cur.fetchall())
    else:
        rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows
