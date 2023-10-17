from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import os
import numpy as np
from collections import defaultdict
import datetime

connector = Connector()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd()+"\winged-scout-401122-ae11907f66c0.json"

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

# ------------ HELPER FUNCTIONS -----------------

def is_within_last_6_months(date):
  """Checks if a datetime.date is within the last 6 months of the current date.
  Args:
    date: A datetime.date object.
  Returns:
    True if the given date is within the last 6 months of the current date, False otherwise.
  """
  current_date = datetime.date.today()
  six_months_ago = current_date - datetime.timedelta(days=6 * 30.5)
  return date >= six_months_ago

def is_between_last_7_to_12_months(date):
  """Checks if a datetime.date is between the last 7 months to 12 months of the current date.
  Args:
    date: A datetime.date object.
  Returns:
    True if the given date is between the last 7 months to 12 months of the current date, False otherwise.
  """
  current_date = datetime.date.today()
  seven_months_ago = current_date - datetime.timedelta(days=7 * 30.5)
  twelve_months_ago = current_date - datetime.timedelta(days=12 * 30.5)
  return date >= seven_months_ago and date <= twelve_months_ago



# ------------ TEST AREA -----------------

sales_data_for_item = getSalesData('22BPJ5NDB3J6KRXC3YNAXBEE')

def parseSalesData(sales_data_for_item):
    salesData = [sales_data_for_item[0][1], len(sales_data_for_item)]   # [name, quantity, revenue, dates overview, 6 months, 7-12 months, +12 months]
    totalRevenue = 0
    countDates = defaultdict(int)
    sixMonths = defaultdict(int)
    twelveMonths = defaultdict(int)
    aboveTwelveMonths = defaultdict(int)
    for row in sales_data_for_item:
        totalRevenue += row[2]
        countDates[str(row[0])] += 1

        if is_within_last_6_months(row[0]):
            sixMonths[str(row[0])] += 1
        elif is_between_last_7_to_12_months(row[0]):
            twelveMonths[str(row[0])] += 1
        else:
            aboveTwelveMonths[str(row[0])] += 1

    salesData.append(totalRevenue)
    salesData.append(countDates)
    salesData.append(sixMonths)
    salesData.append(twelveMonths)
    salesData.append(aboveTwelveMonths)

    return salesData    

parsedData = parseSalesData(sales_data_for_item)
print(parsedData)





# TODO: Calculate the output based on a weighted formula (use of dates required) --> SALES VOLUME


# ['Ladies Nun Fancy Dress Outfit Mother Superior Super Hero Costume', 2, Decimal('33.20'), 
# defaultdict(<class 'int'>, {'2023-10-04': 2}), 
# defaultdict(<class 'int'>, {'2023-10-04': 2}), 
# defaultdict(<class 'int'>, {}), 
# defaultdict(<class 'int'>, {})]