from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import os
import numpy as np

# initialize Connector object
connector = Connector()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ghela\Documents\Hackathon-SQUARE\Scripts\winged-scout-401122-ae11907f66c0.json"

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "winged-scout-401122:europe-west2:team-elk-sql",
        "pymysql",
        user="root",
        password="",
        db="team-elk-db"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

data_array = None
with pool.connect() as db_conn:
    result = db_conn.execute(sqlalchemy.text("SELECT Keyword,text_embedding FROM Keywords WHERE Keyword_ID = 1;")).fetchall()
    # db_conn.execute(sqlalchemy.text("SELECT count(*) FROM Keywords;"))
    
    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    db_conn.commit()

    # Do something with the results
    for row in result:
        print(row)

    # Store the results into a numpy array
    # data_array = np.array(result)
        
connector.close()