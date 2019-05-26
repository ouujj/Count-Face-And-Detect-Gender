import sqlite3

import datetime

class sqllitedb:
	
	def __init__(self):
		
		self.DBname  = 'Detect@'+ str(datetime.datetime.now()) + '.db'
		conn = sqlite3.connect(self.DBname) # You can create a new database by changing the name within the quotes
		c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
		# Create table - CLIENTS
		c.execute('''CREATE TABLE DETECT([generated_id] INTEGER PRIMARY KEY,[GENDER] text, [TimeStramp] text)''')       
		conn.commit()
		
		

	
	def insertDB(self,ID,GENDER):
		conn = sqlite3.connect(self.DBname)
		c = conn.cursor()
		c.execute("INSERT INTO DETECT VALUES ("+str(ID)+", '"+GENDER+"','"+str(datetime.datetime.now())+"') ")
		conn.commit()

	def showData(self):
	
		conn = sqlite3.connect(self.DBname)
		c = conn.cursor()
	
		for row in c.execute('SELECT * FROM DETECT ORDER BY generated_id'):
			print(row)

'''	
DB = sqllitedb()
DB.insertDB(1,"Man")
DB.insertDB(2,"Man")
DB.insertDB(3,"Man")

DB.showData()

# Note that the syntax to create new tables should only be used once in the code (unless you dropped the table/s at the end of the code). 
# The [generated_id] column is used to set an auto-increment ID for each record
# When creating a new table, you can add both the field names as well as the field formats (e.g., Text)
'''
