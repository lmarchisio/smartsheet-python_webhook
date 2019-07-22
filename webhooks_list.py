import smartsheet
import logging

# Set API access token
access_token = None

# initialize client
ss_client = smartsheet.Smartsheet(access_token)
# make sure we don't miss any errors
ss_client.errors_as_exceptions(True)
# log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

# TODO add Smartsheet API access token

# list webhooks
IndexResult = ss_client.Webhooks.list_webhooks(
    page_size = 100,
    page = 1,
    include_all = False)

print(IndexResult)
