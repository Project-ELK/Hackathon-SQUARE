import os
from google.cloud import vision
import base64
from google.cloud.vision_v1 import types
import numpy as np
import csv

# TODO: Integrate Keyword with every image and modify the response JSON to a string/array of keywords?]

# TODO: Store the list/string of keywords into a csv file and then feed into ML algorithm/model

# TODO: Research further integration of ML models - trend prediction? ANN (Artificial Neural Network), Bayes' ML algorithms too?

# TODO: Test using WEKA? weka weka ;)

# Setting the OS environment (Modify as required)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd()+"\winged-scout-401122-ae11907f66c0.json"



#TODO: 
#1) Loop throuugh csv file
#2) Load Image URL 
#3) Generate keywords
#4) Save it to new CSV file in correct format
# FORMAT: Keyword_ID int AUTOINCREMENT, Item_ID varchar(255), Keyword varchar(255), Score DECIMAL(4,4), 

def bulkClassification():
    # Create a client for the Vision API
    client = vision.ImageAnnotatorClient()
    f = None
    numpyList = None
    with open('./Catalog/ImageCatalog.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skips header
        # Acquires a list of rows in the CSV file
        rows = list(reader)
        numpyList = np.array(rows)
    f.close()
        
    # Acquires a list of [Item_ID, ImageURL]
    listOfItems = numpyList[:,[1,5]]

    kf = None
    counter = 1
    with open('./Catalog/keywords.csv', 'w', newline="", encoding='UTF-8') as kf:
        writer = csv.writer(kf)
        for itemID, imgURL in listOfItems:
            # ID where it messes up: CDT6IGHTXLZYY355LXOYBUWF
            # Decode the base64 image data
            try:
                image_data = base64.b64decode(str(imgURL).split(",")[1])
            except:
                continue
            # Create an Image object with the image URL
            image = types.Image(content=image_data)

            # Perform label detection on the image
            response = client.label_detection(image=image)

            rows = []
            for label in response.label_annotations:
                row = [counter, str(itemID), label.description, label.score]
                rows.append(row)
                # TODO: Save the label descr and score as a row (for that particular ITEM ID)
                #print(f"Label: {label.description}, Score: {label.score}")
                counter += 1
            writer.writerows(rows)
    kf.close()
    
def classifyImage(imagepath):
    # Create a client for the Vision API
    client = vision.ImageAnnotatorClient()
    # Create a Vision API client
    try:
        # Open the image file in binary mode and read its content
        with open(imagepath, 'rb') as image_file:
            image_data = image_file.read()

        # Create an Image object with the image data
        image = types.Image(content=image_data)

        # Perform label detection on the image
        response = client.label_detection(image=image)

        # Return the label detection results
        return response
    except Exception as e:
        print("Error:", str(e))

    return None  # Return None in case of an error

# Example usage:
# image_url = "https://example.com/your_image.jpg"
# response = classifyImage(image_url)

if __name__ == "__main__":
    response = classifyImage(os.getcwd()+"\API\static\9152667_R_SET.jpg")
    if response:
        for label in response.label_annotations:
            print(f"Label: {label.description}, Score: {label.score}")
    print ("DONE")