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

# TODO enter Smartsheet API Access Token
# change callbackUrl to function trigger

print('To create webhook enter sheet ID')
this_sheet = input()

# create webhook
Webhook = ss_client.Webhooks.create_webhook(
    smartsheet.models.Webhook({
        'name': 'Webhook #4',
        'callbackUrl': 'https://google-cloud-function-trigger',
        'scope': 'sheet',
        'scopeObjectId': this_sheet,
        'events': ['*.*'],
        'version': 1}))
