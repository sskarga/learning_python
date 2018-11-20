# Реализация простого класса для чтения из файла
import sys

class FileReader:
	""" Реализация простого класса для чтения из файла """

	def __init__(self, file_name = None):
		self._file_name = file_name

	@property
	def file_name(self):
		return self._file_name

	@file_name.setter
	def file_name(self, value):
		self._file_name = value

	def read(self):

		result = ""

		if self._file_name is not None:
			try:
				with open(self._file_name, 'r') as f:
					result = f.read()
			except IOError as e:
   				print("Cannot open file: {0}. I/O error({1}): {2}".format(self._file_name, e.errno, e.strerror))  
			except: #handle other exceptions such as attribute errors
   				print("Cannot open file: {0}. Unexpected error: {1}".format(self._file_name, sys.exc_info()[0]))  
		else:
			print("File name: None. Set file name.")

		return result


reader = FileReader("example1.txt")
print(reader.read())