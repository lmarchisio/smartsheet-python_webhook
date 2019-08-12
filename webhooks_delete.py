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

print('Enter ID of webhook to be deleted')
this_webhook = input()

ss_client.Webhooks.delete_webhook(this_webhook)

# Finish it
print('We made it this far.')
print('Good Job.')
