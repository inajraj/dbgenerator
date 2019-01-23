from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import mysql.connector

from dateUtils import convertdate
from dbscript import runScript

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1WmIHC5ic4IFE4b5uEXgfxEXm1GW-I7aW80xKS7rDcsA'
RANGE_NAME = 'Tables'

mydb = mysql.connector.connect(
        host="localhost",
        user="pma",
        passwd="pma",
        database="test"
    )

mycursor = mydb.cursor()

def formFieldString(row):
    #get the row and form the field it could have the size or not a
    #also not null or not as well as primary key
    #all the int we need to automatically add unsigned
    #we also need to add auto_increment for the fields 'ID'
    finalStr = ""
    if (row[0]  == "ID"):
        finalStr = "`ID` "+ row[1] + ","
        return finalStr

    # need to see size is there or not
    

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for metaRow in values:
            res=sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=metaRow[0]).execute()
            tablerows = res.get('values', [])
            print(metaRow[0])
            if (metaRow[1] == 'Y'):
                #create the table only if the indicator is Y
                #drop the table first
                str = "DROP TABLE IF EXISTS " + metaRow[0]
                mycursor.execute(str)
                finalStr = "CREATE TABLE `" + metaRow[0] + "` ("
                for tdrow in tablerows:
                    
                    finalStr  = finalStr + "`" + tdrow[0] + "` " + tdrow[1] + ","
                    print(tdrow)
                    
                    #check this row has primary key column
                    if ('PK' in tdrow[2]):
                        pkString = "PRIMARY KEY (`" + tdrow[0] + "`))"
                #need to add primary key - to check the loop again
                mycursor.execute(finalStr+pkString)
                print(finalStr+pkString)
            if (metaRow[2] == 'Y'):
                #load sample data 
                #truncate tables
                runScript("TRUNCATE TABLE `" + metaRow[0] + "`")

                #range name will be TableName.SampleData
                DataRange = metaRow[0] + ".SampleData"
                res=sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=DataRange).execute()
                dataRows = res.get('values', [])
                
                #get the columns (max columns will do)
                nColumns = max(list(map(len,dataRows)))
                print(nColumns)
                queryList = []
                for i in range(nColumns):
                    instr = "INSERT INTO `" + metaRow[0] + "` ("
                    valstr = "VALUES ("
                    for fld in zip(tablerows,dataRows): # tuple of two lists
                        if i < len(fld[1]): #check if the second list has members for index i
                            if fld[1][i] != '' and 'ID' not in fld[1][i]: #it it is empty do not add the field
                                instr = instr + fld[0][0] + ","
                                if fld[0][2] == 'D':
                                    valstr = valstr + "'" +  convertdate(fld[1][i]) + "',"
                                else:
                                    valstr = valstr + "'" +  fld[1][i] + "',"
                    qStr = instr[:-1]+") " + valstr[:-1] + ")"
                    runScript(qStr)
                    print(qStr)

if __name__ == '__main__':
    main()