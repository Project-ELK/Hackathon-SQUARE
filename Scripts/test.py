# import csv
# from pprint import pprint 
# import numpy as np
from square.client import Client
import uuid

client = Client(
  access_token="EAAAEDVYe8ka9okFKiK3xkEb-sjcPyg9HNZwIjQDH5JX9EM3zXwQon8avcZgklNE",
  environment="sandbox"
)

# Function to generate Idem Key
def generateIdem():
  return str(uuid.uuid4())


lineItems = []

lineItems.append({
    "quantity": "1",
    "catalog_object_id": "FVQV2MWPNULZ2DL3VKJM64UA",
    "base_price_money": {
    "amount": 571,
    "currency": "GBP"
    }
})

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

# CX0Zln2l6enZe2A6j0dOOAgyUgcZY

# EAAAEDVYe8ka9okFKiK3xkEb-sjcPyg9HNZwIjQDH5JX9EM3zXwQon8avcZgklNE

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
            "amount": 571,
            "currency": "GBP"
        },
        "order_id": order_id,
        "cash_details": {
            "buyer_supplied_money": {
            "amount": 571,
            "currency": "GBP"
            }
        }
    }
)
if result.is_success():
    print(result.body)
elif result.is_error():
    print(result.errors)