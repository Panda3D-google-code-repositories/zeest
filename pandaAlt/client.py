from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.task import Task
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

import PyCEGUI
import PyCEGUIOpenGLRenderer

import sqlite3 as sqlite

loadPrcFileData('', 'show-frame-rate-meter #t')
loadPrcFileData('', 'sync-video #f')

movecount=0
loc=[]


class MyApp(ShowBase):

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
 
    def __init__(self):
        ShowBase.__init__(self)
        ceguiCB = PythonCallbackObject(self.renderCallback)
        self.cbNode = CallbackNode("CEGUI")
        self.cbNode.setDrawCallback(ceguiCB)
        render2d.attachNewNode(self.cbNode)
        base.accept('window-event', self.windowEvent)
        PyCEGUIOpenGLRenderer.OpenGLRenderer.bootstrapSystem()
        self.System = PyCEGUI.System.getSingleton()
        self.initializeResources('./datafiles')
        self.props = WindowProperties()
        self.WindowManager = PyCEGUI.WindowManager.getSingleton()
        self.SchemeManager = PyCEGUI.SchemeManager.getSingleton()
        self.FontManager = PyCEGUI.FontManager.getSingleton()
        self.setupUI()
        self.enable()
        self.networkSetup()
        
    def backwardMovement(self,value):
        self.keymap['s']=value
        self.keymap['w']=0
        
    def captureButton(self, button, name):
        if button == 'wheel_up':
            self.System.injectMouseWheelChange(1)
        elif button == 'wheel_down':
            self.System.injectMouseWheelChange(-1)
        elif button.endswith('-up'):
            self.System.injectMouseButtonUp(self.buttons[button])
        else:
            self.System.injectMouseButtonDown(self.buttons[button])
        
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
        
    def completeRegister(self, args):
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
                x=2
                global password
                password=self.password
                PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
                self.setupUI()
        
    def createCharacter(self, args):
        PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
        
    def __del__(self):
        PyCEGUIOpenGLRenderer.OpenGLRenderer.destroySystem()
        
    def disable(self):
        self.disableInputHandling()
        _renderingEnabled = False
        
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
            
    def forwardMovement(self, value):
        self.keymap['w']=value
        
    def handleDatagram(self, data, msgID):
        if msgID in Handlers.keys():
            Handlers[msgID](msgID,data)
        else:
            print "Unknown msgID: %d" % msgID
            print data
        return 
        
    def incorrectOkClicked(self,args):
        self.Incorrect.setProperty("Visible", "False")
        
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
            
    def leftMovement(self,value):
        self.keymap['a']=value
        
    def loggedIn(self):
        PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
        
        layout=PyCEGUI.WindowManager.getSingleton().loadWindowLayout("characters.layout")
        PyCEGUI.System.getSingleton().setGUISheet(layout)
        
        self.create=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Create")
        self.start=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Start")
        self.create.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'createCharacter')
        self.start.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'play')
        
        self.keymap = {"a":0, "d":0, "w":0, "s":0}
        
        self.human=loader.loadModel('./models/Human.x')
        self.human.reparentTo(render)
        self.human.setScale(7, 7, 7)
        
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

    def login(self, args):
        self.username=self.usernameBox.getText()
        if self.username=="":
            self.noUsername.setProperty("Visible", "True")
        else:
            self.password=self.passwordBox.getText()
            if self.password=="":
                self.noPassword.setProperty("Visible", "True")
            else:
                global username
                username=self.username
                password=self.password
                
                pkg = PyDatagram()
                pkg.addUint16(CMSG_AUTH)
                pkg.addString(username)
                pkg.addString(password)
                self.send(pkg)
                
    def move(self, task):
    
        time=globalClock.getDt()
        
        if self.keymap['d']==1:
            self.human.setH(self.human.getH() - 3)
            self.sendMove('d', time)
            
        if self.keymap['a']==1:
            self.human.setH(self.human.getH() + 3)
            self.sendMove('a', time)
            
        if self.keymap['w']==1:
            self.human.setY(self.human, -3 * time)
            self.sendMove('w', time)
            
        if self.keymap['s']==1:
            self.human.setY(self.human, 3 * time)
            self.sendMove('s', time)
            
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
        
    def msgAuthResponse(self, msgID, data):
        flag = data.getUint32()
        if flag == 0:
            print "Unknown user"
       
        if flag == 2:
            print "Wrong pass, please try again..."

        if flag == 1:
            self.loggedIn()
            
    def msgChat(self, msgID, data):
        print data.getString()
        
    def msgDisconnectAck(self, msgID, data): 
        self.cManager.closeConnection(self.Connection)
        sys.exit()
        
    def networkSetup(self):
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        
        self.Connection = self.cManager.openTCPClientConnection("127.0.0.1", 9099,1000)
        self.cReader.addConnection(self.Connection)

        taskMgr.add(self.readTask, "serverReaderPollTask", -39)
        
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
                
    def noUsernameOkClicked(self,args):
        self.noUsername.setProperty("Visible", "False")
        
    def noPasswordOkClicked(self,args):
        self.noPassword.setProperty("Visible", "False")
        
    def play(self, args):
        base.disableMouse()
        camera.setPos(0, 100, 20)
        PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
        layout=PyCEGUI.WindowManager.getSingleton().loadWindowLayout("interface.layout")
        PyCEGUI.System.getSingleton().setGUISheet(layout)
        self.sendChat=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Send")
        self.sendChat.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'sendMessage')
        self.message=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Message")
        self.chatbox=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Chatbox")
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
        
    def position(self, msgID, data):
        self.human.setPos(data.getFloat64(), data.getFloat64(), data.getFloat64())
            
    def readTask(self, task):
        while 1:
            (datagram, data, msgID) = self.nonBlockingRead(self.cReader)
            if msgID is MSG_NONE:
                break
            else:
                self.handleDatagram(data, msgID)
               
        return Task.cont
        
    def registerClicked(self, args):
        PyCEGUI.WindowManager.getSingleton().destroyWindow("Root")
        layout=PyCEGUI.WindowManager.getSingleton().loadWindowLayout("register.layout")
        PyCEGUI.System.getSingleton().setGUISheet(layout)
        self.registerWindow=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register")
        self.submit=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/Submit")
        self.usernameBox=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/Username")
        self.passwordBox=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/Password")
        self.registerClose=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/Close")
        self.noUsername=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/NoUsername")
        self.noUsernameOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/NoUsername/Ok")
        self.noPassword=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/NoPassword")
        self.noPasswordOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/NoPassword/Ok")
        self.Incorrect=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/Incorrect")
        self.IncorrectOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Register/Incorrect/Ok")
        self.registerClose.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'cancelRegister')
        self.submit.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'completeRegister')
        self.noUsernameOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'noUsernameOkClicked')
        self.noPasswordOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'noPasswordOkClicked')
        
    def renderCallback(self, data):
        if self._renderingEnabled:
            dt = globalClock.getDt()
            self.System.injectTimePulse(dt)
            if base.mouseWatcherNode.hasMouse():
                x = base.win.getXSize() * (1 + base.mouseWatcherNode.getMouseX()) / 2
                y = base.win.getYSize() * (1 - base.mouseWatcherNode.getMouseY()) / 2
                self.System.injectMousePosition(x, y)
            self.System.renderGUI()
            
    def rightMovement(self,value):
        self.keymap['d']=value
        
    def send(self, pkg):
        self.cWriter.send(pkg, self.Connection)
        
    def sendMove(self, key, time):
        pkg = PyDatagram()
        pkg.addUint16(MOVEMENT)
        pkg.addString(key)
        pkg.addFloat64(time)
        self.send(pkg)
        
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
        self.register=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Register")
        self.register.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'registerClicked')
        self.noUsername=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoUsername")
        self.noUsernameOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoUsername/Ok")
        self.noUsernameOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'noUsernameOkClicked')
        self.noPassword=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoPassword")
        self.noPasswordOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/NoPassword/Ok")
        self.noPasswordOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'noPasswordOkClicked')
        self.Incorrect=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Incorrect")
        self.IncorrectOk=PyCEGUI.WindowManager.getSingleton().getWindow("Root/Login/Incorrect/Ok")
        self.IncorrectOk.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'incorrectOkClicked')

    def windowEvent(self, window):
        self.System.notifyDisplaySizeChanged(PyCEGUI.Size(window.getXSize(), window.getYSize()))

MSG_NONE            = 0
CMSG_AUTH           = 1
SMSG_AUTH_RESPONSE  = 2
CMSG_CHAT           = 3
SMSG_CHAT           = 4
CMSG_DISCONNECT_REQ = 5
SMSG_DISCONNECT_ACK = 6
MOVEMENT = 7
POSITION = 8

Client=MyApp()

Handlers = {
    SMSG_AUTH_RESPONSE  : Client.msgAuthResponse,
    SMSG_CHAT           : Client.msgChat,
    SMSG_DISCONNECT_ACK : Client.msgDisconnectAck,
    POSITION            : Client.position,
    }

Client.run()