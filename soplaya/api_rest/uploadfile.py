import csv
from api_rest.models import Report


def import_report():
	file_path = '/home/cristego3000/soplaya/api_rest/static/dataset.csv'
	with open(file_path, 'r') as file:
	    reader = csv.DictReader(file)
	    for row in reader:
	        Report.objects.create(
	            date = row['date'],
	            restaurant = row['restaurant'],
	            planned_hours = row['planned_hours'],
	            actual_hours = row['actual_hours'],
	            budget = row['budget'],
	            sells = row['sells']
	            )
