'''
Created on Jun 10, 2012
@author: Josh
'''
import sqlite3  # this should be enough to start testing, but with its locking process, it does not work well with client / servers apps

class DatabaseHandler(object):
    def __init__(self, filename='database.db'):
        self.filename = filename
        
        self.connected = False
        self.cursor = self.connection = None
        
        try:
            with open(filename) as _: pass
        except IOError as _:
            self.create_database()
        
    def connect(self):
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        self.connected = True
        return self.connected
    
    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connected = False
    
    def create_database(self):
        if self.connected or self.connect():
            self.cursor.execute("CREATE TABLE users (ID INTEGER PRIMARY KEY, characterIDs TEXT, username TEXT, password TEXT, email TEXT, lastLogin TEXT, lastLoginIP TEXT)")
            self.cursor.execute("CREATE TABLE characters (ID INTEGER PRIMARY KEY, classID INTEGER, inventoryID INTEGER, motionID INTEGER, abilityIDs TEXT, attributesID INTEGER, effectIDs TEXT, level INTEGER, experience INTEGER, name TEXT, gender TEXT, creationDate TEXT)")
            self.cursor.execute("CREATE TABLE class (ID INTEGER PRIMARY KEY, name TEXT, description TEXT)")
            self.cursor.execute("CREATE TABLE attributes (ID INTEGER PRIMARY KEY, currentHealth INTEGER, health INTEGER, currentMagic INTEGER, magic INTEGER, strength INTEGER, dexterity INTEGER, wisdom INTEGER, intelligence INTEGER)")
            self.cursor.execute("CREATE TABLE abilities (ID INTEGER PRIMARY KEY, name TEXT, description TEXT)")
            self.cursor.execute("CREATE TABLE effects (ID INTEGER PRIMARY KEY, name TEXT, description TEXT, duration INTEGER)")
            self.cursor.execute("CREATE TABLE motion (ID INTEGER PRIMARY KEY, acceleration_X FLOAT(4), acceleration_y FLOAT(4), acceleration_z FLOAT(4), position_x FLOAT(4), position_y FLOAT(4), position_z FLOAT(4), heading INTEGER, facing INTEGER)")
            
            self.cursor.execute("CREATE TABLE item (ID INTEGER PRIMARY KEY, name TEXT, description TEXT, value INTEGER, effectIDs TEXT, count INTEGER, slot INTEGER, equipped INTEGER)")
            self.cursor.execute("CREATE TABLE inventories (ID INTEGER PRIMARY KEY, itemIDs TEXT)")
            self.close()
            
    def is_user_registered(self, username):
        return not self.get_user_info(username) == None
    
    def get_user_info(self, username):
        if self.connected or self.connect():
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            entry = self.cursor.fetchone()
            self.close()
            
            if entry: return UserInfo(entry)
        return entry or None    
    
    def get_user_pass_match(self, username, password):
        pass
    
    def register_user(self, username, password, email):
        if username and password and email and not self.is_user_registered(username):
            if self.is_email_valid(email) and self.is_password_valid(password):
                if self.connected or self.connect():
                    print "Registering user %s" % username
                    self.cursor.execute("INSERT INTO users (username, password, email) values (?, ?, ?)", (username, password, email,))
                    self.close()
                    return True
        return False
    
    def is_email_valid(self, email):     # write the regex for this later
        return True
    
    def is_password_valid(self, password):
        return len(password) >= 7
            
class UserInfo(object):
    def __init__(self, tuple):
        self.id = tuple[0]
        
        self.characterIDs = None
        try:
            self.characterIDs = [int(x) for x in tuple[1].split(',')]
        except AttributeError as _:
            pass
        
        self.username = tuple[2]
        self.password = tuple[3]
        self.email = tuple[4]
        self.lastLogin = tuple[5]
        self.lastLoginIP = tuple[6]
        
class CharacterInfo(object):  # TODO
    def __init__(self, userInfo):
        pass
        
if __name__ == '__main__':
    handler = DatabaseHandler()
    info = handler.get_user_info('joshbyrom')
    if info:
        print info
    else:
        if handler.register_user('joshbyrom', '0123456', 'something@somewhere.com'):
            print handler.get_user_info('joshbyrom')
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            