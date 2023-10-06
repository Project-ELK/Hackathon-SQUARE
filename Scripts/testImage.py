import os
from google.cloud import vision
from google.cloud.vision_v1 import types

# TODO: Integrate Keyword with every image and modify the response JSON to a string/array of keywords?]

# TODO: Store the list/string of keywords into a csv file and then feed into ML algorithm/model

# TODO: Research further integration of ML models - trend prediction? ANN (Artificial Neural Network), Bayes' ML algorithms too?

# TODO: Test using WEKA? weka weka ;)

# Setting the OS environment (Modify as required)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ghela\Documents\Hackathon-SQUARE\Scripts\winged-scout-401122-ae11907f66c0.json"

# Create a client for the Vision API
client = vision.ImageAnnotatorClient()

# Load an image from a file (you can also use a URL)
with open('download.jpg', 'rb') as image_file:
    content = image_file.read()

# Create an Image object
image = types.Image(content=content)

# Perform label detection on the image
response = client.label_detection(image=image)

# Print labels found in the image
for label in response.label_annotations:
    print(f"Label: {label.description}, Score: {label.score}")

