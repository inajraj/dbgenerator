import datetime

def convertdate(str):
     date_object = datetime.datetime.strptime(str, '%m/%d/%Y')
     return date_object.strftime('%Y-%m-%d')




