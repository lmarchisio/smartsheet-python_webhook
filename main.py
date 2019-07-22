import smartsheet
import json

access_token = None
ss_client = smartsheet.Smartsheet(access_token)

column_map = {}

def smartsheet_webhook_responder(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    # if this is a challenge, return approrpiate verification
    if request.args and 'challenge' in request.args:
        return 'not far enough'
    elif request_json and 'challenge' in request_json:
        return json.dumps({
            "smartsheetHookResponse": request_json['challenge']
        })
    # if this is a callback, delete the test row
    elif request_json and 'scopeObjectId' in request_json:
        sheetid = request_json['scopeObjectId']
        sheet = ss_client.Sheets.get_sheet(
            sheetid)
        for column in sheet.columns:
            column_map[column.title] = column.id
        for row in sheet.rows:
            approved_cell = row.get_column(column_map['Approved?'])
            approved_value = approved_cell.display_value
            item_cell = row.get_column(column_map['Item or Task Description'])
            item_value = item_cell.display_value
            if approved_value == None and item_value != None:
                new_cell = ss_client.models.Cell()
                new_cell.column_id = column_map['Approved?']
                new_cell.formula = '=IF(OR([Supervisor Confirmed]@row = 1, [PM Override]@row = 1), 1, 0)'
                new_cell.strict = False

                new_row = ss_client.models.Row()
                new_row.id = row.id
                new_row.cells.append(new_cell)

                updated_row = ss_client.Sheets.update_rows(
                    sheetid,
                    [new_row])
    else:
        return 'too far!'

