#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Artem Ivashchenko, e-mail: art.ivaschenko@yahoo.com, telegram: art_ivaschenko"

import sqlite3, os.path
import logging, logging.config, logging.handlers
from MessagesLib import Messages


class SqlDataBase(object):
	"""  SQLite class. Used to write data to DB (sqlite3). SQLite3 package need to be installed to use this.  
		 Creates the instance for the specific Log upon initialization.
	"""

	def __init__(self, log_name, columns, values): #Initialization, create table if not exists

		'''
		log_name = log name of DB to connect, columns = needed to create a table, 
		values = used to record something to DB
		'''
		self.Messages = Messages('EN') #Loading messages with language settings

		logdir = os.path.join(os.path.dirname(__file__) + 'logdb.log')

		self.logger = logging.getLogger(__name__) #Logging module initialization 
		self.logger.setLevel(logging.INFO)
		handler = logging.handlers.TimedRotatingFileHandler(logdir, when='midnight', interval=1)
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.info(self.Messages.get('DBInitComplete').format(log_name))

		#Queries initialization
		self.LOG_NAME = log_name
		self.INIT_QUERY = "select * from sqlite_master where name = '{}' and type='table'".format(log_name)
		self.CREATE_TABLE_QUERY = "create table '{}' {}".format(log_name, columns)
		self.INSERT_QUERY = "insert into '{}' values {}".format(log_name, values)
		self.READ_QUERY = "select * from '{}'".format(log_name)
		self.DROP_TABLE_QUERY = "drop table '{}'".format(log_name)
		self.CLEAR_TABLE_QUERY = "delete from '{}'".format(log_name)
		
		self.INITLP_QUERY = "select * from sqlite_master where name ='LastPosition' and type='table'"
		self.CREATE_TABLELP_QUERY = "create table LastPosition (Log TEXT, Position INT)"
		self.READ_LP_QUERY = "select Position from LastPosition where Log = '{}'"
		self.WRITE_LP_QUERY = "insert into LastPosition values (?,?)"
		self.UPDATE_LP_QUERY = "update LastPosition set Position = ? where Log = ?"

		db = sqlite3.connect("database") #Connecting to DB
		c = db.cursor()
		
		c.execute(self.INIT_QUERY) #Creating table for current Log
		if c.fetchone() == None:
			c.execute(self.CREATE_TABLE_QUERY)
			db.commit()
		
		c.execute(self.INITLP_QUERY) #Creating table for LastPosition storage
		if c.fetchone() == None:
			c.execute(self.CREATE_TABLELP_QUERY)
			db.commit()

		db.close()

	#Write record to DB
	def db_write(self, line):
		db = sqlite3.connect("database")
		c = db.cursor()
		c.execute(self.INSERT_QUERY, line)
		#self.logger.info(self.Messages.get('DBWrite').format(self.log_name))
		self.lrid = c.lastrowid - 1 #Getting last row ID here and saving it to class instance
		db.commit()
		db.close()

	#Read from DB and generate XML (IDMEF) report
	def db_read(self):		
		db = sqlite3.connect("database")
		c = db.cursor()
		xml_clear(self.LOG_NAME) #Delete everything for previous report
		c.execute(self.READ_QUERY)
		msg_id = 0 #Message ID
		self.logger.info(self.Messages.get('DBReadStart').format(self.LOG_NAME))
		if c.fetchone() == None: #If nothing in DB
			self.logger.info(self.Messages.get('DBEmpty').format(self.LOG_NAME))
			return 'DBEmpty'
		for row in c.fetchall():
			xml_parse(row, self.LOG_NAME, msg_id) #Parse the record from DB 
			msg_id += 1
		self.logger.info(self.Messages.get('DBReadFinish').format(self.LOG_NAME))
		db.close()
		return 'SystemOK'

	#If need to update any line in DB (if records in log are broken into several)
	def db_update(self, line):    
		
		#Queries used only in this function
		self.SELECT_MSG_QUERY = "select Msg from '{}' where rowid=%d".format(self.LOG_NAME)
		self.UPDATE_MSG_QUERY = "update '{}' set Msg = ? where rowid = ?".format(self.LOG_NAME)

		db = sqlite3.connect("database")
		c = db.cursor()
		if self.lrid == 0: #If DB table is empty
			return
		c.execute(self.SELECT_MSG_QUERY %self.lrid) #Read last record from DB
		lline = c.fetchone() #Save it to lline variable
		fline = "".join(lline) + line #Merge last record with new data
		c.execute(self.UPDATE_MSG_QUERY, (fline, self.lrid)) #Update the last record in DB with new information
		self.logger.info(self.Messages.get('DBUpdateRecord').format(self.LOG_NAME))
		db.commit()
		db.close()

	#Delete specific log's table from DB
	def db_table_delete(self):		
		db = sqlite3.connect("database")
		c = db.cursor()		
		c.execute(self.DROP_TABLE_QUERY)
		db.commit()
		self.logger.info(self.Messages.get('DBDeleteTable').format(self.LOG_NAME))
		db.close() 

	#Create specific log's table
	def db_table_create(self):		
		db = sqlite3.connect("database")
		c = db.cursor()		
		c.execute(self.CREATE_TABLE_QUERY)
		db.commit()
		self.logger.info(self.Messages.get('DBCreateTable').format(self.LOG_NAME))
		db.close() 

	#Delete all records in table
	def db_table_clear(self):
		db = sqlite3.connect("database")
		c = db.cursor()		
		c.execute(self.CLEAR_TABLE_QUERY)
		db.commit()
		self.logger.info(self.Messages.get('DBClearTable').format(self.LOG_NAME))
		db.close()

	#Check date in the log (used only in system.log parser)
	def db_date_check(self):		
		
		SELECT_DATE_QUERY = "select Date from '{}' where rowid=1".format(self.LOG_NAME)

		db = sqlite3.connect("database")
		c = db.cursor()	
		c.execute(SELECT_DATE_QUERY)
		date = c.fetchone()
		db.close() 
		if date:
			return date
		else:
			return None

	#Record last log position (to continue reading from last stop)
	def db_write_lp(self, inp, log=None):
		LOGNAME = self.LOG_NAME
		if log:
		    LOGNAME = log
		db = sqlite3.connect("database")
		c = db.cursor()

		c.execute(self.READ_LP_QUERY) #Try to read LastPosition for the log
		if c.fetchone() == None: #If nothing there
			c.execute(self.WRITE_LP_QUERY, (LOGNAME, inp)) #Write new LastPosition for the log
			self.logger.info(self.Messages.get('DBWriteLP').format(LOGNAME))
		else:
			c.execute(self.UPDATE_LP_QUERY, (inp, LOGNAME)) #Update LastPosition with new number
			self.logger.info(self.Messages.get('DBUpdateLP').format(LOGNAME))
		db.commit()
		db.close()

	#Read last log position
	def db_read_lp(self,log=None):
		LOGNAME = self.LOG_NAME
		if log:
		    LOGNAME = log		
		db = sqlite3.connect("database")
		c = db.cursor()

		c.execute(self.READ_LP_QUERY.format(LOGNAME))
		self.logger.info(self.Messages.get('DBReadLP').format(LOGNAME))
		res = c.fetchone()
		if res == None: 
			return None
		return res[0]
		db.close()
		
class LastPositionDb(object):
	"""  SQLite class for keeping last position of log files """
	
	def __init__(self, db_name): #Initialization, create table if not exists

		self.db_name = db_name
		#Queries initialization
		self.INITLP_QUERY = "select * from sqlite_master where name ='LastPosition' and type='table'"
		self.CREATE_TABLELP_QUERY = "create table LastPosition (LogPath TEXT, Position INT)"
		self.READ_LP_QUERY = "select Position from LastPosition where LogPath = (?)"
		self.WRITE_LP_QUERY = "insert into LastPosition values (?,?)"
		self.UPDATE_LP_QUERY = "update LastPosition set Position = ? where LogPath = ?"

		db = sqlite3.connect(self.db_name) #Connecting to DB
		c = db.cursor()

		c.execute(self.INITLP_QUERY) #Creating table for LastPosition storage
		if c.fetchone() == None:
			c.execute(self.CREATE_TABLELP_QUERY)
			db.commit()

		db.close()

	#Record last log position (to continue reading from last stop)
	def db_write_lp(self, inp, log_path):
		db = sqlite3.connect(self.db_name)
		c = db.cursor()

		c.execute(self.READ_LP_QUERY, (log_path,)) #Try to read LastPosition for the log
		if c.fetchone() == None: #If nothing there
			c.execute(self.WRITE_LP_QUERY, (log_path, inp)) #Write new LastPosition for the log
		else:
			c.execute(self.UPDATE_LP_QUERY, (inp, log_path)) #Update LastPosition with new number
		db.commit()
		db.close()

	#Read last log position
	def db_read_lp(self, log_path):		
		db = sqlite3.connect(self.db_name)
		c = db.cursor()

		c.execute(self.READ_LP_QUERY, (log_path,))
		res = c.fetchone()
		if res == None: 
			return None
		return res[0]
		db.close()