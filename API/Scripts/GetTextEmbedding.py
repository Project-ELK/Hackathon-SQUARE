# from google.cloud import vertexai.preview
from vertexai.language_models import TextEmbeddingModel
from google.cloud import aiplatform
import os
from scipy.spatial.distance import cosine
import numpy as np
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import pickle
import time
import heapq

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd()+"\winged-scout-401122-ae11907f66c0.json"
aiplatform.init(project="winged-scout-401122")
# initialize Connector object for the database
connector = Connector()

def text_embedding(arrOfKeywords) -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko-multilingual")
    return model.get_embeddings(arrOfKeywords)

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

# 1) Generate Text Embeddings for all Keywords in our Keywords Table
# 2) Generate Text embedding for the new item
# 3) Do the cosine similarity for the (new item) compared to (Every item) in our keywords DB text embedding
# 4) pull the keywords that have a good score ( > 0.8)  (sort & pull TOP 10?)
    # 4a) if nothing similar -> show a dancing cat gif
# 5) check their Item_ID
# 6) pull the items from the db
# 7) see if they sell well (using designated metrics)
# 8) Produce descriptive output to the user

# Generate text embeddings in bulk for all of the values in the database
def generateTextEmbeddingsBulk():
    data_array = None
    # Generates text embeddings of all keywords that currently do not have one
    with pool.connect() as db_conn:
        # Looping through keywords in batches of five (ones with empty embeddings)
            while True:
                try:
                    print("Looping again")
                    result = db_conn.execute(sqlalchemy.text("SELECT Keyword_ID, Keyword FROM Keywords WHERE text_embedding IS NULL LIMIT 5;")).fetchall()
                    if not result:
                        print("no keywords")
                        connector.close() #Closes connection to the database
                        break
                    # db_conn.execute(sqlalchemy.text("ALTER TABLE Keywords ADD text_embedding BLOB AFTER Keyword;"))
                    # commit transaction
                    db_conn.commit()
                    
                    # Numpy Array to acquire the list of Item_IDs and Keywords where embeddings are blank
                    data_array = np.array(result)
                    arrOfKeywords = data_array[:,1]
                    # call get embedings on the each keywords
                    embeddings = text_embedding(arrOfKeywords)            
                    
                    for i, embedding in enumerate(embeddings):
                        keyword_id = data_array[:,0][i]
                        # Serialise the text embeddings
                        blobbies = pickle.dumps(embedding.values)

                        # Insert Into the Keywords table
                        db_conn.execute(sqlalchemy.text("UPDATE Keywords SET text_embedding = :blob WHERE Keyword_ID = :keyword_id;"),parameters={"blob": blobbies, "keyword_id":keyword_id})
                        db_conn.commit()
                        print("Adding to the database")

                        # deseralize
                        # loaded_array = pickle.loads(result2[0][0])

                except Exception as error:
                    print(f"Error in database: {error}")
                    time.sleep(55)

# Generates model for text embeddings based on the array of keywords
def generateEmbeddings(keywords):
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko-multilingual")
    embeddings1 = model.get_embeddings(keywords[:5])  # first 5
    # embeddings2 = model.get_embeddings(keywords[5:10])  # last 5
    embeddingVectors = []
    for embedding in embeddings1: #+ embeddings2:
        embeddingVectors.append(embedding.values)
    return embeddingVectors

# Helper function to get cosine similarity
def getCosineSimilarity(vector1, vector2):
    return 1 - cosine(vector1, vector2)


def returnSimilarityScores(pool, labelsMatrix):
    labelNumpy = np.array(labelsMatrix)    
    embeddingVectors = generateEmbeddings(labelNumpy[:,0])

    data_array = None
    with pool.connect() as db_conn:
        # Gets the text embeddings for all keywords in the database table Keywords
        result = db_conn.execute(sqlalchemy.text("SELECT Item_ID, Keyword, Score, text_embedding FROM Keywords WHERE text_embedding IS NOT NULL;")).fetchall()
        db_conn.commit()
        if not result:
            print("No Text Embeddings Found")
            return None
        # Stores the result into a numpy array
        data_array = np.array(result)
    db_conn.close()
    
    # This array stores: [Item_ID, Keyword, Classification Score, Keyword Index Similar to, Similarity Score]
    resultantScores =[]
    # Goes through each keyword in the database
    for Item_ID, Keyword, Score, text_embedding in data_array:
        # Going through each vector for the "new item's keywords"
        for i, vector in enumerate(embeddingVectors):
            # de-serialise database text embedding (for comparison)
            databaseVector = pickle.loads(text_embedding)
            # Gets cosine similariy for the vector(new item) and database vector (database item)
            similarityScore = getCosineSimilarity(vector,databaseVector)
            # If the similarity score is above a certain threshold then add to final array
            if(similarityScore>=0.7):
                resultantScores.append([Item_ID, Keyword, Score, i,similarityScore])
        
    # TODO: maintain sorted data structure OR add to list and sort at end
        # TODO: May not be required?? 
    
    # Returns similar keywords array for further analysis
    return resultantScores

if __name__ == "__main__":
    # TODO: Test Keywords (what the GetItemSummary will pass to this function)
    labelMatrix = [['Train', 0.9055610299110413], ['Mode of transport', 0.8466993570327759], 
                   ['Rolling', 0.8068732619285583], ['Toy', 0.7726133465766907], 
                   ['Rolling stock', 0.7489355206489563], ['Locomotive', 0.732448399066925], 
                   ['Thomas the tank engine', 0.7165026664733887], ['Electric blue', 0.7040618062019348], 
                   ['Vehicle', 0.6723816394805908], ['Railway', 0.6706249713897705]]
    similarScores = returnSimilarityScores(pool,labelMatrix)
    