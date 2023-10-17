from square.client import Client
import csv
import numpy as np
import uuid
import random

#with open("./catalog.csv"):
client = Client(
  access_token="EAAAEDVYe8ka9okFKiK3xkEb-sjcPyg9HNZwIjQDH5JX9EM3zXwQon8avcZgklNE",
  environment="sandbox"
)

# Function to generate Idem Key
def generateIdem():
  return str(uuid.uuid4())

f = None

with open('./Catalog/ImageCatalog.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    # Acquires a list of rows in the CSV file
    rows = list(reader)
    numpyList = np.array(rows)
    # Acquires a list of ItemVariationIDs
    listOfItemVariationIDs = numpyList[:,[2,4]]

# TODO: Do the FOR LOOP HERE
lineItems = []
total_payment = 0
itemCount = 0
for itemID, price in listOfItemVariationIDs:
  
  item_price = int(price)
  # Determines the max number of items to be bought
  upperBound = 7
  if item_price > 20:
    upperBound = 3
  elif item_price > 50:
    upperBound = 2
  elif item_price > 100:
    upperBound = 1
  
  lowerBound = 0
  # Determines if the item is bought or not
  
  # If the item is expensive, we give the user 30% chance of purchasing something
  if item_price >= 100 and random.randint(1,100) >= 70:
    lowerBound = 1
  # If the item is less expensive, we give the user 55% chance of purchasing something  
  elif item_price >= 50 and random.randint(1,100)>45:
    lowerBound = 1
  # If the item is cheap, we give the user 80% chance of purchasing something
  elif item_price >= 0 and random.randint(1,100) >20:
    lowerBound = 1
  
  # Repeats the process every 300 items
  
  # If the lineItem list has reached the maximum amount, we need to make the order (for the previous line items)
  if itemCount >= 299:
    # Creating an order
    result = client.orders.create_order(
    body = {
      "order": {
        "location_id": "L9SATKFBV2TKY",
        "line_items": lineItems,
        "state": "OPEN"
      },
      "idempotency_key": generateIdem()
    }
    )
    order_id = None
    if result.is_success():
      print(result.body)
      order_id = str(result.body["order"]["id"])
    elif result.is_error():
      print(result.errors)

    # Creating the payment for the above order
    result = client.payments.create_payment(
      body = {
        "source_id": "CASH",
        "idempotency_key": generateIdem(),
        "amount_money": {
          "amount": total_payment,
          "currency": "GBP"
        },
        "order_id": order_id,
        "cash_details": {
          "buyer_supplied_money": {
            "amount": total_payment,
            "currency": "GBP"
          }
        }
      }
    )
    if result.is_success():
      print(result.body)
    elif result.is_error():
      print(result.errors)
    
    # Resets the lineItems array and the total payment
    lineItems = []
    itemCount = 0
    total_payment = 0
  else:
    itemCount += 1
  # GENERATE LINE ITEMS + values
  quantity_of_items = random.randint(lowerBound, upperBound)
  lineItems.append({
      "quantity": str(quantity_of_items),
      "catalog_object_id": str(itemID),
      "base_price_money": {
        "amount": item_price,
        "currency": "GBP"
      }
  })
  total_payment += (item_price * quantity_of_items)