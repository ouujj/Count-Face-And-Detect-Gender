
import datetime
from firebase import firebase

import time
import  urllib, http.client
import json
import os 

firebaseURL = 'https://peoples-and-gender-count.firebaseio.com/'

firebase = firebase.FirebaseApplication(firebaseURL, None)


def update_firebase(ID,gender):
	
	try:
		#start_time = time.time()
		data = { "timestramp":datetime.datetime.now(),"ID": ID, "Gender": gender}
		firebase.post('/Conut/people', data)
		#print("Totle time to update ",time.time()-start_time)
	except Exception as e: 
		print("Can't update Firebase with exception:"+str(e) )	
		
	
	
