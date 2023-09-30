from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import numpy as np
import csv

 
# What you enter here will be searched for in
# Google Images

with open('./Catalog/catalog.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

numpyList = np.array(rows)
f.close()

options = webdriver.ChromeOptions()
# This will disable any extensions installed in chrome (for testing)
options.add_argument("--disable-extensions")
options.add_argument("--incognito")  # Open in incognito mode
options.add_argument("--disable-cache")  # Disable cache  
 
# Creating a webdriver instance
driver = webdriver.Chrome(options=options)
 
# Maximize the screen
driver.maximize_window()
 
# Open Google Images in the browser
driver.get('https://images.google.com/')

time.sleep(1)
reject_policy_button = driver.find_element(By.ID, 'W0wltc')
reject_policy_button.click()

# ----------------- RUNNING THE SEARCH FOR THE FIRST TIME ----------------------------------

listOfNames = numpyList[:,2]
query = listOfNames[0]
listOfImageURLS = []


# Finding the search box
box = driver.find_element(By.NAME, 'q')
# Type the search query in the search box
box.send_keys(query)
box.submit()
time.sleep(1)
# Only gets the first element found on the search
firstImageReturned = driver.find_elements(by='css selector', value='.FRuiCf')[0]
imageElement = firstImageReturned.find_element(By.TAG_NAME,'img')
listOfImageURLS.append(imageElement.get_attribute('src'))
# TODO: Write IMAGE URL to CSV

for i in range(1,len(listOfNames)):
    try:
        box = driver.find_element(By.NAME, 'q')
        box.clear()
        query = str(random.randint(0,50))
        # Type the search query in the search box
        query = listOfNames[i]
        box.send_keys(query)
        box.submit()
        # time.sleep(0.25)
        # Only gets the first element found on the search
        firstImageReturned = driver.find_elements(by='css selector', value='.FRuiCf')[0]
        imageElement = firstImageReturned.find_element(By.TAG_NAME,'img')
        # print(imageElement.get_attribute('src'))
        listOfImageURLS.append(imageElement.get_attribute('src'))
    except Exception as e:
        listOfImageURLS.append("")


numpyList[:, 3] = listOfImageURLS
formatted_data = np.array([f'{row[0]}, "{row[1]}", "{row[2]}", "{row[3]}"' for row in numpyList])
# savedArray = np.asarray(numpyList)

np.savetxt('./Catalog/ImageCatalog.csv', formatted_data, delimiter=',', fmt='%s', header='Item Number,Item ID,Item Name,Image URL', comments='')
driver.close()
driver.quit()


# TODO Get IMAGE from square API for pepsi (as test)