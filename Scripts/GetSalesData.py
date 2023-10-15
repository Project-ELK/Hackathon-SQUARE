from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import os
import numpy as np

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

# TODO: Acquire the Item_IDs for all of the keywords that have a good cosine similarity to the embeddings (new item vs Keyword--> for the item)
# TODO: Acquire the sales data for the specific item ID
def getSalesData(itemID):
    with pool.connect() as db_conn:
        # Query to get sales data for the specific item
        query =f"SELECT Date, Item, Gross_Sales FROM Item_Sales WHERE Item = (SELECT Item_Name FROM Items WHERE Item_ID = '{itemID}')"
        # Executes the query
        result = db_conn.execute(sqlalchemy.text(query)).fetchall()
        # commit transaction to db
        db_conn.commit()
        # If no results are returned...
        if not result: 
            print ("No results found")
            return None
        # Store the results into a numpy array
    connector.close()
    return np.array(result)


# ------------ TEST AREA -----------------

sales_data_for_item = getSalesData('22BPJ5NDB3J6KRXC3YNAXBEE')
for row in sales_data_for_item:
    print (row)


# TODO: Calculate the output based on a weighted formula (use of dates required) --> SALES VOLUME