import sqlite3 as sqlite
import twisted
from twisted.internet import reactor, protocol
from twisted.protocols.basic import StatefulStringProtocol, Int32StringReceiver

user=None
password=None
clients=[]
con=''
cur=''

class listen(StatefulStringProtocol,Int32StringReceiver,protocol.Protocol):

    def connectionMade(self):
        print str(self.transport.getPeer()) + "connected"
        self.sendString("connected")

    def proto_init(self, data):
        print data
        if data=="Login:":
            return 'user'
        else:
            return 'init'

    def proto_user(self, data):
        global user
        user=data
        return 'pass'
        
    def proto_pass(self, data):
        global password
        password=data
        return 'login'
        
    def proto_login(self, data):
        global user, password, con, cur
        con=sqlite.connect('users.sqlite')
        cur=con.cursor()
        user= "'" + str(user) + "'"
        password=str(password)
        sql="""SELECT password FROM users WHERE username=%s""" % \
                (user)
        cur.execute(sql)
        info=cur.fetchall()
        try:
            data=data[0][0]
            info=str(info[0][0])
            password=str(password)
            if password==info:
                print user +" logged in"
                self.sendString("logged in")
                query="""SELECT loc_x from users where username='chrisvj'"""
                cur.execute(query)
                self.sendString("Position")
                info=cur.fetchone()
                self.sendString(str(info[0]))
                query="""SELECT loc_y from users where username='chrisvj'"""
                cur.execute(query)
                info=cur.fetchone()
                self.sendString(str(info[0]))
                query="""SELECT loc_z from users where username='chrisvj'"""
                cur.execute(query)
                info=cur.fetchone()
                self.sendString(str(info[0]))
                sql="""SELECT name,loc_x,loc_y,loc_z FROM enemies"""
                cur.execute(sql)
                info=cur.fetchall()
                self.sendString(str(info[0][0]))
                self.sendString(str(info[0][1]))
                self.sendString(str(info[0][2]))
                self.sendString(str(info[0][3]))
                return 'loggedin'
                
            else:
                self.sendString("inv")
            	return 'init'
        except IndexError:
            print "invalid username/password"
            self.sendString("inv")
            return 'init'
        
    def proto_loggedin(self, data):
        if data=="chat":
            return 'chat'
        if data == "moved":
            return 'moved';
        else:
            return 'loggedin'

    def prot_chat(self, data):
        print "data"
        return 'loggedin'
        
    def proto_moved(self,data):
        query = """update users set loc_x=%s where username='chrisvj'""" % \
                (data)
        cur.execute(query)
        con.commit()
        return 'movedy'

    def proto_movedy(self,data):
        query = """update users set loc_y=%s where username='chrisvj'""" % \
                (data)
        cur.execute(query)
        con.commit()
        return 'movedz'
        
    def proto_movedz(self,data):
        query = """update users set loc_z=%s where username='chrisvj'""" % \
                (data)
        cur.execute(query)
        con.commit()
        return 'loggedin'

class redir(protocol.ServerFactory):
    protocol=listen
  

def main():
    re=redir()
    reactor.listenTCP(5000,re)
    reactor.run()

if __name__ == '__main__':
    main()
