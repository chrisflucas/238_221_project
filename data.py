import csv
import sys, os

'''
	Wrapper class for data reading, handling, etc.
'''
class DataUtil():
	def __init__(self):
		return None
	'''
		Takes in and parses a CSV file.
		Return: 
			rows - list of dicts, each dict represents a 
			row of data and maps from column names to data point value
	'''
	def read_file(self, infile, extract_school_names=False):
		def _format_row(r):
			return r.replace('$','').replace(',','').replace('.00', '')

		def _format_col(c):
			return c.replace('\"', '').replace(' ','-').lower()

		columns = []
		rows = []
		with open(infile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in reader:
				if not columns: columns = [_format_col(c) for c in row]
				else:
					rows.append({columns[i]: _format_row(c) for i, c in enumerate(row)})

		if extract_school_names: return self.extract_school_names(rows)
		return rows

	'''
		Extract school name from data and use that as a key that maps
		to school data. i.e. 'Stanford University' => {'median-pay': 1000, 'high-pay': ...}
	'''
	def extract_school_names(self, rows):
		return {dr['school-name']: dr for dr in rows}

if __name__ == '__main__':
	data_rows = read_file('data/salaries-by-college-type.csv')




