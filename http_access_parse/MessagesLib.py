#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Artem Ivashchenko, e-mail: art.ivaschenko@yahoo.com, telegram: art_ivaschenko"

import os.path

class MessagesCodes(object):

	'''Agent messages'''
	HostInfo = 0
	LocalTime = 1
	LocalUsers = 2
	SystemOK = 3
	SystemFail = 4

	'''Parser messages'''
	QtyScannedLines = 5
	QtyMissedLines = 6
	LogOpenError = 7
	SkippedLine = 8
	NoChanges = 9

	'''DataBase messages'''
	DBInitComplete = 10
	DBWrite = 11
	DBReadStart = 12
	DBReadFinish = 13
	DBUpdateRecord = 14
	DBCreateTable = 15
	DBDeleteTable = 16
	DBWriteLP = 17
	DBUpdateLP = 18
	DBReadLP = 19
	DBEmpty = 20
	DBClearTable = 21


class Messages(object):

	def __init__(self, lang):
		
		confdir = os.path.join(os.path.dirname(__file__), 'config/')
		
		self.Lang = lang
		if self.Lang == 'RU':
			with open(os.path.join(confdir, 'messages_ru.conf')) as f:
				self.content = f.readlines()
		elif self.Lang == 'EN':
			with open(os.path.join(confdir, 'messages_en.conf')) as f:
				self.content = f.readlines()

		self.MessagesCodes = MessagesCodes()

	def get(self, message):

		if message == 'HostInfo':
			return self.content[self.MessagesCodes.HostInfo].rstrip('\n')

		if message == 'LocalTime':
			return self.content[self.MessagesCodes.LocalTime].rstrip('\n')

		if message == 'LocalUsers':
			return self.content[self.MessagesCodes.LocalUsers].rstrip('\n')

		if message == 'SystemOK':
			return self.content[self.MessagesCodes.SystemOK].rstrip('\n')

		if message == 'SystemFail':
			return self.content[self.MessagesCodes.SystemFail].rstrip('\n')

		if message == 'QtyScannedLines':
			return self.content[self.MessagesCodes.QtyScannedLines].rstrip('\n')

		if message == 'QtyMissedLines':
			return self.content[self.MessagesCodes.QtyMissedLines].rstrip('\n')

		if message == 'LogOpenError':
			return self.content[self.MessagesCodes.LogOpenError].rstrip('\n')

		if message == 'SkippedLine':
			return self.content[self.MessagesCodes.SkippedLine].rstrip('\n')

		if message == 'NoChanges':
			return self.content[self.MessagesCodes.NoChanges].rstrip('\n')

		if message == 'DBInitComplete':
			return self.content[self.MessagesCodes.DBInitComplete].rstrip('\n')

		if message == 'DBWrite':
			return self.content[self.MessagesCodes.DBWrite].rstrip('\n')

		if message == 'DBReadStart':
			return self.content[self.MessagesCodes.DBReadStart].rstrip('\n')

		if message == 'DBReadFinish':
			return self.content[self.MessagesCodes.DBReadFinish].rstrip('\n')

		if message == 'DBUpdateRecord':
			return self.content[self.MessagesCodes.DBUpdateRecord].rstrip('\n')

		if message == 'DBCreateTable':
			return self.content[self.MessagesCodes.DBCreateTable].rstrip('\n')
			
		if message == 'DBDeleteTable':
			return self.content[self.MessagesCodes.DBDeleteTable].rstrip('\n')

		if message == 'DBWriteLP':
			return self.content[self.MessagesCodes.DBWriteLP].rstrip('\n')

		if message == 'DBUpdateLP':
			return self.content[self.MessagesCodes.DBUpdateLP].rstrip('\n')

		if message == 'DBReadLP':
			return self.content[self.MessagesCodes.DBReadLP].rstrip('\n')

		if message == 'DBEmpty':
			return self.content[self.MessagesCodes.DBEmpty].rstrip('\n')

		if message == 'DBClearTable':
			return self.content[self.MessagesCodes.DBClearTable].rstrip('\n')	