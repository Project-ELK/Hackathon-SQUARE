"""
create a single order, but loop through CSV and buy from every inventory item a random amount under 500

open csv

    request body = {
        ...
    }
    for each item

        append to request body the (variation id...)
    
close csv

append trailing objects to request body after we have got all the items sales data

make api request

"""
from square.client import Client

client = Client(
    access_token="EAAAEDVYe8ka9okFKiK3xkEb-sjcPyg9HNZwIjQDH5JX9EM3zXwQon8avcZgklNE",
    environment="sandbox"
)

file = None


result = client.orders.create_order(
  body = {
    "order": {
      "location_id": "057P5VYJ4A5X1",
      "reference_id": "my-order-001",
      "line_items": [
        {
          "name": "New York Strip Steak",
          "quantity": "1",
          "base_price_money": {
            "amount": 1599,
            "currency": "USD"
          }
        },
        {
          "quantity": "2",
          "catalog_object_id": "BEMYCSMIJL46OCDV4KYIKXIB",
          "modifiers": [
            {
              "catalog_object_id": "CHQX7Y4KY6N5KINJKZCFURPZ"
            }
          ],
          "applied_discounts": [
            {
              "discount_uid": "one-dollar-off"
            }
          ]
        }
      ],
      "taxes": [
        {
          "uid": "state-sales-tax",
          "name": "State Sales Tax",
          "percentage": "9",
          "scope": "ORDER"
        }
      ],
      "discounts": [
        {
          "uid": "labor-day-sale",
          "name": "Labor Day Sale",
          "percentage": "5",
          "scope": "ORDER"
        },
        {
          "uid": "membership-discount",
          "catalog_object_id": "DB7L55ZH2BGWI4H23ULIWOQ7",
          "scope": "ORDER"
        },
        {
          "uid": "one-dollar-off",
          "name": "Sale - $1.00 off",
          "amount_money": {
            "amount": 100,
            "currency": "USD"
          },
          "scope": "LINE_ITEM"
        }
      ]
    },
    "idempotency_key": "8193148c-9586-11e6-99f9-28cfe92138cf"
  }
)

if result.is_success():
  print(result.body)
elif result.is_error():
  print(result.errors)