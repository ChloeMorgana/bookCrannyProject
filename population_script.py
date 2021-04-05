import os

local_files = os.listdir()

if "data.json" in local_files and "manage.py" in local_files:
	print("manage.py and data.json found, running python manage.py loaddata data.json")
	os.system("python manage.py loaddata data.json")
else:
	print("manage.py or data.json not found - are you running this in the same directory as manage.py and data.json?")