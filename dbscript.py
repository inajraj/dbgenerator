import mysql.connector

def runScript(str):

    mydb = mysql.connector.connect(
            host="localhost",
            user="pma",
            passwd="pma",
            database="test"
        )

    mycursor = mydb.cursor()

    mycursor.execute(str)

    mydb.commit()



