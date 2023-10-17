from Scripts.ImageKeywords import classifyImage
import numpy as np
import os
from pprint import pprint 

from Scripts.GetTextEmbedding import *

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

    pprint(arr)

    return arr



if __name__ == "__main__":
    similarScores = getSummary()

# 4) does it sell well

# # 2) get keywords of uploaded image
# if __name__ == "__main__":

#     aiplatform.init(project="winged-scout-401122")
#     # initialize Connector object for the database
#     connector = Connector()
    
#     def getconn() -> pymysql.connections.Connection:
#         conn: pymysql.connections.Connection = connector.connect(
#             "winged-scout-401122:europe-west2:team-elk-sql",
#             "pymysql",
#             user="root",
#             password="",
#             db="team-elk-db"
#         )
#         return conn
#     # create connection pool
#     pool = sqlalchemy.create_engine(
#         "mysql+pymysql://",
#         creator=getconn,
#     )
    
#     labelMatrix = getItemKeywordFromImage("9152667_R_SET.jpg")
#     similarScores = returnSimilarityScores(pool,labelMatrix)

#     arr = np.array(similarScores)
#     arr = arr[arr[:, 4].argsort()][::-1]

#     pprint(arr)

#     print("done")

#     print(arr)

