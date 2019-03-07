import win32api, win32con, win32gui, win32ui, os, dontExecute, time, threading,ctypes, uuid
from multiprocessing.connection import Listener
from time import sleep

version = "2.4"
activeSlot, hWindow, slot1, slot2, recoil11 = (0,)*5
recoil12,recoil21,recoil22 = (0,)*3
gameselected, processfound, rcsactive = (False,)*3
overlayActive = "True"
overlaykey = "Numpad 0"
slot1 = "none"
slot2 = "none"

def child(conn):
	global slot1, slot2, activeSlot,recoil11,recoil12,recoil21,recoil22, gameselected, processfound, rcsactive, overlaykey, overlayActive
	while True:
		try:
			msg = conn.recv()
			setting, weaponcfg = msg.split("|")
			processfound, gameselected, rcsactive, overlaykey, overlayActive = setting.split(";")
			_slot1, _slot2, activeSlot = weaponcfg.split(";")
			slot1,recoil11,recoil12 = _slot1.split(",")
			slot2,recoil21,recoil22 = _slot2.split(",")
			if overlayActive.lower() == "True".lower() or overlayActive == True:
				win32gui.ShowWindow(hWindow, True)
			win32gui.RedrawWindow(hWindow, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
			
		except EOFError:
			pass
			break
		except ConnectionResetError:
			print("Client closed connection")
			slot1, slot2 = ("none",)*2
			recoil11,recoil12,recoil21,recoil22, activeSlot = (0,)*5
			gameselected, processfound, rcsactive = (False,)*3
			if overlayActive.lower() == "True".lower() or overlayActive == True:
				win32gui.ShowWindow(hWindow, True)
			win32gui.RedrawWindow(hWindow, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
			exit()
			break
		
def mother(address):
	serv = Listener(address)
	while True:
		client = serv.accept()
		child(client)
	
def updateGui(hWnd):
	if overlayActive.lower() == "True".lower() or overlayActive == True:
		win32gui.ShowWindow(hWnd, True)
		hdc, paintStruct = win32gui.BeginPaint(hWnd)
		win32gui.SetBkMode(hdc,win32con.TRANSPARENT)
		rect = win32gui.GetClientRect(hWnd)
		hbrush = win32gui.CreateSolidBrush(win32api.RGB(137, 137, 137))
		RectCoords = (int(rect[2]*0.90),int(rect[3]*0.5),int(rect[2]*0.99),int(rect[3]*0.7))
		win32gui.FillRect(hdc, RectCoords,hbrush)
		if int(activeSlot) == 1:
			win32gui.SetTextColor(hdc,win32api.RGB(0,255,0))
		win32gui.DrawText(hdc,'Weaponslot 1: ' + "{:<8}".format(slot1),-1,(0,0,int(rect[2]*0.98),int(rect[3]*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.DrawText(hdc,'RecoilValue 1: ' + "{:<3}".format(str(recoil11)),-1,(0,0,int(rect[2]*0.97),int((rect[3]+25)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.DrawText(hdc,'RecoilValue 2: ' + "{:<3}".format(str(recoil12)),-1,(0,0,int(rect[2]*0.97),int((rect[3]+50)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.SetTextColor(hdc,win32api.RGB(0,0,0))
		if int(activeSlot) == 2:
			win32gui.SetTextColor(hdc,win32api.RGB(0,255,0))
		win32gui.DrawText(hdc,'Weaponslot 2: ' + "{:<8}".format(slot2),-1,(0,0,int(rect[2]*0.98),int((rect[3]+100)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.DrawText(hdc,'RecoilValue 1: ' + "{:<3}".format(str(recoil21)),-1,(0,0,int(rect[2]*0.97),int((rect[3]+125)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.DrawText(hdc,'RecoilValue 2: ' + "{:<3}".format(str(recoil22)),-1,(0,0,int(rect[2]*0.97),int((rect[3]+150)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.SetTextColor(hdc,win32api.RGB(0,0,0))
		win32gui.DrawText(hdc,'Process found: ' + "{:<5}".format(str(processfound)),-1,(0,0,int(rect[2]*0.98),int((rect[3]+225)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.DrawText(hdc,'Game selected: ' + "{:<5}".format(str(gameselected)),-1,(0,0,int(rect[2]*0.98),int((rect[3]+250)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.DrawText(hdc,'RCS Activated: ' + "{:<5}".format(str(rcsactive)),-1,(0,0,int(rect[2]*0.98),int((rect[3]+275)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.DrawText(hdc,'Overlay: ' + "{:<5}".format(str(overlaykey)),-1,(0,0,int(rect[2]*0.98),int((rect[3]+325)*0.519)),win32con.DT_RIGHT | win32con.DT_BOTTOM | win32con.DT_NOCLIP | win32con.DT_SINGLELINE)
		win32gui.EndPaint(hWnd, paintStruct)
	else:
		win32gui.ShowWindow(hWnd, False)
		hdc, paintStruct = win32gui.BeginPaint(hWnd)
		win32gui.SetBkMode(hdc,win32con.TRANSPARENT)
		win32gui.EndPaint(hWnd, paintStruct)
	

def Render(hWnd,message,wParam,lParam):
	updateGui(hWnd)
	
def Destroy(hwnd,message,wParam,lParam):
	PostQuitMessage(0)
		
def KeyPressed(hWnd,message,wParam,lParam):
	print(message,wParam,lParam)
		
def main():
	global hWindow
	message_map = {
			win32con.WM_PAINT: Render,
			win32con.WM_DESTROY: Destroy,
			win32con.WM_KEYDOWN: KeyPressed
		}
	hInstance = win32api.GetModuleHandle()
	className = uuid.uuid4().hex	
	wndClass                = win32gui.WNDCLASS()
	wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
	wndClass.lpfnWndProc    = message_map
	wndClass.hInstance      = hInstance
	wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
	wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
	wndClass.lpszClassName  = className
	wndClassAtom = win32gui.RegisterClass(wndClass)
	exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
	style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE
	hWindow = win32gui.CreateWindowEx(exStyle, wndClassAtom, None,style,0,0,win32api.GetSystemMetrics(win32con.SM_CXSCREEN), 
		win32api.GetSystemMetrics(win32con.SM_CYSCREEN),None, None, hInstance,None
	)
	win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
	win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

	win32gui.UpdateWindow(hWindow) 
	
	t1 = threading.Thread(target=mother,args=(('',1337),))
	t1.setDaemon(True)
	t1.start()
	print("YOU CAN MINIMIZE THIS WINDOW NOW!")
	print("IF YOU WANT TO CLOSE THE SERVER, CLOSE THIS WINDOW!")
	ctypes.windll.kernel32.SetConsoleTitleW("No Recoil Script V"+version+ " Overlay-Server     Made by SiedlerLP")
	while True:
		b,msg = win32gui.GetMessage(hWindow,0,0)
		if msg == 0:
			break
		win32gui.TranslateMessage(msg)
		win32gui.DispatchMessage(msg)
		

if __name__ == '__main__':
	main()