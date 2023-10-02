from square.client import Client
from pprint import pprint
import csv

client = Client(
    access_token="EAAAEDVYe8ka9okFKiK3xkEb-sjcPyg9HNZwIjQDH5JX9EM3zXwQon8avcZgklNE",
    environment="sandbox"
)

file = None

try:
  with open("./Catalog/VariationIdCatalog.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    prevCursor = ""
    result = None
    globalCountItems = 1
    while True:
      if prevCursor == "":
        # Lists catalog for the first page (100 items)
        result = client.catalog.list_catalog(
          types="ITEM"
        )
      else:
        # Lists the catalog for the next page as per cursor
        result = client.catalog.list_catalog(
          cursor=prevCursor,
          types="ITEM"
        )

      # Loop through
      if result.is_success():
        for object in result.body["objects"]:
          item_id = object["id"]
          variation_id = object["item_data"]["variations"][0]["id"]
          # item_name = object["item_data"]["name"]
          # print(globalCountItems, item_id, item_name)
          writer.writerow([globalCountItems,variation_id])
          globalCountItems += 1
      elif result.is_error():
        # TODO throw error
        pprint(result.errors)

      prevCursor = result.body["cursor"]
except Exception as error:
  file.close()
  print(f"Error: {error}")


