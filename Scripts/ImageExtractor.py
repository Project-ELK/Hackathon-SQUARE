from selenium import webdriver
from selenium.webdriver.common.by import By
import time

 
# What you enter here will be searched for in
# Google Images
query = "jelly cat frog"

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

# Finding the search box
box = driver.find_element(By.NAME, 'q')



# Type the search query in the search box
box.send_keys(query)
box.submit()

time.sleep(1)

# Only gets the first element found on the search
firstImageReturned = driver.find_elements(by='css selector', value='.FRuiCf')[0]
imageElement = firstImageReturned.find_element(By.TAG_NAME,'img')
# Outputs image src
print(imageElement.get_attribute('src'))
print("done")

driver.close()
driver.quit()


# TODO Get IMAGE from square API for pepsi (as test)