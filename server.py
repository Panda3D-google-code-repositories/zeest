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
        self.factory.clientConnectionMade(self)

    def proto_init(self, data):
        print data
        if data=="Login:":
            return 'user'
        elif data=="Register:":
            return 'registerUser'
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
        
    def proto_registerUser(self, data):
        global user
        user=data
        return 'registerPass'
        
    def proto_registerPass(self, data):
        global password
        password=data
        return 'register'
        
    def proto_register(self, data):
        global user, password, con, cur
        con=sqlite.connect('users.sqlite')
        cur=con.cursor()
        user= "'" + str(user) + "'"
        password=str(password)
        sql="""insert into users (username, password) values (%s, %s);""" % \
                (str(user), str(password))
        cur.execute(sql)
        con.commit()
        con.close()
        return 'init'
        
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
                sql="""SELECT * FROM enemies"""
                cur.execute(sql)
                info=cur.fetchall()
                continuea=True
                enemycount=0
                while continuea == True:
                    try:
                        self.sendString("Enemy")
                        self.sendString(str(info[enemycount][0]))
                        self.sendString(str(info[enemycount][1]))
                        self.sendString(str(info[enemycount][2]))
                        self.sendString(str(info[enemycount][3]))
                        self.sendString(str(info[enemycount][4]))
                        self.sendString(str(info[enemycount][5]))
                        self.sendString(str(info[enemycount][6]))
                        enemycount += 1
                    except IndexError:
                        continuea = False
                return 'loggedin'
                
            else:
                self.sendString("inv")
            	return 'init'
                
        except IndexError:
            self.sendString("inv")
            return 'init'
        
    def proto_loggedin(self, data):
        if data=="chat":
            return 'chat'
        if data == "moved":
            return 'moved';
        else:
            print data
            return 'loggedin'

    def proto_chat(self, data):
        global clients
        for client in clients:
            client.sendString("chat")
            client.sendString(user.strip("'") + ": " + data)
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
    def clientConnectionMade(self, client):
        global clients
        clients.append(client)
        
    def clientConnectionLost(self, client):
        global clients
        clients.remove(client)
  

def main():
    re=redir()
    reactor.listenTCP(5000,re)
    reactor.run()

if __name__ == '__main__':
    main()
