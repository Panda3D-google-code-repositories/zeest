#as this is multi-threaded, it currently must be exited by closing your terminal/resetting IDLE.

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.task import Task

import PyCEGUI
import PyCEGUIOpenGLRenderer

from twisted.internet import reactor,protocol
from twisted.protocols.basic import Int32StringReceiver, StatefulStringProtocol

import threading
import Queue



queue=Queue.Queue(-1)
prot = None
user=None
started=False
msg=None
username=None
password=None
boxItems=[]
loadPrcFileData('', 'show-frame-rate-meter #t')
loadPrcFileData('', 'sync-video #f')
x=1
logged=False
enemyNum=0
enemyLoc1=[]
enemyLoc2=[]
enemyLoc3=[]
loc=[]
newloc=[]
movecount=0

def loginClicked(user, password):
    global prot
    prot.sendString('Login:')
    prot.sendString(str(user))
    prot.sendString(str(password))
    
def gotProtocol(proto):
    global prot
    prot = proto
    
def loggedin():
    global queue
    global logged
    logged=True
    queue.put(lambda: PyCEGUI.WindowManager.getSingleton().destroyWindow("Root"))
    
def movement():
    global loc
    prot.sendString("moved")
    prot.sendString(str(loc[0]))
    prot.sendString(str(loc[1]))
    prot.sendString(str(loc[2]))
    loc=[]
    
def inv():
    global queue
    queue.put(lambda: PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Incorrect").setProperty("Visible", "True"))

class PandaCEGUI(object, DirectObject):
    buttons = {
        'mouse1': PyCEGUI.MouseButton.LeftButton,
        'mouse2': PyCEGUI.MouseButton.RightButton,
        'mouse3': PyCEGUI.MouseButton.MiddleButton,
        'mouse1-up': PyCEGUI.MouseButton.LeftButton,
        'mouse2-up': PyCEGUI.MouseButton.RightButton,
        'mouse3-up': PyCEGUI.MouseButton.MiddleButton,
        'wheel_up': PyCEGUI.MouseButton.NoButton,
        'wheel_down': PyCEGUI.MouseButton.NoButton,
    }
   
    keys = {
        'a': (PyCEGUI.Key.Scan.A, 'a', 'A'),
        'b': (PyCEGUI.Key.Scan.B, 'b', 'B'),
        'c': (PyCEGUI.Key.Scan.C, 'c', 'C'),
        'd': (PyCEGUI.Key.Scan.D, 'd', 'D'),
        'e': (PyCEGUI.Key.Scan.E, 'e', 'E'),
        'f': (PyCEGUI.Key.Scan.F, 'f', 'F'),
        'g': (PyCEGUI.Key.Scan.G, 'g', 'G'),
        'h': (PyCEGUI.Key.Scan.H, 'h', 'H'),
        'i': (PyCEGUI.Key.Scan.I, 'i', 'I'),
        'j': (PyCEGUI.Key.Scan.J, 'j', 'J'),
        'k': (PyCEGUI.Key.Scan.K, 'k', 'K'),
        'l': (PyCEGUI.Key.Scan.L, 'l', 'L'),
        'm': (PyCEGUI.Key.Scan.M, 'm', 'M'),
        'n': (PyCEGUI.Key.Scan.N, 'n', 'N'),
        'o': (PyCEGUI.Key.Scan.O, 'o', 'O'),
        'p': (PyCEGUI.Key.Scan.P, 'p', 'P'),
        'q': (PyCEGUI.Key.Scan.Q, 'q', 'Q'),
        'r': (PyCEGUI.Key.Scan.R, 'r', 'R'),
        's': (PyCEGUI.Key.Scan.S, 's', 'S'),
        't': (PyCEGUI.Key.Scan.T, 't', 'T'),
        'u': (PyCEGUI.Key.Scan.U, 'u', 'U'),
        'v': (PyCEGUI.Key.Scan.V, 'v', 'V'),
        'w': (PyCEGUI.Key.Scan.W, 'w', 'W'),
        'x': (PyCEGUI.Key.Scan.X, 'x', 'X'),
        'y': (PyCEGUI.Key.Scan.Y, 'y', 'Y'),
        'z': (PyCEGUI.Key.Scan.Z, 'z', 'Z'),

        '`': (PyCEGUI.Key.Scan.Grave, '`', '~'),
        '0': (PyCEGUI.Key.Scan.Zero, '0', ')'),
        '1': (PyCEGUI.Key.Scan.One, '1', '!'),
        '2': (PyCEGUI.Key.Scan.Two, '2', '@'),
        '3': (PyCEGUI.Key.Scan.Three, '3', '#'),
        '4': (PyCEGUI.Key.Scan.Four, '4', '$'),
        '5': (PyCEGUI.Key.Scan.Five, '5', '%'),
        '6': (PyCEGUI.Key.Scan.Six, '6', '^'),
        '7': (PyCEGUI.Key.Scan.Seven, '7', '&'),
        '8': (PyCEGUI.Key.Scan.Eight, '8', '*'),
        '9': (PyCEGUI.Key.Scan.Nine, '9', '('),
        '-': (PyCEGUI.Key.Scan.Minus, '-', '_'),
        '=': (PyCEGUI.Key.Scan.Equals, '=', '+'),


        '[': (PyCEGUI.Key.Scan.LeftBracket, '[', '{'),
        ']': (PyCEGUI.Key.Scan.RightBracket, ']', '}'),
        '\\': (PyCEGUI.Key.Scan.Backslash, '\\', '|'),
        ';': (PyCEGUI.Key.Scan.Semicolon, ';', ':'),

        "'": (PyCEGUI.Key.Scan.Apostrophe, "'", '"'),
        ',': (PyCEGUI.Key.Scan.Comma, ',', '<'),
        '.': (PyCEGUI.Key.Scan.Period, '.', '>'),
        '/': (PyCEGUI.Key.Scan.Slash, '/', '?'),

        'f1': (PyCEGUI.Key.Scan.F1, '', ''),
        'f2': (PyCEGUI.Key.Scan.F3, '', ''),
        'f3': (PyCEGUI.Key.Scan.F3, '', ''),
        'f4': (PyCEGUI.Key.Scan.F4, '', ''),
        'f5': (PyCEGUI.Key.Scan.F5, '', ''),
        'f6': (PyCEGUI.Key.Scan.F6, '', ''),
        'f7': (PyCEGUI.Key.Scan.F7, '', ''),
        'f8': (PyCEGUI.Key.Scan.F8, '', ''),
        'f9': (PyCEGUI.Key.Scan.F9, '', ''),
        'f10': (PyCEGUI.Key.Scan.F10, '', ''),
        'f11': (PyCEGUI.Key.Scan.F11, '', ''),
        'f12': (PyCEGUI.Key.Scan.F12, '', ''),

        'enter': (PyCEGUI.Key.Scan.Return, '\r', '\r'),
        'tab': (PyCEGUI.Key.Scan.Tab, '\t', '\t'),
        'space': (PyCEGUI.Key.Scan.Space, ' ', ' '),

        'escape': (PyCEGUI.Key.Scan.Escape, '', ''),
        'backspace': (PyCEGUI.Key.Scan.Backspace, '', ''),

        'insert': (PyCEGUI.Key.Scan.Insert, '', ''),
        'delete': (PyCEGUI.Key.Scan.Delete, '', ''),

        'home': (PyCEGUI.Key.Scan.Home, '', ''),
        'end': (PyCEGUI.Key.Scan.End, '', ''),
        'page_up': (PyCEGUI.Key.Scan.PageUp, '', ''),
        'page_down': (PyCEGUI.Key.Scan.PageDown, '', ''),

        'arrow_left': (PyCEGUI.Key.Scan.ArrowLeft, '', ''),
        'arrow_up': (PyCEGUI.Key.Scan.ArrowUp, '', ''),
        'arrow_down': (PyCEGUI.Key.Scan.ArrowDown, '', ''),
        'arrow_right': (PyCEGUI.Key.Scan.ArrowRight, '', ''),

        'num_lock': (PyCEGUI.Key.Scan.NumLock, '', ''),
        'caps_lock': (PyCEGUI.Key.Scan.Capital, '', ''),
        'scroll_lock': (PyCEGUI.Key.Scan.ScrollLock, '', ''),

        'lshift': (PyCEGUI.Key.Scan.LeftShift, '', ''),
        'rshift': (PyCEGUI.Key.Scan.RightShift, '', ''),
        'lcontrol': (PyCEGUI.Key.Scan.LeftControl, '', ''),
        'rcontrol': (PyCEGUI.Key.Scan.RightControl, '', ''),
        'lalt': (PyCEGUI.Key.Scan.LeftAlt, '', ''),
        'ralt': (PyCEGUI.Key.Scan.RightAlt, '', ''),
        }
    hideSystemCursor = True
    _renderingEnabled = True
    _capsLock = False
    _shiftCount = 0
    
    def __init__(self):
        ceguiCB = PythonCallbackObject(self.renderCallback)
        self.cbNode = CallbackNode("CEGUI")
        self.cbNode.setDrawCallback(ceguiCB)
        render2d.attachNewNode(self.cbNode)
        base.accept('window-event', self.windowEvent)
        PyCEGUIOpenGLRenderer.OpenGLRenderer.bootstrapSystem()
        self.props = WindowProperties()
        self.System = PyCEGUI.System.getSingleton()
        self.WindowManager = PyCEGUI.WindowManager.getSingleton()
        self.SchemeManager = PyCEGUI.SchemeManager.getSingleton()
        self.FontManager = PyCEGUI.FontManager.getSingleton()

    def __del__(self):
        PyCEGUIOpenGLRenderer.OpenGLRenderer.destroySystem()

    def initializeResources(self, resourcePath):
        rp = self.System.getResourceProvider()
        rp.setResourceGroupDirectory("schemes", resourcePath)
        rp.setResourceGroupDirectory("imagesets", resourcePath)
        rp.setResourceGroupDirectory("fonts", resourcePath)
        rp.setResourceGroupDirectory("layouts", resourcePath)
        rp.setResourceGroupDirectory("looknfeels", resourcePath)
        rp.setResourceGroupDirectory("schemas", resourcePath)
        PyCEGUI.Imageset.setDefaultResourceGroup("imagesets")
        PyCEGUI.Font.setDefaultResourceGroup("fonts")
        PyCEGUI.Scheme.setDefaultResourceGroup("schemes")
        PyCEGUI.WidgetLookManager.setDefaultResourceGroup("looknfeels")
        PyCEGUI.WindowManager.setDefaultResourceGroup("layouts")
        parser = self.System.getXMLParser()
        if parser.isPropertyPresent("SchemaDefaultResourceGroup"):
            parser.setProperty("SchemaDefaultResourceGroup", "schemas")

    def enableInputHandling(self):
        for button, cegui_name in self.buttons.iteritems():
            base.accept(button, self.captureButton, [button, cegui_name])
        base.mouseWatcherNode.setModifierButtons(ModifierButtons())
        base.buttonThrowers[0].node().setModifierButtons(ModifierButtons())
        for key, keyTuple in self.keys.iteritems():
            base.accept(key, self.captureKeys, [key, keyTuple])
            base.accept(key + '-up', self.captureKeys, [key + '-up', keyTuple])
            base.accept(key + '-repeat', self.captureKeys, [key, keyTuple])
        if (self.hideSystemCursor):
            self.props.setCursorHidden(True)
            base.win.requestProperties(self.props)

    def disableInputHandling(self):
        for button, name in self.buttons.iteritems():
            base.ignore(button)
        for key, keyTuple in self.keys.iteritems():
            base.ignore(key)
            base.ignore(key + '-up')
            base.ignore(key + '-repeat')
        if (self.hideSystemCursor):
            self.props.setCursorHidden(False)
            base.win.requestProperties(self.props)

    def enable(self):
        self.enableInputHandling()
        _renderingEnabled = True

    def disable(self):
        self.disableInputHandling()
        _renderingEnabled = False
   
    def captureKeys(self, key, keyTuple):
        cegui_key = keyTuple[0]
        key_ascii = keyTuple[1]
        key_shift = keyTuple[2]
        if key.find('shift') > 0:
            if key.endswith('-up'):
                if self._shiftCount > 0:
                    self._shiftCount -= 1
            else:
                self._shiftCount += 1
        elif key == 'caps_lock':
            self._capsLock = not self._capsLock

        elif key.endswith('-up'):
            self.System.injectKeyUp(cegui_key)
        else:
            self.System.injectKeyDown(cegui_key)
            if key_ascii != '':
                if self._shiftCount > 0:
                    if self._capsLock and key_ascii in string.lowercase:
                        self.System.injectChar(ord(key_ascii))
                    else:
                        self.System.injectChar(ord(key_shift))
                elif self._capsLock and key_ascii in string.lowercase:
                    self.System.injectChar(ord(key_shift))
                else:
                    self.System.injectChar(ord(key_ascii))

    def captureButton(self, button, name):
        if button == 'wheel_up':
            self.System.injectMouseWheelChange(1)
        elif button == 'wheel_down':
            self.System.injectMouseWheelChange(-1)
        elif button.endswith('-up'):
            self.System.injectMouseButtonUp(self.buttons[button])
        else:
            self.System.injectMouseButtonDown(self.buttons[button])

    def windowEvent(self, window):
        self.System.notifyDisplaySizeChanged(PyCEGUI.Size(window.getXSize(), window.getYSize()))

    def renderCallback(self, data):
        self.queue()
        if self._renderingEnabled:
            dt = globalClock.getDt()
            self.System.injectTimePulse(dt)
            if base.mouseWatcherNode.hasMouse():
                x = base.win.getXSize() * (1 + base.mouseWatcherNode.getMouseX()) / 2
                y = base.win.getYSize() * (1 - base.mouseWatcherNode.getMouseY()) / 2
                self.System.injectMousePosition(x, y)
            self.System.renderGUI()
        
        


    

    
    def queue(self):
        global x
        global username
        global password
        if x==0:
            #must be called twice for some reason(bug?)
            reactor.callFromThread(loginClicked, username, password)
            reactor.callFromThread(loginClicked, username, password)
            x=1
        global queue
        while not queue.empty():
            callable=queue.get()
            callable()
            queue.task_done
            global logged
            
            
            if logged==True:
                layout=PyCEGUI.WindowManager.getSingleton().loadWindowLayout("characters.layout")
                PyCEGUI.System.getSingleton().setGUISheet(layout)
                
                self.create=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Create")
                self.start=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Start")
                self.create.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'createCharacter')
                self.start.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'play')
                
                self.keymap = {"a":0, "d":0, "w":0, "s":0}
                
                self.human=loader.loadModel('./models/Human.x')
                self.human.reparentTo(render)
                self.human.setScale(9, 9, 9)
                
                global enemyLoc1
                global enemyLoc2
                global enemyLoc3
                global enemyNum
                numloaded = 0
                while enemyNum > numloaded:
                
                    self.enemy=loader.loadModel('./models/Human.x')
                    self.enemy.reparentTo(render)
                    self.enemy.setScale(9,9,9)
                    self.enemy.setPos(enemyLoc1[0], enemyLoc2[0], enemyLoc3[0])
                    numloaded += 1
                    
                if enemyNum == 0:
                    print "No enemies"
                
                self.environment=loader.loadModel('./models/Environment.x')
                self.environment.reparentTo(render)
                self.environment.setScale(20,20,20)
                self.environment.setPos(0,0,0)
                
                plight=PointLight('plight')
                plight.setColor(VBase4(.9,.9,.9,1))
                plnp=render.attachNewNode(plight)
                plnp.setPos(2, -5, 1000)
                render.setLight(plnp)
                
                ambientLight = AmbientLight('ambientLight')
                ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
                ambientLightNP = render.attachNewNode(ambientLight)
                render.setLight(ambientLightNP)
                
                self.floater = NodePath(PandaNode("floater"))
                self.floater.reparentTo(render)
                
                self.cTrav = CollisionTraverser()
                
                self.humanGroundRay = CollisionRay()
                self.humanGroundRay.setOrigin(0,0,1000)
                self.humanGroundRay.setDirection(0,0,-1)
                
                self.humanGroundCol=CollisionNode('humanRay')
                self.humanGroundCol.addSolid(self.humanGroundRay)
                self.humanGroundCol.setFromCollideMask(BitMask32.bit(0))
                self.humanGroundCol.setIntoCollideMask(BitMask32.allOff())
                self.humanGroundColNp=self.human.attachNewNode(self.humanGroundCol)
                
                self.humanGroundHandler=CollisionHandlerQueue()
                
                self.cTrav.addCollider(self.humanGroundColNp, self.humanGroundHandler)
                self.cTrav.traverse(render)
                
                entries=[]
                for i in range(self.humanGroundHandler.getNumEntries()):
                    entry = self.humanGroundHandler.getEntry(i)
                    entries.append(entry)
                entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                             x.getSurfacePoint(render).getZ()))
                if (len(entries)>0) and (entries[0].getIntoNode().getName()== "terrain"):
                    self.human.setZ(entries[0].getSurfacePoint(render).getZ()+1.8)
                logged=False
                
                self.accept("w", self.forwardMovement, [1])
                self.accept("w-up", self.forwardMovement, [0])
                self.accept("s", self.backwardMovement, [1])
                self.accept("s-up", self.backwardMovement, [0])
                self.accept("a", self.leftMovement, [1])
                self.accept("a-up", self.leftMovement, [0])
                self.accept("d", self.rightMovement, [1])
                self.accept("d-up", self.rightMovement, [0])
                self.accept("r", self.forwardMovement, [1])
                
                global newloc
                print "starting"
                self.human.setPos(newloc[0], newloc[1], newloc[2])
                newloc=[]
            return
            
        
    def play(self, args):
           
        
        base.disableMouse()
        camera.setPos(0, 100, 20)
        PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
        layout=PyCEGUI.WindowManager.getSingleton().loadWindowLayout("interface.layout")
        PyCEGUI.System.getSingleton().setGUISheet(layout)
        global started
        started=True
        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0,0,1000)
        self.camGroundRay.setDirection(0,0,-1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.camGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        taskMgr.add(self.move,"moveTask")
        
    def move(self, task):
    
        global movecount
        move = False
        
        if self.keymap['d']==1:
            self.human.setH(self.human.getH() - 3)
            
        if self.keymap['a']==1:
            self.human.setH(self.human.getH() + 3)
            
        if self.keymap['w']==1:
            self.human.setY(self.human, -3 * globalClock.getDt())
            
        if self.keymap['s']==1:
            self.human.setY(self.human, 3 * globalClock.getDt())
            
        if movecount > 10:
            global loc
            loc.append(self.human.getX())
            loc.append(self.human.getY())
            loc.append(self.human.getZ())
            reactor.callFromThread(movement)
            movecount = 0
        if self.keymap['d']==1 | self.keymap['a']==1 | self.keymap['w']==1 | self.keymap['s']==1:  
            movecount += 1
            
        camvec = self.human.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        
        if (camdist > 35.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-35))
            camdist = 35.0
        if (camdist < 30.0):
            base.camera.setPos(base.camera.getPos() - camvec*(30-camdist))
            camdist = 30.0
        self.floater.setPos(self.human.getPos())
        self.floater.setZ(self.human.getZ() + 10.0)
        base.camera.lookAt(self.floater)
        
        return task.cont
        
    def forwardMovement(self, value):
        self.keymap['w']=value
        
    def backwardMovement(self,value):
        self.keymap['s']=value
        self.keymap['w']=0
        
    def leftMovement(self,value):
        self.keymap['a']=value
        
    def rightMovement(self,value):
        self.keymap['d']=value

class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
        self.CEGUI = PandaCEGUI()
        self.CEGUI.initializeResources('./datafiles')
        self.setupUI()
        self.CEGUI.enable()


    def setupUI(self):
        PyCEGUI.SchemeManager.getSingleton().create("VanillaSkin.scheme")
        PyCEGUI.System.getSingleton().setDefaultFont("AnkeCalligraph")
        PyCEGUI.System.getSingleton().setDefaultMouseCursor("Vanilla-Images", "MouseArrow")
        layout=PyCEGUI.WindowManager.getSingleton().loadWindowLayout("login.layout")
        PyCEGUI.System.getSingleton().setGUISheet(layout)
        self.loginWindow=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login")
        self.submit=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Submit")
        self.usernameBox=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Username")
        self.passwordBox=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Password")
        self.submit.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'login')
        self.noUsername=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoUsername")
        self.noUsernameOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoUsername/Ok")
        self.noUsernameOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'noUsernameOkClicked')
        self.noPassword=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoPassword")
        self.noPasswordOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoPassword/Ok")
        self.noPasswordOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'noPasswordOkClicked')
        self.Incorrect=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Incorrect")
        self.IncorrectOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Incorrect/Ok")
        self.IncorrectOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'incorrectOkClicked')

    def login(self, args):
        self.username=self.usernameBox.getText()
        if self.username=="":
            self.noUsername.setProperty("Visible", "True")
        else:
            self.password=self.passwordBox.getText()
            if password=="":
                self.noPassword.setProperty("Visible", "True")
            else:
                global username
                username=self.username
                global x
                x=0
                global password
                password=self.password
                
    def noUsernameOkClicked(self,args):
        self.noUsername.setProperty("Visible", "False")
        
    def noPasswordOkClicked(self,args):
        self.noPassword.setProperty("Visible", "False")
        
    def incorrectOkClicked(self,args):
        self.Incorrect.setProperty("Visible", "False")
        
    def createCharacter(self, args):
        PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
        
    def play(self, args):
        PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
        layout=PyCEGUI.WindowManager.getSingleton().loadWindowLayout("interface.layout")
        PyCEGUI.System.getSingleton().setGUISheet(layout)
        reactor.callFromThread(start)
        global started
        started=True
                
class EchoClient(StatefulStringProtocol,Int32StringReceiver):
    def connectionMade(self):
        print "connected"

    def proto_init(self, data):
        if data=="inv":
            reactor.callInThread(inv)
            
        elif data=="logged in":
            reactor.callInThread(loggedin)
            
        elif data=="Enemy":
            return 'enemy'
            
        elif data=="Position":
            return 'position'
            
        else:
            print data
            
        return 'init'
        
    def proto_enemy(self, data):
        global enemyNum
        global enemyLoc1
        enemyNum += 1
        enemyLoc1.append(float(data));
        return 'enemy1'
        
    def proto_enemy1(self, data):
        global enemyLoc2
        enemyLoc2.append(float(data));
        return 'enemy2'
        
    def proto_enemy2(self, data):
        global enemyLoc3
        enemyLoc3.append(float(data))
        return 'init'
        
    def proto_position(self, data):
        global newloc
        newloc.append(float(data))
        return 'positiony'
        
    def proto_positiony(self, data):
        global newloc
        newloc.append(float(data))
        return 'positionz'
        
    def proto_positionz(self, data):
        global newloc
        newloc.append(float(data))
        return 'init'

    def connectionLost(self, reason):
        print "connection lost"
        
class twistedThread(threading.Thread):
    def run(self):
        creator = protocol.ClientCreator(reactor, EchoClient)
        d = creator.connectTCP("localhost", 5000)
        d.addCallback(gotProtocol)
        reactor.run(False)
        
twistedThread().start()

app = MyApp()
app.run()