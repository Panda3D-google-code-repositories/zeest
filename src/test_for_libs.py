'''
Created on Jun 7, 2012

@author: Josh
'''

if __name__ == '__main__':
    try:
        print "Importing a Panda3D module"
        from direct.showbase.ShowBase import ShowBase
        print " -- success"
    except:
        print "Panda3D is not installed!"
        
    try:
        print "Importing a Twisted module"
        from twisted.internet.protocol import Protocol
        print " -- success"
    except:
        print "Twisted is not installed!"
        
    try:
        print "Importing a PyCEGUI module"
        from PyCEGUI import *
        print " -- success"
    except:
        print "PyCEGUI is not installed!"