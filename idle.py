import sys
import json
import time
import codecs
import pythoncom, pyHook
from PyQt4.QtGui import *
from datetime import datetime
from pytz import timezone
from tendo import singleton
import ctypes, ctypes.wintypes

global get_keywin_names


def keyboard_hook():
	idle()


	k_window_name = {"z":0}
	m_win_name = {"z":0}

	def get_keywin_names(o):

	    x = str(o)

	    if x.decode('utf-8','replace') in  k_window_name.keys():
	        return k_window_name[x.decode('utf-8','replace')]  
	    else:
	        k_window_name[x.decode('utf-8','replace')]=max(k_window_name.values())+1
	    return k_window_name[x.decode('utf-8','replace')]
	     
	def get_mousewin_names(o):
		
		x = str(o)
		if x.decode('utf-8','replace') in  m_win_name.keys():
			return m_win_name[x.decode('utf-8','replace')]
		else:
			m_win_name[x.decode('utf-8','replace')]=max(m_win_name.values())+1
			return m_win_name[x.decode('utf-8','replace')]


	def OnKeyboardEvent(event): 
	    s = ""   
	    s += str(event.Time)+","
	    s += str(get_keywin_names(event.WindowName))+"," 
	    s += str(event.Ascii)
	    s += str(event.Key) 
	    s += "\n"
	    f = open("keylog","a") 
	    f.write(s)
	    h = open("text.txt",'w')
	    json.dump(k_window_name, h)
	                      
	    f.close()
	# return True to pass the event to other handlers
	    return True

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
	 
	    h = open("click_window.txt",'w')
	    json.dump(m_win_name, h)

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
	hm.MouseAll = OnMouseEvent
	# set the hook
	hm.HookKeyboard()
	# set the hook
	hm.HookMouse()
	# wait foreverhai srinath 
	pythoncom.PumpMessages()


def gui():

	india = timezone('Asia/Kolkata')

	# Create an PyQT4 application object.
	a = QApplication(sys.argv)       
	 
	# The QWidget widget is the base class of all user interface objects in PyQt4.
	w = QWidget()
	 
	# Set window size. 
	w.resize(320, 240)
	 
	# Set window title  
	w.setWindowTitle("Watch Dog") 

	def start():
		ind_time = datetime.now(india)
		print str(ind_time)[11:19]
		keyboard_hook()

	def stop(): 
		ind_time = datetime.now(india)
		print str(ind_time)[11:19]
		return sys.exit()
	 
	# Add a button
	btn = QPushButton('Play', w)
	btn.resize(btn.sizeHint())
	btn.clicked.connect(start)
	btn.move(40, 100)
	btn1 = QPushButton('Stop', w)
	btn1.resize(btn.sizeHint())
	btn1.clicked.connect(stop)
	btn1.move(200, 100)       
	 
	# Show window
	w.show() 
	 
	sys.exit(a.exec_())


def idle():

	india = timezone('Asia/Kolkata')


	class LASTINPUTINFO(ctypes.Structure):
		    _fields_ = [
		      ('cbSize', ctypes.wintypes.UINT),
		      ('dwTime', ctypes.wintypes.DWORD),
		      ]

	PLASTINPUTINFO = ctypes.POINTER(LASTINPUTINFO)

	user32 = ctypes.windll.user32
	GetLastInputInfo = user32.GetLastInputInfo
	GetLastInputInfo.restype = ctypes.wintypes.BOOL
	GetLastInputInfo.argtypes = [PLASTINPUTINFO]

	kernel32 = ctypes.windll.kernel32
	GetTickCount = kernel32.GetTickCount
	Sleep = kernel32.Sleep

	def wait_until_idle(idle_time=60):

		idle_time_ms = int(idle_time*1000)
		liinfo = LASTINPUTINFO()
		liinfo.cbSize = ctypes.sizeof(liinfo)
		while True:
		    GetLastInputInfo(ctypes.byref(liinfo))
		    elapsed = GetTickCount() - liinfo.dwTime
		    if elapsed>=idle_time_ms:

		        break
		    Sleep(idle_time_ms - elapsed or 1)


	def wait_until_active(tol=5):

		liinfo = LASTINPUTINFO()
		liinfo.cbSize = ctypes.sizeof(liinfo)
		lasttime = None
		delay = 1 # ms
		maxdelay = int(tol*1000)
		while True:
		    GetLastInputInfo(ctypes.byref(liinfo))
		    
		    if lasttime is None: lasttime = liinfo.dwTime
		    if lasttime != liinfo.dwTime:
		        break
		    delay = min(2*delay, maxdelay)

		    Sleep(delay)
	while True:

		wait_until_idle(10)
		user32.MessageBeep(0)

		wait_until_active(1)

		if user32.MessageBeep(0):
			print str(datetime.now(india))[11:19]
	

def test():
	gui()
	



if __name__=='__main__':
	test()