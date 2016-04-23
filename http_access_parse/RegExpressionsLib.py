#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Vasiliy Ermilov, e-mail: inkz@xakep.ru, telegram: inkz1"


class LinuxAuthLogRegex(object):
    '''Regular expression for LinuxAuthLog'''

    #HOST ProcessName[PID]: Message
    TYPE_1 = r'([^:]*) (.*)\[(\d*)\]\: (.*)'

    #HOST ProcessName: Message
    TYPE_2 = r'([^:]*) ([^\s]*): (.*)'

    #Service Name: rest of the message
    MESSAGE_TYPE_1 = r'([^\s]*): (.*)'
    
    #List of regex for searching username in message
    MESSAGE_USER = (r'for.*\buser\s(\w+)', r'USER=(\w+)')
    
    #List of regex for searching IP in message
    MESSAGE_IP = (r'\bfrom\s(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)',)
    
    #List of regex for searching UID in message
    MESSAGE_UID = (r'\(uid=(\d*)\)',)
    
    #List of regex for searching command in message
    MESSAGE_COMMAND = (r'COMMAND=([^\]]*)',)
    
    #List of regex for searching cwd in message
    MESSAGE_CWD = (r'CWD=([^\]]*)',)

class LinuxBootLogRegex(object):
    '''Regular expression for LinuxAuthLog'''

    # 'Starting' expression
    TYPE_START = r'Starting (.*)\[(.*)\]'
    
    # 'Stopping' expression
    TYPE_STOP = r'Stopping (.*)\[(.*)\]'
    
class LinuxMessagesLogRegex(object):
    '''Regular expression for LinuxAuthLog'''
    
    TYPE_1 = r'(\w{3}\s{1,2}\d{1,2} \d{2}:\d{2}:\d{2}) ([^\s]*) ([^\s]*): (.*)'
    
class LinuxHttpdErrorLogRegex(object):
    '''Regular expression for LinuxHttpdErrorLog'''

    # [Date] [ErrorType] [PID] [AH] [Message]
    TYPE_1 = r'\[(.*)\] \[(.*)\] \[pid (\d*)\] (\w*): (.*)'
    # TYPE_DATE = r'(\w{3} \w{3} \d{2} \d{2}:\d{2}:.* \d{4})'
    
class LinuxHttpdAccessLogRegex(object):
    '''Regular expression for LinuxHttpdAccessLog'''
    
    #IP - - [Date] "RequestType Address Protocol" Status Length
    TYPE_1 = r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b) \[(.*)\] "(\w*) (.*) (.*)" (\d*) (\d*)'
    
class LinuxAuditLogRegex(object):
    '''Regular expression for LinuxAuditLog'''

    TYPE_1 = r'type=(.*) msg=(.*):\s'
    
    TYPE_2 = r'(syscall|success|pid|auid|uid|tty|ses|comm|exe|key|cwd|ouid|ogid)=([^\s]*)'
    
class LinuxDpkgLogRegex(object):
    '''Regular expression for LinuxDpkgLog'''
    
    #date action package_info
    TYPE_1 = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s(status|install|configure|trigproc|upgrade|remove|purge)\s(.*)'
    
    #status package_info
    TYPE_STATUS = r'(not-installed|config-files|half-installed|unpacked|half-configured|triggers-awaited|triggers-pending|installed)\s(.*)'