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

# TODO: Offer regular sync of sales data to the db.


data_array = None
with pool.connect() as db_conn:
    
    # TODO: --------------- TEST NESTED SQL QUERY ----------------------
    # query ="SELECT Item_Name FROM Items WHERE Item_ID = '22BPJ5NDB3J6KRXC3YNAXBEE';"
    item_id = "22BPJ5NDB3J6KRXC3YNAXBEE"
    query =f"SELECT Date, Item, Gross_Sales FROM Item_Sales WHERE Item = (SELECT Item_Name FROM Items WHERE Item_ID = '{item_id}')"
    
    
    # itemName = "AFUNTA Hubsan X4 H107C Quadcopter Black / Red Spare Parts Crash Pack Includes One Body Shell + One HD Camera PCB Module (200W) + One Protection Cover + 4 Rubber Feet + 4 Spare Blades Set (16 pieces) + One Spare 380mA Battery +2pcs Motors + One U Wrench"
    # query = f"SELECT * FROM Items WHERE Item_Name = '{itemName}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    # db_conn.execute(sqlalchemy.text("SELECT count(*) FROM Keywords;"))
    
    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    db_conn.commit()

    # Do something with the results
    
    if not result: print ("No results found")
    
    for row in result:
        print(row)

    # Store the results into a numpy array
    # data_array = np.array(result)
        
connector.close()