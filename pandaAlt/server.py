from pandac.PandaModules import *
loadPrcFileData("", 'window-type none')

import direct.directbase.DirectStart
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import sqlite3 as sqlite

PORT = 9099

MSG_NONE            = 0
CMSG_AUTH           = 1
SMSG_AUTH_RESPONSE  = 2
CMSG_CHAT           = 3
SMSG_CHAT           = 4
CMSG_DISCONNECT_REQ = 5
SMSG_DISCONNECT_ACK = 6
MOVEMENT            = 7
POSITION            = 8

CLIENTS = {}
USERS={}
MOVECOUNTW={}
MOVECOUNTS={}
MOVECOUNTA={}
MOVECOUNTD={}

con=''
cur=''

class Server(DirectObject):

    def __init__(self):
       
        self.accept("escape", self.quit)
        self.lastConnection = None

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        self.tcpSocket = self.cManager.openTCPServerRendezvous(PORT, 1000)
        self.cListener.addConnection(self.tcpSocket)
        taskMgr.add(self.listenTask, "serverListenTask",-40)
        taskMgr.add(self.readTask, "serverReadTask", -39)
        taskMgr.add(self.move, "moveTask", -38)
        
    def handleDatagram(self, data, msgID, client):
        if msgID in Handlers.keys():
            Handlers[msgID](msgID,data,client)
        else:
            print "Unknown msgID: %d" % msgID
            print data
        return

    def listenTask(self, task):
        if self.cListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
           
            if self.cListener.getNewConnection(rendezvous,netAddress,newConnection):
                newConnection = newConnection.p()
                self.cReader.addConnection(newConnection)
                CLIENTS[newConnection] = netAddress.getIpString()
                self.lastConnection = newConnection
                print "Got a connection!"
            else:
                print "getNewConnection returned false"
        return Task.cont
        
    def move(self, task):
        return Task.cont
        
    def moving(self, msgID, data, client):
        key=data.getString()
        time=data.getFloat64()
        if key == 'w':
            num=MOVECOUNTW[client]
            num += time
            MOVECOUNTW[client]=num
        elif key == 's':
            num=MOVECOUNTS[client]
            num += time
            MOVECOUNTS[client]=num
            
        elif key == 'a':
            num=MOVECOUNTA[client]
            num += time
            MOVECOUNTA[client]=num
            
        elif key == 'd':
            num=MOVECOUNTD[client]
            num += time
            MOVECOUNTD[client]=num
            
        else:
            print "INVALID KEY! " + key
        
    def msgAuth(self, msgID, data, client):
        username = data.getString()
        password = data.getString()
        
        global con, cur
        
        con=sqlite.connect('users.sqlite')
        cur=con.cursor()
        user= "'" + str(username) + "'"
        password=str(password)
        sql="""SELECT password, loc_x, loc_y, loc_z FROM users WHERE username=%s""" % \
                (user)
        cur.execute(sql)
        info=cur.fetchall()
        try:
            info=str(info[0][0])
            password=str(password)
            if password==info:
       
                flag = 1
                CLIENTS[username] = 1
                USERS[client] = username
                print "User: %s, logged in with pass: %s" % (username,password)
                pkg = PyDatagram()
                pkg.addUint16(SMSG_AUTH_RESPONSE)
                pkg.addUint32(flag)
                self.cWriter.send(pkg,client)
                MOVECOUNTW[client]=0
                MOVECOUNTA[client]=0
                MOVECOUNTS[client]=0
                MOVECOUNTD[client]=0
                self.sendPos(username, client)
                
            else:
                flag = 2
                pkg = PyDatagram()
                pkg.addUint16(SMSG_AUTH_RESPONSE)
                pkg.addUint32(flag)
                self.cWriter.send(pkg, client)
                
        except IndexError:
            flag = 0
            pkg = PyDatagram()
            pkg.addUint16(SMSG_AUTH_RESPONSE)
            pkg.addUint32(flag)
            self.cWriter.send(pkg, client)

    def msgChat(self, msgID, data, client):
        print "ChatMsg: %s" % data.getString()

    def msgDisconnectReq(self, msgID, data, client):
        pkg = PyDatagram()
        pkg.addUint16(SMSG_DISCONNECT_ACK)
        self.cWriter.send(pkg,client)
        del CLIENTS[client]
        self.cReader.removeConnection(client)
        
    def nonBlockingRead(self,qcr):
        if self.cReader.dataAvailable():
            datagram = NetDatagram()
            if self.cReader.getData(datagram):
                data = PyDatagramIterator(datagram)
                msgID = data.getUint16()
            else:
                data = None
                msgID = MSG_NONE
        else:
            datagram = None
            data = None
            msgID = MSG_NONE
        return (datagram, data, msgID)
        
    def quit(self):
        self.cManager.closeConnection(self.tcpSocket)
        sys.exit()

    def readTask(self, task):
        while 1:
            (datagram, data, msgID) = self.nonBlockingRead(self.cReader)
            if msgID is MSG_NONE:
                break
            else:
                self.handleDatagram(data, msgID,datagram.getConnection())
               
        return Task.cont
        
    def sendPos(self, user, client):
        sql="""SELECT loc_x, loc_y, loc_z FROM users WHERE username=%s""" % \
                (("'" + user + "'"))
        cur.execute(sql)
        info=cur.fetchall()
    
        pkg = PyDatagram()
        pkg.addUint16(POSITION)
        pkg.addString(info[0][0])
        pkg.addString(info[0][1])
        pkg.addString(info[0][2])
        self.cWriter.send(pkg, client)

serverHandler = Server()

Handlers = {
    CMSG_AUTH           : serverHandler.msgAuth,
    CMSG_CHAT           : serverHandler.msgChat,
    CMSG_DISCONNECT_REQ : serverHandler.msgDisconnectReq,
    MOVEMENT            : serverHandler.moving,
    }

run() 