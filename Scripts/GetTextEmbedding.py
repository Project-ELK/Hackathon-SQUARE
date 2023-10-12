
# from google.cloud import vertexai.preview
from vertexai.language_models import TextEmbeddingModel
from google.cloud import aiplatform
import os
from scipy.spatial.distance import cosine
import numpy as np




aiplatform.init(project="winged-scout-401122")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Eashan Ghelani\Documents\Hackathon-SQUARE\Scripts\winged-scout-401122-ae11907f66c0.json"
# Set your Google Cloud project ID as an environment variable


# 1) Generate Text Embeddings for all Keywors in our Keywords Table
# 2) Generate Text embedding for the new item
# 3) Do the cosine similarity for the (new item) compared to (Every item) in our keywords DB text embedding
# 4) pull the keywords that have a good score ( > 0.8)  (sort & pull TOP 10?)
    # 4a) if nothing similar -> show a dancing cat gif
# 5) check their Item_ID
# 6) pull the items from the db
# 7) see if they sell well (using designated metrics)
# 8) Produce descriptive output to the user

def text_embedding() -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko-multilingual")
    # model.task_type = "SEMANTIC_SIMILARITY"
    return model.get_embeddings(["Mode of transport", "Food"])

def vector_similarity(vec1, vec2):
    return np.dot(np.squeeze(np.array(vec1)),np.squeeze(np.array(vec2)))



if __name__ == "__main__":
    embeddings = text_embedding()
    # Calculate cosine similarity between the two vectors
    similarity = 1 - cosine(embeddings[0].values, embeddings[1].values)
    print(f"Cosine Similarity: {similarity}")

    print(f"Vector Similarity: {vector_similarity(embeddings[0].values, embeddings[1].values)}")
