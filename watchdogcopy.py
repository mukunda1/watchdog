import pythoncom, pyHook
import json
import codecs 
import sys
from tendo import singleton
from datetime import datetime
import ctypes, ctypes.wintypes
import PyQt4
from PyQt4 import QtCore, QtGui, QtSvg
import os
import os.path

global get_keywin_names
global get_mousewin_names
global window_name
	 
#global OnKeyboardEvent
k_window_name = {"z":0}
m_window_name = {"z":0}

if not os.path.isfile("keywin.txt"):
	f = open("keywin.txt","wb+")

if os.stat("keywin.txt").st_size != 0: 
	f = open("keywin.txt","r")
	for ol in f:
		k_window_name = json.loads(ol)

if not os.path.isfile("clickwin.txt"):
	g = open("clickwin.txt","wb+")

if os.stat("clickwin.txt").st_size != 0:
	g = open("clickwin.txt","r")
	for kl in g:
		m_window_name = json.loads(kl)
 
def hooker(action):
	
	def get_keywin_names(o): 

	    x = str(o) 

	    if x.decode('utf-8','replace') in  k_window_name.keys(): 
	        return k_window_name[x.decode('utf-8','replace')]  
	    else:
	        k_window_name[x.decode('utf-8','replace')]=max(k_window_name.values())+1
	    return k_window_name[x.decode('utf-8','replace')]
	     
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
	    json.dump(k_window_name, h) 
	    f.close() 
	# return True to pass the event to other handlers
	    return True

	def get_mousewin_names(o):

	    x = str(o)

	    if x.decode('utf-8','replace') in  m_window_name.keys():
	        return m_window_name[x.decode('utf-8','replace')]  
	    else:
	        m_window_name[x.decode('utf-8','replace')]=max(m_window_name.values())+1
	    return m_window_name[x.decode('utf-8','replace')]


	def OnMouseEvent(event):
	    s = ""
	    # called when mouse events are received
	    s += str(event.MessageName)+","
	    s += str(event.Message)+","
	    s += str(event.Time)+","
	    s += str(event.Window)+","
	    s += str(get_mousewin_names(event.WindowName))+"," 
	    s += str(event.Position)+","
	    s += str(event.Wheel)+","
	    s += str(event.Injected)+","
	    s += "\n"
	    f = open("clicklog","a") 
	    f.write(s)
	    h = open("clickwin.txt",'w')
	    json.dump(m_window_name, h)
	    f.close()

	# return True to pass the event to other handlers
	    return True
	     
	 
	# create a hook manager
	hm = pyHook.HookManager()
	# watch for all mouse events 
	hm.KeyDown = OnKeyboardEvent
	# watch for all mouse events
	hm.MouseAll = OnMouseEvent
	# set the hook
	hm.HookKeyboard()
	# set the hook
	hm.HookMouse()

	if action=="stop":
		
		
		
		sys.exit()
	# wait foreverhai srinath 
	pythoncom.PumpMessages()

#gui Start point

# for single instance 

def gui():

	me = singleton.SingleInstance()

	app = QtGui.QApplication([])

	i = QtGui.QSystemTrayIcon()

	m = QtGui.QMenu()



	def startCB():
	  	hooker("")

	def quitCB():
		QtGui.QApplication.quit()
		hooker("stop")
	


	m.addAction('Start', startCB)
	m.addAction('Private', quitCB)
	m.addAction('Stop', quitCB)
	i.setContextMenu(m)

	svg = QtSvg.QSvgRenderer('Feed-icon.svg')
	if not svg.isValid():
		raise RuntimeError('bad SVG')
	pm = QtGui.QPixmap(16, 16)
	painter = QtGui.QPainter(pm)
	svg.render(painter)
	icon = QtGui.QIcon(pm)
	i.setIcon(icon)
	i.show()

	app.exec_()

	del painter, pm, svg # avoid the paint device getting
	del i, icon          # deleted before the painter
	del app


def main():
    gui()

if __name__ == '__main__':
    main()





