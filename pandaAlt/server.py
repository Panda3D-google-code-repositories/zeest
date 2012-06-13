from pandac.PandaModules import *
import direct.directbase.DirectStart
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

PORT = 9099

MSG_NONE            = 0
CMSG_AUTH           = 1
SMSG_AUTH_RESPONSE  = 2
CMSG_CHAT           = 3
SMSG_CHAT           = 4
CMSG_DISCONNECT_REQ = 5
SMSG_DISCONNECT_ACK = 6

CLIENTS = {}

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

    def readTask(self, task):
        while 1:
            (datagram, data, msgID) = self.nonBlockingRead(self.cReader)
            if msgID is MSG_NONE:
                break
            else:
                self.handleDatagram(data, msgID,datagram.getConnection())
               
        return Task.cont

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

    def handleDatagram(self, data, msgID, client):
        if msgID in Handlers.keys():
            Handlers[msgID](msgID,data,client)
        else:
            print "Unknown msgID: %d" % msgID
            print data
        return

    def msgAuth(self, msgID, data, client):
        username = data.getString()
        password = data.getString()
       
        flag = 1
        CLIENTS[username] = 1
        print "User: %s, logged in with pass: %s" % (username,password)
        pkg = PyDatagram()
        pkg.addUint16(SMSG_AUTH_RESPONSE)
        pkg.addUint32(flag)
        self.cWriter.send(pkg,client)

    def msgChat(self, msgID, data, client):
        print "ChatMsg: %s" % data.getString()

    def msgDisconnectReq(self, msgID, data, client):
        pkg = PyDatagram()
        pkg.addUint16(SMSG_DISCONNECT_ACK)
        self.cWriter.send(pkg,client)
        del CLIENTS[client]
        self.cReader.removeConnection(client)

    def quit(self):
        self.cManager.closeConnection(self.tcpSocket)
        sys.exit()

serverHandler = Server()
Handlers = {
    CMSG_AUTH           : serverHandler.msgAuth,
    CMSG_CHAT           : serverHandler.msgChat,
    CMSG_DISCONNECT_REQ : serverHandler.msgDisconnectReq,
    }

run() 