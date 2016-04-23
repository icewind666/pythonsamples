#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Vasiliy Ermilov, e-mail: inkz@xakep.ru, telegram: inkz1'

import os.path, re

class LogFinder():
	"""class for finding log file location in config files"""
	
	def iterateConfigs(self, rx, conf_locations, action):
		for path in conf_locations:
			if os.path.isfile(path) == True:
				return action(rx, path)
	
	def findEnvVar(self, variable): 
		def matchEnvPath(rx, path):
			for line in open(path):
				search = re.search(rx, line)
				if search != None:
					return search.group(1)
			return None
			
		result = self.iterateConfigs(r'export '+variable+r'=(.*)\$SUFFIX', ('/etc/apache2/envvars',), matchEnvPath)
		if result == None:
			result = self.iterateConfigs(r'export '+variable+r'=([^\s]*)', ('/etc/apache2/envvars',), matchEnvPath)
		return result
		
	def parseEnvVar(self, log_path):
		search = re.search(r'\${(.*)}', log_path)  # trying to figure out if log path contains env variable
		if search != None:
			env_path = self.findEnvVar(search.group(1)) # looking for env variable value
			if env_path != None:
				return re.sub(r'(\${.*})',env_path,log_path)
		return log_path
			
		

	def findLogLocation(self, rx, conf_path):
		log_path = None
		
		for line in open(conf_path):  #looking for a regex match with a log path declaration
			search = re.search(rx, line)
			if search != None:
				log_path = search.group(1)
				
		if log_path != None:
			log_path = self.parseEnvVar(log_path)
			log_path = re.sub(r'^"|"$', '', log_path) # get rid of double quotes if they exist
			if not os.path.isabs(log_path):  # trying to join paths if given log path is not absolute
				joined_log_path = os.path.join(os.path.dirname(conf_path),log_path)
				if not os.path.isfile(joined_log_path):
					joined_log_path = os.path.join(os.path.dirname(conf_path),'..',log_path)
					
				if os.path.isfile(joined_log_path):
					log_path = joined_log_path
			else:
				if not os.path.isfile(log_path):
					log_path = None
					
		return log_path

	def find(self,rx, conf_locations):  # main operation
		logs = []
		for path in conf_locations:
			if os.path.isfile(path) == True:  # checking for existing config file
				log_location = self.findLogLocation(rx, path)  # perform searching inside existing config
				if log_location != None:
					logs.append(log_location)
		return logs