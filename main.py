def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

import smartsheet

access_token = None
ss_client = smartsheet.Smartsheet(access_token)

column1 = smartsheet.models.Column({
    'title': 'wibbles',
    'type': 'DATE',
    'index': 1
})

new_columns = ss_client.Sheets.add_columns(
    1142764617394052,
    [column1])

print('done now')
