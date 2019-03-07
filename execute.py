import win32api, mouse, keyboard, random, dontExecute, os, time, sys, ctypes, threading
from time import sleep
from random import randint
from multiprocessing.connection import Client
from subprocess import call
import colorama

colorama.init()

#TO-DO:
#[X] Toggle Overlay 
#[ ] Add Tabfire
#[ ] (Add DBZ (move while looting)) not sure if
#[ ] Add Menu/Map/Inventory
#[X] Move Recoil/Weapon/Slot Switching out of "rcson = true" condition

version = "2.6"
rcson, procfound, gameSelected, rapidFire,holdBreath = (False,)*5
toggleOverlayBool = True
needSendData = True
rndopt = randint(0,1)
lastKey, toggleKey, exitKey, reloadKey, restartKey = (0,)*5 
upKey, downKey, leftKey, rightKey, page_up = (0,)*5
page_down, activeSlot, slot1, slot2 = (0,)*4
aPid, count, rcValue2, rcValue1, toggleOverlay = (0,)*5
nPid = 1
processname = "putty" #PUBG = TslGame
c = None
colorcounter = 0
colors = [colorama.Fore.RED,colorama.Fore.YELLOW,colorama.Fore.GREEN,colorama.Fore.CYAN,colorama.Fore.BLUE,colorama.Fore.MAGENTA]

def loadConfig():
	global toggleKey, exitKey, reloadKey,restartKey, upKey, downKey, leftKey, rightKey, page_up, page_down,processname, rapidFireKey, configLoaded, slot1, slot2,rcValue2,rcValue1,toggleOverlay
	toggleKey = int(dontExecute.getConfig("Settings","default_toggle_key"))
	exitKey = int(dontExecute.getConfig("Settings","default_exit_key"))
	reloadKey = int(dontExecute.getConfig("Settings","default_reload_key"))
	restartKey = int(dontExecute.getConfig("Settings","default_restart_key"))
	upKey = int(dontExecute.getConfig("Settings","default_select_key_up"))
	downKey = int(dontExecute.getConfig("Settings","default_select_key_down"))
	leftKey = int(dontExecute.getConfig("Settings","default_select_key_left"))
	rightKey = int(dontExecute.getConfig("Settings","default_select_key_right"))
	page_up = int(dontExecute.getConfig("Settings","default_select_key_second_up"))
	page_down = int(dontExecute.getConfig("Settings","default_select_key_second_down"))
	rapidFireKey = int(dontExecute.getConfig("Settings","default_rapidFireKey"))
	toggleOverlay = int(dontExecute.getConfig("Settings","default_toggle_overlay_key"))
	processname = str(dontExecute.getConfig("Settings","default_processname"))
	slot1 = str(dontExecute.getConfig("Settings","slot1"))
	slot2 = str(dontExecute.getConfig("Settings","slot2"))
	rcValue1 = dontExecute.getRecoilValues(slot1)
	rcValue2 = dontExecute.getRecoilValues(slot2)
	
def drawScreen():
	global colorcounter
	os.system('cls' if os.name=='nt' else 'clear')
	colorcounter = randint(0,len(colors)-1)
	outStr  = "========================= "+ colors[colorcounter] +" No-Recoil-Script V"+version+" "+ colorama.Style.RESET_ALL +" =========================\n"
	outStr += "\n"
	outStr += colorama.Fore.YELLOW + "Status:"+ colorama.Style.RESET_ALL+"\n"
	outStr += "Process found: " + "{:<15}".format(((colorama.Fore.BLUE + str(True)) if procfound else (colorama.Fore.RED + str(False)))) + colorama.Style.RESET_ALL+"{:<15}".format("Recoil-Script: ") + "{:<5}".format(((colorama.Fore.BLUE + str(True)) if rcson else (colorama.Fore.RED + str(False)))) + colorama.Style.RESET_ALL+"\n"
	outStr += "Game selected: " + "{:<15}".format(((colorama.Fore.BLUE + str(True)) if aPid==nPid else (colorama.Fore.RED + str(False)))) + colorama.Style.RESET_ALL+"{:<15}".format("Rapidfire: ") + "{:<5}".format(((colorama.Fore.BLUE + str(True)) if rapidFire else (colorama.Fore.RED + str(False)))) + colorama.Style.RESET_ALL+"\n"
	outStr += "Overlay      : " + "{:<15}".format(((colorama.Fore.BLUE + str(True)) if toggleOverlayBool else (colorama.Fore.RED + str(False))))
	outStr += "\n"
	outStr += "\n"
	outStr += colorama.Fore.YELLOW + "Keybinds:" + colorama.Style.RESET_ALL+"\n"
	outStr += "Toggle Recoil-Script	: " + dontExecute.getKeyFromValue(toggleKey)+"\n"
	outStr += "Toggle Overlay		: " + dontExecute.getKeyFromValue(toggleOverlay)+"\n"
	outStr += "Change Weapon 	   	: " + dontExecute.getKeyFromValue(leftKey)+" & "+ dontExecute.getKeyFromValue(rightKey)+"\n"
	outStr += "Change Recoil 	   	: " + dontExecute.getKeyFromValue(upKey)+" & "+ dontExecute.getKeyFromValue(downKey)+"\n"
	outStr += "Change Second Recoil	: " + dontExecute.getKeyFromValue(page_up)+" & "+ dontExecute.getKeyFromValue(page_down)+"\n"
	outStr += "Select Slot  		: 1/Numpad 1    &    2/Numpad 2\n"
	outStr += "Reload Config       	: " + dontExecute.getKeyFromValue(reloadKey)+"\n"
	outStr += "Restart Script      	: " + dontExecute.getKeyFromValue(restartKey)+"\n"
	outStr += "Exit Recoil-Script  	: " + dontExecute.getKeyFromValue(exitKey)+"\n"
	outStr += "\n"
	outStr += "Config File Path: " + os.path.realpath('config.cfg') + "\n"
	outStr += "\n"
	outStr += "\n"
	outStr += "Recoil-Table Slot 1 ("+ dontExecute.getConfig("Settings","slot1") +"): " + ','.join(dontExecute.getRecoilValues(dontExecute.getConfig("Settings","slot1")))
	outStr += "\n"
	outStr += "Recoil-Table Slot 2 ("+ dontExecute.getConfig("Settings","slot2") +"): " + ','.join(dontExecute.getRecoilValues(dontExecute.getConfig("Settings","slot2")))
	outStr += "\n"
	outStr += "\n"
	outStr += "=========================== "+ colors[colorcounter] +" Made by SiedlerLP "+ colorama.Style.RESET_ALL +" ===========================\n"
	print(outStr)

	
def restart():
	os.execv(sys.executable, ['python'] + sys.argv)


def getKeyPress():
	global aPid, count, rcValue2, rcValue1, toggleOverlay, nPid, rcson,processname, c, procfound, gameSelected, rapidFire,holdBreath,toggleOverlayBool,needSendData,lastKey, toggleKey, exitKey, reloadKey, restartKey,upKey, downKey, leftKey, rightKey, page_up,page_down, rapidFireKey, activeSlot, slot1, slot2
	
	if win32api.GetAsyncKeyState(toggleKey):
		rcson = not rcson
		sleep(0.2)
		drawScreen()
		
	if win32api.GetAsyncKeyState(exitKey):
		print('RCS SHUTTING DOWN')
		sleep(1)
		os.system('cls')
		exit()
		
	if win32api.GetAsyncKeyState(toggleOverlay):
		toggleOverlayBool = not toggleOverlayBool
		drawScreen()
		
	if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('1')) or win32api.GetAsyncKeyState(dontExecute.getValueFromKey('Numpad 1')):
		activeSlot = 1
		
	if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('2')) or win32api.GetAsyncKeyState(dontExecute.getValueFromKey('Numpad 2')):
		activeSlot = 2
		
	if win32api.GetAsyncKeyState(leftKey):
		if activeSlot == 1:
			slot1 = dontExecute.getNextItem(slot1,True)
			dontExecute.saveConfig("Settings","slot1", slot1)
		if activeSlot == 2:
			slot2 = dontExecute.getNextItem(slot2,True)
			dontExecute.saveConfig("Settings","slot2", slot2)
			
	if win32api.GetAsyncKeyState(rightKey):
		if activeSlot == 1:
			slot1 = dontExecute.getNextItem(slot1,False)
			dontExecute.saveConfig("Settings","slot1", slot1)
		if activeSlot == 2:
			slot2 = dontExecute.getNextItem(slot2,False)
			dontExecute.saveConfig("Settings","slot2", slot2)
	
	if win32api.GetAsyncKeyState(downKey):
		if activeSlot == 1:
			rcsValues = dontExecute.getRecoilValues(slot1)
			#rcsValues[0] = str(int(rcsValues[0]) - 1)
			dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
		if activeSlot == 2:
			rcsValues = dontExecute.getRecoilValues(slot2)
			#rcsValues[0] = str(int(rcsValues[0]) - 1)
			dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
			
	if win32api.GetAsyncKeyState(upKey):
		if activeSlot == 1:
			rcsValues = dontExecute.getRecoilValues(slot1)
			#rcsValues[0] = str(int(rcsValues[0]) + 1)
			dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
		if activeSlot == 2:
			rcsValues = dontExecute.getRecoilValues(slot2)
			#rcsValues[0] = str(int(rcsValues[0]) + 1)
			dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
	
	if win32api.GetAsyncKeyState(page_down):
		if activeSlot == 1:
			rcsValues = dontExecute.getRecoilValues(slot1)
			#rcsValues[1] = str(int(rcsValues[1]) - 1)
			dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
	
		if activeSlot == 2:
			rcsValues = dontExecute.getRecoilValues(slot2)
			#rcsValues[1] = str(int(rcsValues[1]) - 1)
			dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
	
	if win32api.GetAsyncKeyState(page_up):
		if activeSlot == 1:
			rcsValues = dontExecute.getRecoilValues(slot1)
			#rcsValues[1] = str(int(rcsValues[1]) + 1)
			dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
		if activeSlot == 2:
			rcsValues = dontExecute.getRecoilValues(slot2)
			#rcsValues[1] = str(int(rcsValues[1]) + 1)
			dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
			
	if win32api.GetAsyncKeyState(reloadKey):
		loadConfig()
		
	if win32api.GetAsyncKeyState(restartKey):
		print('RCS RESTARTING IN 2sec')
		sleep(2)
		restart()
		
	if mouse.is_pressed(button='right'):
		if holdBreath == False:
			keyboard.send(int(0xA0))
			holdBreath = True
			sleep(1)
		else:
			keyboard.send(int(0xA0))
			holdBreath = False	
			sleep(1)
		


if not os.path.exists('config.cfg'):
	dontExecute.writeConfig()
else:
	if dontExecute.checkConfig():
		print("Everything is up-to-date")
	else:
		print(" Your Configfile is outdated!")
		print(" Please save your current config file")
		print(" Delete the original one (config.cfg)")
		print(" And run the script again to create a new config file")
		print(" after that you can update your changes from the old config file to the new one")
		exit()

os.system('mode con: cols=81 lines=31')
ctypes.windll.kernel32.SetConsoleTitleW("No Recoil Script V"+version+ "     Made by SiedlerLP")
loadConfig()
drawScreen()

while True:
	if procfound:
		if dontExecute.processExists(processname) == False:
			procfound = False
			gameSelected = False
			rapidFire = False
			activeSlot = 0
			aPid = 0
			nPid = 1
		else:
			try:
				aPid = int(dontExecute.activeWindow())
				nPid = int(dontExecute.neededWindow(processname))
			except:
				aPid = 0
				nPid = 1
				drawScreen()
			if (aPid == nPid):
				if mouse.is_pressed(button='right'):
					if holdBreath == False:
						keyboard.send(int(0xA0))
					else:
						keyboard.send(int(0xA0))
				if gameSelected == False:
					gameSelected = True
					drawScreen()
				getKeyPress()
				while rcson is True:
					try:
						aPid = int(dontExecute.activeWindow())
						nPid = int(dontExecute.neededWindow(processname))
					except:
						aPid = 0
						nPid = 1
						drawScreen()
					if aPid != nPid:
						gameSelected = False
						rapidFire = False
						rcson = False
						aPid = 0
						nPid = 1
						drawScreen()
					else:
						count = 0
						while mouse.is_pressed(button='left'):
							if rapidFire:
								mouse.release(button='left')
								mouse.press(button="left")
							if activeSlot != 0:
								rndopt = randint(0,1)
								if rndopt == 1:
									randomized = randint(0,5)
								elif rndopt == 0:
									randomized = random.uniform(0,-5)
								rcsValue = dontExecute.getRecoilValues((slot1 if activeSlot==1 else (slot2 if activeSlot==2 else slot1)))
								if(count >= len(rcsValue)):
									count = 0    
								ammount = int(rcsValue[count])
								if rndopt == 1:
									ammount = ammount + randomized
								elif rndopt == 0:
									ammount = ammount - randomized
								ammountFinal = int(round(ammount))
								win32api.mouse_event(0x0001,0,ammountFinal)
								count = count + 1
							sleep(0.1) 
							
					getKeyPress()
						
				getKeyPress()
			else:
				if gameSelected == True or rapidFire == True or rcson == True:
					gameSelected = False
					rapidFire = False
					rcson = False
					aPid = 0
					nPid = 1
					drawScreen()
				getKeyPress()
				sleep(0.1)
	else:
		getKeyPress()
		if dontExecute.processExists(processname):
			error_code = [colorama.Style.RESET_ALL,""]
			procfound = True
			drawScreen()
		sleep(0.1)
	sleep(0.1)