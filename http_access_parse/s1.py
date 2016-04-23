#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Vasiliy Ermilov, e-mail: inkz@xakep.ru, telegram: inkz1'


import re, hashlib, logging, logging.handlers, logging.config, os.path
from tqdm import *
from Database import SqlDataBase
from Filereader import File
from sys import argv, exit, stdout
from RegExpressionsLib import LinuxHttpdAccessLogRegex
from MessagesLib import Messages
from LogFinder import LogFinder


class LinuxHttpdAccessLogParser(object):
    def __init__(self):
        confdir = os.path.join(os.path.dirname(__file__), '/config/logging.conf')
        self.db = SqlDataBase('LinuxHttpdAccessLog',
                              "(Logpath TEXT, IP TEXT, Date TEXT, RequestType TEXT, Address TEXT, Protocol TEXT, Status TEXT, Length TEXT)", "(?,?,?,?,?,?,?,?)")
        # Messages library initialization
        self.Messages = Messages('EN')

        #logging.config.fileConfig(confdir)  # Loading log config file and creating logger
        self.logger = logging.getLogger(__name__)


    def parse(self, line):
        
        # empty parts of result
        result = {
            "IP" : "None",
            "Date" : "None",
            "RequestType" : "None",
            "Address" : "None",
            "Protocol" : "None",
            "Status" : "None",
            "Length" : "None"
        }

        # trying to find matches in line
        match = re.match(LinuxHttpdAccessLogRegex.TYPE_1, line)
        if match != None:
           result["IP"] = match.group(1)
           result["Date"] = match.group(2)
           result["RequestType"] = match.group(3)
           result["Address"] = match.group(4)
           result["Protocol"] = match.group(5)
           result["Status"] = match.group(6)          
           result["Length"] = match.group(7)                               
        else:
           return 0
        
        return [ result["IP"], result["Date"], result["RequestType"], result["Address"], result["Protocol"], result["Status"], result["Length"] ]

    
    def logFileSearcher(self):
        conf_locations = ("/usr/local/etc/apache22/httpd.conf",
			"/etc/apache2/apache2.conf",
            "/etc/httpd/conf/httpd.conf",
			"/opt/lampp/etc/httpd.conf")
            
        rx = r'CustomLog\s*"(.*)"'
        lf = LogFinder()
        return lf.find(rx, conf_locations)
            
    
    def reader(self):
       total_lines = 0  # Parsed lines
       missed_lines = 0  # Missed lines (didn't match any pattern)

       #logs = self.logFileSearcher()
       logs = ['access.log.25', 'access.log.26', 'access.log.27', 'access.log.28', 'access.log.29']
       
       for log in logs:
            if log == None or os.path.isfile(log) != True:  # Check if log exists
                self.logger.error(self.Messages.get('LogOpenError').format('LinuxHttpdAccessLog'))
                print 'LogOpenError:'+log
                continue
            else:
                f = File(log)
        
            last_position = self.db.db_read_lp(log)  # Read last position in log
            if last_position == None:  # If reading log for the first time
                last_position = 0
            else:
                if f.cur_position() == last_position:  # Check if there were any changes since last read
                    self.logger.info(self.Messages.get('NoChanges').format('LinuxHttpdAccessLog'))
                    print 'NoChanges'
                    continue
        
            for line in tqdm(f.head(last_position)):  # Reading file line by line
                line = line.decode('utf8')
                result = self.parse(line)
                #print 'LINE:',line
                #print 'RESULT:',result
                if result == 0:  #Line didn't meet any pattern
                    missed_lines += 1
                    self.logger.warning(self.Messages.get('SkippedLine').format(line.encode('utf8'), 'LinuxHttpdAccessLog'))
                    #print 'skipped lines',missed_lines
                    continue
                else:
                    self.db.db_write([log]+result)  #Recording to DB
                    total_lines += 1
                    #print 'Total lines:',total_lines
        
            self.db.db_write_lp(f.cur_position(),log)  # Update current position
            self.logger.info(self.Messages.get('QtyScannedLines').format(total_lines, 'LinuxHttpdAccessLog'))
            self.logger.info(self.Messages.get('QtyMissedLines').format(missed_lines, 'LinuxHttpdAccessLog'))

       return 'SystemOK'

    def idmef_report_create(self):
       r = self.db.db_read()
       if r == 'DBEmpty': #Check if DB has any info in it
          return 'DBEmpty'
       else:
          return 'SystemOK'


if (__name__ == "__main__"):
    p = LinuxHttpdAccessLogParser() 
    r = p.reader()
    print r
    if len(argv) > 1:
        if argv[1] == 'REPORT_CREATE':
            p.idmef_report_create()