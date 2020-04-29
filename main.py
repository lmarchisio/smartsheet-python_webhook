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
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = column_map["Approved?"]
    new_cell.formula = '=IF(OR([Supervisor Confirmed]@row = 1, [PM Override]@row = 1), 1, 0)'

    new_row = smartsheet.models.Row()
    new_row.id = source_row.id
    new_row.cells.append(new_cell)
    return new_row

#def make_pm(source_row, pm):
#    new_cell = smartsheet.models.Cell()
#    new_cell.column_id = column_map["PM"]
#    new_cell.value = pm

#    new_row = smartsheet.models.Row()
#    new_row.id = source_row.id
#    new_row.cells.append(new_cell)

#    return new_row

def make_start(source_row, source_dept):
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = column_map[source_dept + " Start"]
    new_cell.formula = '=IF([Labor / Complete]@row = 0, IF([Dept.]@row = "' + source_dept + '", Start@row))'

    new_row = smartsheet.models.Row()
    new_row.id = source_row.id
    new_row.cells.append(new_cell)

    return new_row

def make_finish(source_row, source_dept):
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = column_map[source_dept + " Finish"]
    new_cell.formula = '=IF([Labor / Complete]@row = 0, IF([Dept.]@row = "' + source_dept + '", Finish@row))'

    new_row = smartsheet.models.Row()
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
        
#        row_map = {}
#        for row in sheet.rows:
#            row_map[row.row_number] = row
        
        # updating pm done here because it gums things up if executed below and because contact columns don't copy down like functions
#        pm_cell = get_cell_by_column_name(row_map[1], 'PM')
        
#        pm_rows = []
#        for row in sheet.rows:
#            if get_cell_by_column_name(row, 'PM').value is None:
#                pm_rows.append(make_pm(row, pm_cell.value))
        
#        updated_row = ss_client.Sheets.update_rows(
#            sheet.id,
#            pm_rows)

        # keep these as loops run on rowsToUpdate, running as individual test-then-write loops uses excess memory or time
        if rowsToUpdate != []:
            writeRows = []
            for row in rowsToUpdate:
                write_row = make_approved(row)
                writeRows.append(write_row)

            result = ss_client.Sheets.update_rows(sheetid, writeRows)

            if sheetid != 6507095957759876:
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
