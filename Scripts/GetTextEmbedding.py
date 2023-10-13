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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ghela\Documents\Hackathon-SQUARE\Scripts\winged-scout-401122-ae11907f66c0.json"
aiplatform.init(project="winged-scout-401122")
# Set your Google Cloud project ID as an environment variable

# initialize Connector object for the database
connector = Connector()


def text_embedding(arrOfKeywords) -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko-multilingual")
    return model.get_embeddings(arrOfKeywords)

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


        
# 1) Generate Text Embeddings for all Keywords in our Keywords Table
# 2) Generate Text embedding for the new item
# 3) Do the cosine similarity for the (new item) compared to (Every item) in our keywords DB text embedding
# 4) pull the keywords that have a good score ( > 0.8)  (sort & pull TOP 10?)
    # 4a) if nothing similar -> show a dancing cat gif
# 5) check their Item_ID
# 6) pull the items from the db
# 7) see if they sell well (using designated metrics)
# 8) Produce descriptive output to the user


# TODO: Pass list of keywords to get_embedding

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

data_array = None
file = None
with pool.connect() as db_conn:
    # Looping through keywords in batches of five (ones with empty embeddings)
    try:
        
        while True:
            result = db_conn.execute(sqlalchemy.text("SELECT Keyword_ID, Keyword FROM Keywords WHERE text_embedding IS NULL LIMIT 5;")).fetchall()
            if not result:
                print("no keywords")
                connector.close #Closes connection to the database
                if file: file.close() #Closes the file if it exists
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
                keyword_id = data_array[0,i]
                # Serialise the text embeddings
                blobbies = pickle.dumps(embeddings[i].values)

                # Insert Into the Keywords table
                db_conn.execute(sqlalchemy.text("UPDATE Keywords SET text_embedding = :blob WHERE Keyword_ID = :keyword_id;"),parameters={"blob": blobbies, "keyword_id":keyword_id})
                db_conn.commit()

                # Check if the blob was saved
                # result2 = db_conn.execute(sqlalchemy.text("SELECT text_embedding FROM Keywords WHERE Keyword_ID = 1;")).fetchall()
                # db_conn.commit()

                # deseralize
                # loaded_array = pickle.loads(result2[0][0])

                # testTextEmbed = text_embedding(arrOfKeywords=["railway"])
                # TEST COSINE SIMILARITY
                # Calculate cosine similarity between the two vectors
                # similarity = 1 - cosine(testTextEmbed[0].values, loaded_array)
                # print(f"Cosine Similarity: {similarity}")
                break
            break
 
    except Exception as error:
        print(f"Error in database: {error}")
        # file.close()
        # Close the database connection
        connector.close()
    # Executes a select query (acquires 5 keywords where embeddings is blank)
    
# loaded_array = None
# with open('PickleFiles/embedding_1.pkl', 'rb') as file:
#     loaded_array = pickle.load(file)

# TEST COSINE SIMILARITY
# Calculate cosine similarity between the two vectors
# similarity = 1 - cosine(embeddings[0].values, embeddings[1].values)
# similarity2 = 1 - cosine(embeddings[0].values,loaded_array)
# print(f"Cosine Similarity: {similarity} and similarity 2: {similarity2}")

# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time} seconds")

# Close the pickle files
# file.close()

# # Close the database connection
# connector.close()