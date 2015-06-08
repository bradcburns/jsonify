import csv
import argparse
import json
import os

class Jsonifier(object):

	def __init__(self):
		self.InputFile = ''
		self.OutputFile = ''
		pass

	def _parse_cmd_line(self):
		StrProgDescription = ('A program that converts csv into JSON.')

		parser = argparse.ArgumentParser(description=StrProgDescription)

		parser.add_argument('--inputfile',
			'-i',
			required=True,
			help='path to .csv file to convert to json',
			dest='inputfile')

		parser.add_argument('--outputfile',
			'-o',
			help='export json to this location.',
			dest='outputfile')

		args = parser.parse_args()

		self.InputFile = args.inputfile

		self.OutputFile = args.outputfile

		return args

	def _verify_cmd_line(self):

		#verify file exists
		if not os.path.isfile(self.InputFile):
			print 'path does not exist: ' + self.InputFile
			return False

		if not self.OutputFile:
			self.OutputFile = os.path.splitext(self.InputFile)[0] + '.json'

		return True


	def ListOfDictsFromCSV(self,csvfile=''):

		ListOutput = []

		if not csvfile:
			csvfile = self.InputFile

		with open(csvfile, 'rb') as filo:

			print 'press enter to use a comma [,] as the delimiter.'
			delimiter = raw_input("what is the delimiter? [,] ")
			if not delimiter:
				delimiter = ','

			print 'assuming that the first row in the csv is headers.'		
			csvreader = csv.reader(filo, delimiter=delimiter)

			#grab headers
			ListHeaders = next(csvreader)

			#iterate through rest of csv
			for row in csvreader:
				#map headers to value in each row
				DictRow = dict(zip(ListHeaders,row))
				ListOutput.append(DictRow)


		return ListOutput

	def WriteJSONToFile(self,jsontowrite,outputfile=''):
		if not outputfile:
			outputfile = self.OutputFile

		print 'writing to ' + outputfile + '\n'

		with open(outputfile,'wb') as filo:
			StrWriteOut = json.dumps(jsontowrite)
			filo.write(StrWriteOut)

	def PrettyPrintJSON(self,JsonToPrint):
		print json.dumps(JsonToPrint, indent=4,sort_keys=True)

	def _run_from_cmd_line(self):
		self.args = self._parse_cmd_line()

		if not self._verify_cmd_line():
			raise Exception('a command line argument was entered incorrectly. '
				'perhaps a path you provided does not exist?')

		ListOfCSVDicts = self.ListOfDictsFromCSV()

		self.WriteJSONToFile(jsontowrite=ListOfCSVDicts)

		self.PrettyPrintJSON(ListOfCSVDicts)




if __name__ == "__main__":
	jfier = Jsonifier()
	jfier._run_from_cmd_line()


