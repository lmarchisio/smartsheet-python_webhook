# smartsheet-python_webhook
The goal of this work is to fix the occasional Smartsheet issue where users add data in a blank row that is between several other blank rows.  When this occurs Smartsheet not to Autofill is not triggered.  This creates a common problem where formulas (possibly hidden) that admins or other users rely on for data collection, or other back end work, do not get copied from rows above or below the new row.  

A common work around to solve this problem is the blank report.  This collects all lines where the cell that would normally have the required formula are blank.  When something shows up in the blank report, the admin knows the formula was not copied and can go correct the error.  

However, a more ideal solution would be for Smartsheet to "listen for" these blank lines and fill in the necessary formulas whenever a change occurs that creates a blank line.  This can be achieved by using the Smartsheet API webhook functionality to trigger a Google Cloud Function which can then find and fill the blank cells.  

## Requirements
* Google Cloud Account
* Smartsheet Python SDK

## Goals/Proof of Concept
- [x] Successfully establish a webhook between Smartsheet test sheet and Hello World Google Cloud Function
- [x] Write a base case Google Cloud function that succesfully changes an existing sheet when manually triggered (create new column in test sheet)
- [ ] Rewrite 
