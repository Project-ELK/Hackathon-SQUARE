from Scripts.ImageKeywords import *
import numpy as np
import os
from pprint import pprint 
from Scripts.GetTextEmbedding import *
from GetSalesData import *

def getImageURL(Item_IDs):
    data_list = []
    csv_file = os.getcwd() + "\Catalog\ImageCatalog.csv"
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if row[1] == Item_IDs[0] or row[1] == Item_IDs[1] or row[1] == Item_IDs[2] or row[1] == Item_IDs[3] or row[1] == Item_IDs[4]:
                data_list.append(row[5])
    return data_list

def getItemKeywordFromImage(fileName):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd()+"\winged-scout-401122-ae11907f66c0.json"
    response = classifyImage(os.getcwd()+f"\API\static\{fileName}")     # TODO: check FILE PATH IS CORRECT

    keywordsMatrix = []
    if response:
        for label in response.label_annotations:
            print(f"Label: {label.description}, Score: {label.score}")
            keywordsMatrix.append([label.description, label.score])
    else:
        print("Cannot classify Image")

    # TODO: Pass Keywords matrix to the returnSimilarityScores() function in GetTextEmbeddings --> see example

    print ("getItemKeywordFromImage() is DONE")
    return keywordsMatrix

def getSummary():
    aiplatform.init(project="winged-scout-401122")
    # initialize Connector object for the database
    connector = Connector()
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

    labelMatrix = getItemKeywordFromImage("9152667_R_SET.jpg")
    similarScores = returnSimilarityScores(pool,labelMatrix)

    arr = np.array(similarScores)
    arr = arr[arr[:, 4].argsort()][::-1]

    # find top 375
    itemIDs = set()
    counter = 0
    topkeywordsUnique = []
    for row in arr:
        if counter == 375:
            break
        if row[0] in itemIDs:
            continue
        counter +=1
        itemIDs.add(row[0])
        topkeywordsUnique.append(row)   
    # Converts to np array 
    topkeywordsUnique = np.array(topkeywordsUnique)
    
    salesData = []
    for item in topkeywordsUnique:
        getSalesDataVal =getSalesData(item[0])
        #if getSalesDataVal[0][1]:
        if getSalesDataVal is not None:
            salesData.append(parseSalesData(getSalesDataVal))
    
    # 5 sales data
    # below = 0
    # above or average = 1
    
    goodSalesValue = 0    
    for sales in salesData:
        averageSalesforItem = getSalesAverages(isSix=True, price=sales[2]/sales[1])
        if sales[2] >= averageSalesforItem:
            goodSalesValue += 1
    
    goodSalesValue = goodSalesValue / len(salesData)
    print(f"The percent is: {goodSalesValue*100}")    

    top5KeywordsUnique = topkeywordsUnique[0:5, :]



    connector.close()
    return (round(goodSalesValue, 4), getImageURL(top5KeywordsUnique[:,0]), salesData[:5])



if __name__ == "__main__":
    similarScores = getSummary()

