'''
Created on Jun 9, 2012
@author: Josh
'''

from time import time

class Message(object):
    def __init__(self, type=None, source=None, destination=None, message=None):
        self.type = type
        self.source = source
        self.destination = destination
        self.message = message
        self.timestamp = int(round(time() * 1000))
        
    def __repr__(self):
        return "message \n type = %s \n source = %s \n destination = %s \n message = %s \n timestamp = %s" % \
            (self.type, self.source, self.destination, self.message, self.timestamp)