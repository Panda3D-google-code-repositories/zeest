'''
Created on Jun 9, 2012
@author: Josh
'''
from Message import Message
#iterparse may be faster than sax here
from xml.sax import parseString
from xml.sax.handler import ContentHandler 

xml_template = "<Message> \n\t<Type>%s</Type> \n\t<Source>%s</Source> \n\t<Destination>%s</Destination>  \n\t<Message>%s</Message>  \n\t<Timestamp>%s</Timestamp>  \n</Message>"

class XMLMessage(object):
    def __init__(self):
        self.xml = None
        self.message = Message()
        
    def from_xml(self, xml):
        self.xml = xml
        self.build_message()
        return self.message
        
    def from_message(self, message):
        self.message = message
        self.build_xml()
        return self
        
    def build_xml(self):
        self.xml = xml_template % (self.message.type, 
                                   self.message.source, 
                                   self.message.destination, 
                                   self.message.message, 
                                   self.message.timestamp,)
        
    def build_message(self):
        parseString(self.xml, XMLMessageHandler(self.message))
        
    def get_message(self): 
        return self.message
    
    def get_xml(self): 
        return self.xml
        
    def is_empty(self):
        return not (self.message.type or
                    self.message.source or
                    self.message.destination or
                    self.message.message or
                    self.message.timestamp)
        
    def __repr__(self):
        return self.xml or "empty XML message"
        
class XMLMessageHandler(ContentHandler):
    def __init__(self, message):
        self.message = message
        
        self.inType = False
        self.inSource = False
        self.inDestination = False
        self.inMessage = False
        self.inTimestamp = False
        
    def startElement(self, name, attrs):
        if name == 'Type': self.inType = True
        elif name == 'Source': self.inSource = True
        elif name == 'Destination': self.inDestination = True
        elif name == 'Message': self.inMessage = True
        elif name == 'Timestamp': self.inTimestamp = True
        
    def characters(self, chars):
        if self.inType:
            self.message.type = chars
            self.inType = False
        elif self.inSource:
            self.message.source = chars
            self.inSource = False
        elif self.inDestination:
            self.message.destination = chars
            self.inDestination = False
        elif self.inMessage:
            self.message.message = chars
            self.inMessage = False
        elif self.inTimestamp:
            self.message.timestamp = chars
            self.inTimestamp = False
        
if __name__ == '__main__':
    msg = Message("Sight Request", 
                  "Player 1", 
                  "Entity 14", 
                  "Player 1 wants to know if he can see Entity 14")
    print msg
    
    xmlMsg = XMLMessage().from_message(msg)
    print xmlMsg
    print XMLMessage().from_xml(xmlMsg.get_xml())
    
    
    
    
    