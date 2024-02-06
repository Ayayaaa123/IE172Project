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
'''
def getdblocation():
    db = psycopg2.connect(
        host='localhost',
        database='vetmed12',
        user='postgres',
        port=5432,
        password='colline'
    )
    return db
'''
def getdblocation():
    db = psycopg2.connect(
        host='localhost',
        database='vetmed42',
        user='postgres',
        port=5432,
        password='sabinobacay080901'
    )
    return db

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




sql = """
    select max(visit_id)
    from visit
    """
values = []
df = querydatafromdatabase(sql,values)
visit_id = int(df.loc[0,0])

sql = """
    select patient_id, visit_date
    from visit
    where visit_id = %s
    """
values = [visit_id]
col = ['patient_id', 'visit_date']
df = querydatafromdatabase(sql, values, col)
patient_id = int(df['patient_id'][0])
visit_date = df['visit_date'][0]

print(visit_id)
print(patient_id)
print(visit_date)

sql = """
    select problem_id
    from visit
    where visit_id = %s
    """
values = [visit_id]
df = querydatafromdatabase(sql, values)
problem_id = df.loc[0][0]
if problem_id == None:
    problem_id = 0
else:
    problem_id = int(problem_id)
print(problem_id)

sql = """
    select note_have_been_tested
    from note
    where problem_id = %s
    """
values = [2]
cols = ['result_id']
df = querydatafromdatabase(sql, values, cols)
for result in df['result_id']:
    if result:
        print("Yas")
    else:
        print('Naur')