# smartsheet-python_webhook
The goal of this work is to fix the occasional Smartsheet issue where users add data in a blank row that is between several other blank rows.  When this occurs Smartsheet Autofill is not triggered.  This creates a common problem where formulas (possibly hidden) that admins or other users rely on for data collection, or other back end work, do not get copied from rows above or below the new row.  

A common work around to solve this problem is the blank report.  This collects all lines where the cell that would normally have the required formula are blank.  When something shows up in the blank report, the admin knows the formula was not copied and can go correct the error.  

However, a more ideal solution would be for Smartsheet to "listen for" these blank lines and fill in the necessary formulas whenever a change occurs that creates a blank line.  This can be achieved by using the Smartsheet API webhook functionality to trigger a Google Cloud Function which can then find and fill the blank cells.  

The basic concept:
1. Each open project sheet has a webhook that listens for any change
2. When a change is detected, an HTTP trigger is sent to the cloud functions URL
3. The cloud function checks for any blank lines and writes formulas into any admin columns with blank cells

## Requirements
* Google Cloud Account
* Smartsheet Python SDK

## Goals/Proof of Concept
- [x] Successfully establish a webhook between Smartsheet test sheet and Hello World Google Cloud Function
- [x] Write a base case Google Cloud function that succesfully changes an existing sheet when manually triggered (create new column in test sheet)
- [ ] Create a base case where Smartsheet alerts Google Cloud function to a change in a single sheet and then Google Cloud Function creates a column in that single sheet (essentially combine the two steps above)
- [ ] Rewrite admin_refresh.py to check for blank lines and find/update cells rather than brute force rewriting all the admin columns
- [ ] Figure out how to get the webhook to tell the Cloud Function which sheet to run on (get the cloud function to alter the sheet it acts on based on the scopObjectID delivered by the webhook). 

## Useful References
- [Google Cloud Functions Quick Start](https://cloud.google.com/functions/docs/quickstart-console)
- [Specifying Dependencies in Google Cloud Functions](https://cloud.google.com/functions/docs/writing/specifying-dependencies-python)
- [Smartsheet API Webhooks Reference](https://smartsheet-platform.github.io/api-docs/#webhooks-reference)
