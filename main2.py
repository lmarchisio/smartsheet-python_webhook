import smartsheet
import json

access_token = None
column_map = {}
status_columns = {}
smart = smartsheet.Smartsheet(access_token)

def get_cell(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)

def get_status_cell(row, column_name):
    column_id = status_columns[column_name]
    return row.get_column(column_id)

def find_pm(sheetid):
    response = smart.Sheets.get_sheet_summary_fields(
        sheetid
    )

    a = json.loads(str(response))

    if 'data' in a:
        b = a['data']
        for thing in b:
            if thing['title'] == 'PM':
                if 'objectValue' in thing:
                    if 'email' in thing['objectValue']:
                        return((thing['objectValue'])['email'])
    else:
        return None

def make_pm(source_row, pm):
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = column_map['PM']
    new_cell.value = pm
    
    new_row = smartsheet.models.Row()
    new_row.id = source_row.id
    new_row.cells.append(new_cell)
    
    return new_row

def update_pm(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    # if this is a challenge, return verification
    if request.args and 'challenge' in request.args:
        return None
    elif request_json and 'challenge' in request_json:
        return json.dumps({
            "smartsheetHookResponse": request_json['challenge']
        })
    elif request_json and 'scopeObjectId' in request_json:
        sheetid = request_json['scopeObjectId']
        sheet = smart.Sheets.get_sheet(sheetid)
        the_pm = find_pm(sheetid)
           
        for column in sheet.columns:
            column_map[column.title] = column.id

        rowsToUpdate = [row for row in sheet.rows if get_cell(row, "PM").display_value is None]

        if rowsToUpdate != []:
            pm_rows = []
            for row in rowsToUpdate:
                write_row = make_pm(row, the_pm)
                pm_rows.append(write_row)

            result = smart.Sheets.update_rows(sheetid, pm_rows)


