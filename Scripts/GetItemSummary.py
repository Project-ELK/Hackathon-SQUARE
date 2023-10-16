from ImageKeywords import classifyImage
import numpy as np

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd()+"\winged-scout-401122-ae11907f66c0.json"
response = classifyImage(os.getcwd()+"\API\static\9152667_R_SET.jpg")

keywordsMatrix = []
if response:
    for label in response.label_annotations:
        print(f"Label: {label.description}, Score: {label.score}")
        keywordsMatrix.append([label.description, label.score])
else:
    print("Cannot classify Image")

# TODO: Pass Keywords matrix to the returnSimilarityScores() function in GetTextEmbeddings --> see example

print ("DONE")
