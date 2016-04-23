#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Artem Ivashchenko, e-mail: art.ivaschenko@yahoo.com, telegram: art_ivaschenko"

class File(file):
	""" Filereader class (inherited from standard file class). Used to read large files to not overload the memory.  """

	def __init__(self, *args, **kwargs):
		super(File, self).__init__(*args, **kwargs)
		self.BLOCKSIZE = 32 #Has to be less than minimum length of a string

	#Reading from the begining of file, yielding line by line, this one is used right now
	def head(self, last):

		self.seek(last) 
		while True:
			line = super(File, self).next()
			yield line

	#Reading from the end by BLOCKSIZE
	def tail(self, lines_2find=1):

		self.seek(0, 2)                   
		bytes_in_file = self.tell()
		lines_found, total_bytes_scanned = 0, 0
		while (lines_2find + 1 > lines_found and
			   bytes_in_file > total_bytes_scanned): 
			byte_block = min(
				self.BLOCKSIZE,
				bytes_in_file - total_bytes_scanned)
			self.seek( -(byte_block + total_bytes_scanned), 2)
			total_bytes_scanned += byte_block
			lines_found += self.read(self.BLOCKSIZE).count('\n')
		self.seek(-total_bytes_scanned, 2)
		line_list = list(self.readlines())
		return line_list[-lines_2find:]

	#Reading from end to the very begining
	def backward(self, last):
		
		self.seek(0, 2)                     
		blocksize = self.BLOCKSIZE
		last_row = ''
		while self.tell() > last:
			try:
				self.seek(-blocksize, 1)
			except IOError:
				blocksize = self.tell()
				self.seek(-blocksize, 1)
			block = self.read(blocksize)
			self.seek(-blocksize, 1)
			rows = block.split('\n')
			rows[-1] = rows[-1] + last_row
			while rows:
				last_row = rows.pop(-1)
				if rows and last_row:
					yield last_row
		yield last_row

	#Return file size in bytes
	def cur_position(self):

		self.seek(0, 2)
		return self.tell()

#For test purposes
if (__name__ == "__main__"):
	f = File("/var/log/system.log")
	#print f.head(5)
	#print f.tail(5)
	for line in f.head():
		print f.tell()
	print "!!! {}".format(f.cur_position())

