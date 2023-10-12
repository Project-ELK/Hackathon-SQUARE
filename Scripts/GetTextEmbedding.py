# from google.cloud import vertexai.preview
from vertexai.language_models import TextEmbeddingModel
from google.cloud import aiplatform
import os
from scipy.spatial.distance import cosine
import numpy as np
import time
import mysql.connector


aiplatform.init(project="winged-scout-401122")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Eashan Ghelani\Documents\Hackathon-SQUARE\Scripts\winged-scout-401122-ae11907f66c0.json"
# Set your Google Cloud project ID as an environment variable


# 1) Generate Text Embeddings for all Keywords in our Keywords Table
# 2) Generate Text embedding for the new item
# 3) Do the cosine similarity for the (new item) compared to (Every item) in our keywords DB text embedding
# 4) pull the keywords that have a good score ( > 0.8)  (sort & pull TOP 10?)
    # 4a) if nothing similar -> show a dancing cat gif
# 5) check their Item_ID
# 6) pull the items from the db
# 7) see if they sell well (using designated metrics)
# 8) Produce descriptive output to the user


# Connect to the Google Cloud SQL database
connection = mysql.connector.connect(
    user='root',
    password='',
    host='34.142.61.56',
    database='team-elk-db'
)



# TODO: Get list of IDS, keywords from gcloud database
#SELECT item_id, keyword FROM elk-project-db WHERE score > 0.7



# TODO: Pass list of keywords to get_embedding


#Insert a column with a BLOB
# ALTER TABLE [table name] ADD embeddings BLOB
# INSERT INTO [table name] (embedding) VALUES ()

def text_embedding(text1, text2) -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko-multilingual")
    # model.task_type = "SEMANTIC_SIMILARITY"
    return model.get_embeddings([text1, text2,text1, text2,text1])

def vector_similarity(vec1, vec2):
    return np.dot(np.squeeze(np.array(vec1)),np.squeeze(np.array(vec2)))


text1 = "Cat"
text2 = "Kitten"


if __name__ == "__main__":
    start_time = time.time()
    embeddings = text_embedding(text1, text2)
    # Calculate cosine similarity between the two vectors
    similarity = 1 - cosine(embeddings[0].values, embeddings[1].values)
    print(f"Cosine Similarity: {similarity}")
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
