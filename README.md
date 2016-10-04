# CSTimetableConverter

## Installation

1. Clone or download repository

2. Within directory install requirements:

	```
	pip install -r requirements.txt
	```

3. Fill in calendar URL in `load_timetable.py` (available from MyManchester):

	```
	url = ''
	```

	The timetable widget can be found within on the MyManchester homepage:
	![Calendar Widget](./images/Timetable.png)


	The URL can be found in the edit section of the widget:
	![Calendar Widget](./images/URL.png)
	
4. Edit converted name:

	```
	'COMP25111':'Operating Systems',
	'COMP26120':'Algorithms and Imperitive Programming',
	'COMP28411':'Computer Networks'
	```
	
5. Run the script:

	```
	python load_timetable.py
	```
	
6. Import as a new calendar

7. Run regularly to ensure calendar remains up to date
