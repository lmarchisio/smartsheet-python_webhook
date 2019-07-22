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

print('To enable webhook enter webhook ID')
the_webhook = input()

# enable webhook
Webhook = ss_client.Webhooks.update_webhook(
    the_webhook,
    ss_client.models.Webhook({
        'enabled': True}))
