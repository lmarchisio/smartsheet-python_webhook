import smartsheet
import json

access_token = None
ss_client = smartsheet.Smartsheet(access_token)

column_map = {}
departments = ["CNC", "Design"]

def get_cell_by_column_name(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)

def make_approved(source_row):
  # build new cell value
  new_cell = ss_client.models.Cell()
  new_cell.column_id = column_map["Approved?"]
  new_cell.formula = '=IF(OR([Supervisor Confirmed]@row = 1, [PM Override]@row = 1), 1, 0)'

  # build the row to update
  new_row = ss_client.models.Row()
  new_row.id = source_row.id
  new_row.cells.append(new_cell)

  return new_row

def make_cncstart(source_row, source_dept):
  new_cell = ss_client.models.Cell()
  new_cell.column_id = column_map[source_dept + " Start"]
  new_cell.formula = '=IF([Labor / Complete]@row = 0, IF([Dept.]@row = "' + source_dept + '", Start@row))'

  new_row = ss_client.models.Row()
  new_row.id = source_row.id
  new_row.cells.append(new_cell)

  return new_row

def make_cncfinish(source_row):
  new_cell = ss_client.models.Cell()
  new_cell.column_id = column_map["CNC Finish"]
  new_cell.formula = '=IF([Labor / Complete]@row = 0, IF([Dept.]@row = "CNC", Finish@row))'

  new_row = ss_client.models.Row()
  new_row.id = source_row.id
  new_row.cells.append(new_cell)

  return new_row

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
    # if this is a callback
    elif request_json and 'scopeObjectId' in request_json:
        sheetid = request_json['scopeObjectId']
        sheet = ss_client.Sheets.get_sheet(sheetid)
        for column in sheet.columns:
          column_map[column.title] = column.id

        rowsToUpdate = [row for row in sheet.rows if get_cell_by_column_name(row, "Approved?").display_value is None and get_cell_by_column_name(row, "Item or Task Description").display_value is not None]

        if rowsToUpdate != []:
          writeRows1 = []
          for row in rowsToUpdate:
            write_row1 = make_approved(row)
            writeRows1.append(write_row1)

          result = ss_client.Sheets.update_rows(sheetid, writeRows1)

          for department in departments:
            writeRows2 = []
            for row in rowsToUpdate:
              write_row2 = make_cncstart(row, department)
              writeRows2.append(write_row2)
              
            result = ss_client.Sheets.update_rows(sheetid, writeRows2)

