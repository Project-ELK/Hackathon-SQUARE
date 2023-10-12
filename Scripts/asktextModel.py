import vertexai
from vertexai.language_models import TextGenerationModel
import os
import timeit

vertexai.init(project="winged-scout-401122")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Eashan Ghelani\Documents\Hackathon-SQUARE\Scripts\winged-scout-401122-ae11907f66c0.json"

parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}

def askModel():
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        """Give the similarity score of a: kitten, cat(in decimal)""",
        **parameters
    )
    print(f"Response from Model: {response.text}")
    
    
execution_time = timeit.timeit(askModel, number=5)
print(f"Execution time: {execution_time} seconds for 5 run")