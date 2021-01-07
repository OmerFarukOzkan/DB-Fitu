import psycopg2
from psycopg2 import Error

try:

    connection = psycopg2.connect(user="postgres",password = "database1",database="Ömer Faruk Özkan")
    cursor = connection.cursor()
    query='''SELECT * FROM exercise;'''
    cursor.execute(query)
    print(cursor.fetchall())

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)