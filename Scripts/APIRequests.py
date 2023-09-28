from square.client import Client

client = Client(
  access_token="EAAAEDVYe8ka9okFKiK3xkEb-sjcPyg9HNZwIjQDH5JX9EM3zXwQon8avcZgklNE",
  environment="sandbox"
)



result = client.catalog.retrieve_catalog_object(
  object_id = "IN7HYUDZLRFPKXGRK4ZYS7ST",
  include_related_objects = True
)

if result.is_success():
  print(result.body)  
elif result.is_error():
  print(result.errors)