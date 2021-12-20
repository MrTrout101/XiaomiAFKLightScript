from yeelight import Bulb, discover_bulbs
from win10toast import ToastNotifier
from pynput.mouse import Controller
import time

#Gets current epoch time
def currentTime():
    return int(time.time())

toastNotification = ToastNotifier()
mouseController = Controller()
lastMoveTime = currentTime()
lastMousePos = mouseController.position
timeLimit = 10 #AFK threshold (in seconds)
AFK = False

#Discovers Yeelight bulb's on the network
def bulbIP():
    try:
        discoverBulbsList = discover_bulbs()
        discoverBulbsDict = discoverBulbsList[0]
        return discoverBulbsDict['ip']
    except:
        toastNotification.show_toast("AFK Light Script","No lights found on local network")

#Checks if afk
def afkCheck():
    global lastMousePos
    global lastMoveTime
    global AFK

    if mouseController.position != lastMousePos:
        #Is not AFK
        lastMoveTime = currentTime() 
        lastMousePos = mouseController.position
        AFK = False
    elif (lastMousePos == mouseController.position) and ((currentTime() - lastMoveTime) > (timeLimit - 2)):
        #Is AFK
        AFK = True
        try:
            light = Bulb(bulbIP())
            light.turn_off()
            toastNotification.show_toast("AFK Light Script","You are now AFK")
        except:
            toastNotification.show_toast("AFK Light Script","Unable to turn lights off")

#Checks if mouse has moved after being AFK
def afk():
    global lastMousePos
    global AFK
    
    if mouseController.position != lastMousePos:
        AFK = False
        try:
            light = Bulb(bulbIP())
            light.turn_on()
            toastNotification.show_toast("AFK Light Script","You are no longer AFK")
        except:
            toastNotification.show_toast("AFK Light Script","Unable to turn lights on")

while True:
    time.sleep(1)
    if not AFK:
        afkCheck()
    else:
        afk()
