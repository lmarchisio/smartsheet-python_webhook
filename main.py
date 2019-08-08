import smartsheet
import json

access_token = None
ss_client = smartsheet.Smartsheet(access_token)

column_map = {}
departments = ["CNC", "Design", "Fab", "Install", "Metal", "Paint", "Sculpt", "Shipping"]

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

def make_start(source_row, source_dept):
  new_cell = ss_client.models.Cell()
  new_cell.column_id = column_map[source_dept + " Start"]
  new_cell.formula = '=IF([Labor / Complete]@row = 0, IF([Dept.]@row = "' + source_dept + '", Start@row))'

  new_row = ss_client.models.Row()
  new_row.id = source_row.id
  new_row.cells.append(new_cell)

  return new_row

def make_finish(source_row, source_dept):
  new_cell = ss_client.models.Cell()
  new_cell.column_id = column_map[source_dept + " Finish"]
  new_cell.formula = '=IF([Labor / Complete]@row = 0, IF([Dept.]@row = "' + source_dept + '", Finish@row))'

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
        event = request_json['events']
        time = request_json['timestamp']
        sheet = ss_client.Sheets.get_sheet(sheetid)
        
        row_a = ss_client.models.Row()
        row_a.to_top = True
        row_a.cells.append({
            'column_id': 6413332329588612,
            'value': str(sheetid)
        })
        row_a.cells.append({
            'column_id': 502357818664836,
            'value': str(event)
        })
        row_a.cells.append({
            'column_id': 8665132143273860,
            'value': str(time)
        })
        
        response = ss_client.Sheets.add_rows(
            5111763491415940,
            [row_a])
        
        for column in sheet.columns:
          column_map[column.title] = column.id

        rowsToUpdate = [row for row in sheet.rows if get_cell_by_column_name(row, "Approved?").display_value is None and get_cell_by_column_name(row, "Item or Task Description").display_value is not None]

        if rowsToUpdate != []:
          writeRows = []
          for row in rowsToUpdate:
            write_row = make_approved(row)
            writeRows.append(write_row)

          result = ss_client.Sheets.update_rows(sheetid, writeRows)

          for department in departments:
            writeRows = []
            for row in rowsToUpdate:
              write_row = make_start(row, department)
              writeRows.append(write_row)

            result = ss_client.Sheets.update_rows(sheetid, writeRows)

          for department in departments:
            writeRows = []
            for row in rowsToUpdate:
              write_row = make_finish(row, department)
              writeRows.append(write_row)

            result = ss_client.Sheets.update_rows(sheetid, writeRows)

        else:
          return None
