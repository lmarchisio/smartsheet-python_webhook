# smartsheet-python_webhook
The goal of this work is to fix the occasional Smartsheet issue where users add data in a blank row that is between several other blank rows.  When this occurs Smartsheet Autofill is not triggered.  This creates a common problem where formulas that admins or other users rely on for data collection, or other back end work, do not get copied from rows above or below the new row.  

A common work around to solve this problem is the blank report.  This collects all lines where the cell that would normally have the required formula are blank.  When something shows up in the blank report, the admin knows the formula was not copied and can go correct the error.  

However, a more ideal solution is for Smartsheet to "listen for" these blank lines and fill in the necessary formulas whenever a change occurs that creates a blank line.  This can be achieved by using the Smartsheet API webhook functionality to trigger a Google Cloud Function which can then find and fill the blank cells.  

The basic concept:
1. Each open project sheet has a webhook that listens for any change
2. When a change is detected, an HTTP trigger is sent to the cloud function URL
3. The cloud function checks for any blank lines and writes formulas into any admin columns with blank cells

Note that lines 73-90 in main.py are used to capture each webhook callback and save them to an additional smartsheet.  If you do not wish to use this functionality comment out or delete these lines and omit steps 2 and 5 of the setup.

## Requirements
- [Google Cloud Computing Account](https://cloud.google.com/)
- [Smartsheet Python SDK](https://github.com/smartsheet-platform/smartsheet-python-sdk)

## Setup
1. [Create a new Google Cloud Function using the Python runtime](https://cloud.google.com/functions/docs/quickstart-console)
2. Upload the spreadsheet ```Webhook Log.xls``` to Smartsheet
3. Copy ```main.py``` and ```requirements.txt``` to the source tab
4. In the **function to execute** field change *hello_world* to *smartsheet_webhook_responder*, or change the function name in ```main.py``` to *hello_world* (exact names are actually irrelevant as long as the **function to execute** field matches the function name in ```main.py```
5. Change the sheet ID and column IDs in lines 73-90 to match up with corresponding IDs from the newly uploaded Webhook Log
6. Create a webhook from the desired sheet to the cloud function trigger URL
7. Update the webhook to enabled = true
8. Adjust Google Function memory allocation and timeout as needed

## Dashboard
Google Cloud Computing resource use metrics, billing data and log files from Cloud Functions may be exported to BigQuery for importation as data sources in Google Data Studio reports.  Data Studio reports can then be embedded in Smartsheet Dashboards to allow simultaneous monitoring of Smartsheet and Google Cloud metrics.  

1. [Export Google billing data to BigQuery] (https://cloud.google.com/billing/docs/how-to/export-data-bigquery)
2. [Export log files to BigQuery] (https://cloud.google.com/logging/docs/export/configure_export_v2)
3. [Connect Data Studio to BigQuery data sources] (https://cloud.google.com/bigquery/docs/visualize-data-studio)
4. Create charts and reports
5. Embed reports in Smartsheet dashboard using a web content widget

## Example Dasboard Reports

### Usage and Cost Bar Chart

### Projected Billing Table

### Log Files Counter

## Troubleshooting
- ```webhooks_list.py``` lists all webhooks to find those that are not enabeled or NOT_VERIFIED

## Proof of Concept
- [x] Successfully establish a webhook between Smartsheet test sheet and Hello World Google Cloud Function
- [x] Write a base case Google Cloud function that succesfully changes an existing sheet when manually triggered (create new column in test sheet)
- [x] Create a base case where Smartsheet alerts Google Cloud function to a change in a single sheet and then Google Cloud Function creates a column in that single sheet (essentially combine the two steps above)
- [x] Rewrite ```admin_refresh.py``` to check for blank lines and find/update cells rather than brute force rewriting all the admin columns
- [x] Figure out how to get the webhook to tell the Cloud Function which sheet to run on (get the cloud function to alter the sheet it acts on based on the ```scopObjectID``` delivered by the webhook). 

## Prototyping
- [x] Complete base usable case, update Approved? column with correct formua for all lines where Approved? and Item/Task Description are blank whenever sheet is changed
- [x] Complete next case which updates Approved? and a pair of department Start/Finish Columns (considered second stage gate b/c of nested loops in the original ```admin_refresh.py```) decide between writing a multi step function and creating additional webhooks and functions for each admin column
- [x] Complete next case which updates all columns based on previous stage decisions.  If all work is being done by a single function at this point, review run time using a copy of an existing large project sheet.  Currently, manually running ```admin_refresh.py``` on large projects takes approx 90 seconds.  
- [x] Enable webhook/function on a few projects and monitor invocation rate

## Deployment
- [x] Deploy to all active sheets
- [x] Update project close documentation to include deletion of webhooks
- [x] Update ```start_new_project.py``` to include the creation of webhooks (and possibly the enableing of webhooks)
- [x] Add monitoring of cloud function invocation rate to Smartsheet manual (daily task)

## Useful References
- [Google Cloud Functions Quick Start](https://cloud.google.com/functions/docs/quickstart-console)
- [Specifying Dependencies in Google Cloud Functions](https://cloud.google.com/functions/docs/writing/specifying-dependencies-python)
- [Smartsheet API Webhooks Reference](https://smartsheet-platform.github.io/api-docs/#webhooks-reference)
