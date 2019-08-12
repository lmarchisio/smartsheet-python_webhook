import smartsheet
import logging
import json
import pprint

# list webhooks

# Set API access token
access_token = None

# initialize client
smart = smartsheet.Smartsheet(access_token)
# make sure we don't miss any errors
smart.errors_as_exceptions(True)
# log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

IndexResult = smart.Webhooks.list_webhooks(
    page_size=100,
    page=1,
    include_all=False)

a = json.loads(str(IndexResult))
b = a.get('data', 0)

for n in range(len(b)):
    c = b[n]
    print(str(c['status']) + ': ' + str(c['id']) + ': ' + str(c['name']))
    
print(len(b))

# uncomment below to also print all data
# pprint.pprint(a)

