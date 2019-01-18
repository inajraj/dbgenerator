import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="pma",
        passwd="pma",
        database="test"
    )

mycursor = mydb.cursor()

str = """CREATE TABLE `WorkedHours` (`ID` int UNSIGNED NOT NULL AUTO_INCREMENT,`EmpID` int(5) UNSIGNED NOT NULL,`Period` varchar(15) NOT NULL,`From` date NOT NULL,`To` date NOT NULL,`TotalUnits` int(3) UNSIGNED DEFAULT 0,`WorkedUnits` int(3) UNSIGNED DEFAULT 0,`LeaveUnits` int(3) UNSIGNED DEFAULT 0,`LOPUnits` int(3) UNSIGNED DEFAULT 0,`PrevPeriodUnits` int(3) UNSIGNED DEFAULT 0,PRIMARY KEY (`ID`))"""

mycursor.execute(str)

