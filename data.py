import csv
import sys, os
import datetime

'''
	Wrapper class for data reading, handling, etc.
'''
class DataUtil():
	def __init__(self):
		self.data = {}
		return None
	'''
		Takes in and parses a CSV file.
		Return: 
			rows - list of dicts, each dict represents a 
			row of data and maps from column names to data point value
	'''
	def read_file(self, filePath):
		with open(filePath) as f:
			reader = csv.reader(f)
			rowNum = 0
			headers = []
			dataMap = {}
			for row in reader:
				rowNum+=1
				if rowNum == 1:
					for x in range(0, len(row)): headers.append(row[x])
					continue
				date = row[0].split()
				curDate = date[0].split('-')
				dtObject = datetime.date(int(curDate[0]), int(curDate[1]), int(curDate[2]))
				dataMap[dtObject] = {}
				for x in range(1, len(row)):
					try:
						float(row[x])
						dataMap[dtObject][headers[x]] = float(row[x])
					except ValueError:
						print row[x]
		return dataMap

	'''
		Extract school name from data and use that as a key that maps
		to school data. i.e. 'Stanford University' => {'median-pay': 1000, 'high-pay': ...}
	'''
	def extract_school_names(self, rows):
		return {dr['school-name']: dr for dr in rows}

if __name__ == '__main__':
	data_rows = DataUtil()
	data_rows.read_file('/Users/charlesvidrine/Documents/CS 221/project/238_221_project/bitcoin_dataset.csv')
