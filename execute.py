import win32api
import mouse
from time import sleep
import random
from random import randint
import dontExecute
import os, time, sys
from threading import Timer
import ctypes

# vars
version = "2.3"
rcson = False
procfound = False
rapidFire = False
rndopt = randint(0,1)
lastKey, toggleKey, exitKey, reloadKey, restartKey, upKey, downKey, leftKey, rightKey, page_up, page_down, rapidFireKey, activeSlot, slot1, slot2, slot3, aPid, count = (0,)*18
nPid = 1
processname = "TslGame" #PUBG = TslGame
error_code = [dontExecute.bcolors.ENDC,""]
somethingChanged = False
gameSelected = False

def loadConfig():
	global toggleKey, exitKey, reloadKey,restartKey, upKey, downKey, leftKey, rightKey, page_up, page_down,processname, rapidFireKey, configLoaded, slot1, slot2, slot3, somethingChanged
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
	processname = str(dontExecute.getConfig("Settings","default_processname"))
	slot1 = str(dontExecute.getConfig("Settings","slot1"))
	slot2 = str(dontExecute.getConfig("Settings","slot2"))
	slot3 = str(dontExecute.getConfig("Settings","slot3"))
	somethingChanged = True
	
def drawScreen():
	global somethingChanged
	if somethingChanged:
		os.system('cls' if os.name=='nt' else 'clear')
		outStr  = "========================= "+ dontExecute.bcolors.HEADER +" No-Recoil-Script V"+version+" "+ dontExecute.bcolors.ENDC +" =========================\n"
		outStr += "\n"
		outStr += dontExecute.bcolors.YELLOW + "Status:"+ dontExecute.bcolors.ENDC+"\n"
		outStr += "Process found: " + "{:<15}".format(((dontExecute.bcolors.BLUE + str(True)) if procfound else (dontExecute.bcolors.RED + str(False)))) + dontExecute.bcolors.ENDC+"{:<15}".format("Recoil-Script: ") + "{:<5}".format(((dontExecute.bcolors.BLUE + str(True)) if rcson else (dontExecute.bcolors.RED + str(False)))) + dontExecute.bcolors.ENDC+"\n"
		outStr += "Game selected: " + "{:<15}".format(((dontExecute.bcolors.BLUE + str(True)) if aPid==nPid else (dontExecute.bcolors.RED + str(False)))) + dontExecute.bcolors.ENDC+"{:<15}".format("Rapidfire: ") + "{:<5}".format(((dontExecute.bcolors.BLUE + str(True)) if rapidFire else (dontExecute.bcolors.RED + str(False)))) + dontExecute.bcolors.ENDC+"\n"
		outStr += "\n"
		outStr += "\n"
		outStr += dontExecute.bcolors.YELLOW + "Weapon Selection:" + dontExecute.bcolors.ENDC+"\n"
		outStr += (dontExecute.bcolors.GREEN if activeSlot==1 else dontExecute.bcolors.ENDC ) + "Weapon Slot 1:    	" + "{:<8}".format(slot1) + dontExecute.bcolors.ENDC + (dontExecute.bcolors.GREEN if activeSlot==2 else dontExecute.bcolors.ENDC ) + "       Weapon Slot 2:    	" + slot2 + dontExecute.bcolors.ENDC+"\n"
		outStr += (dontExecute.bcolors.GREEN if activeSlot==1 else dontExecute.bcolors.ENDC ) + "Recoil-Value:		" + "{:<3}".format(str(dontExecute.getRecoilValues(slot1)[0]))+ dontExecute.bcolors.ENDC + (dontExecute.bcolors.GREEN if activeSlot==2 else dontExecute.bcolors.ENDC ) +"            Recoil-Value:     	" + "{:<3}".format(str(dontExecute.getRecoilValues(slot2)[0])) + dontExecute.bcolors.ENDC+"\n"
		outStr += (dontExecute.bcolors.GREEN if activeSlot==1 else dontExecute.bcolors.ENDC ) + "Recoil-Value Second:	" + "{:<3}".format(str(dontExecute.getRecoilValues(slot1)[1]))+ dontExecute.bcolors.ENDC + (dontExecute.bcolors.GREEN if activeSlot==2 else dontExecute.bcolors.ENDC ) +"            Recoil-Value Second:	" + "{:<3}".format(str(dontExecute.getRecoilValues(slot2)[1])) + dontExecute.bcolors.ENDC+"\n"
		outStr += "\n"
		outStr += "\n"
		outStr += dontExecute.bcolors.YELLOW + "Keybinds:" + dontExecute.bcolors.ENDC+"\n"
		outStr += "Toggle Recoil-Script	: " + dontExecute.getKeyFromValue(toggleKey)+"\n"
		outStr += "Toggle Rapidfire 	: " + dontExecute.getKeyFromValue(rapidFireKey)+"\n"
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
		outStr += error_code[0] + error_code[1] + dontExecute.bcolors.ENDC+"\n"
		outStr += "\n"
		outStr += "=========================== "+ dontExecute.bcolors.HEADER +" Made by SiedlerLP "+ dontExecute.bcolors.ENDC +" ===========================\n"
		print(outStr)
		somethingChanged = False

	
def restart():
	os.execv(sys.executable, ['python'] + sys.argv)

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

loadConfig()
os.system('mode con: cols=81 lines=31')
ctypes.windll.kernel32.SetConsoleTitleW("No Recoil Script V"+version+ "     Made by SiedlerLP")

while True:
	drawScreen()
	
	if procfound:
		if dontExecute.processExists(processname) == False:
			procfound = False
			gameSelected = False
			rapidFire = False
			aPid = 0
			nPid = 1
			somethingChanged = True
		else:
			try:
				aPid = int(dontExecute.activeWindow())
				nPid = int(dontExecute.neededWindow(processname))
			except:
				aPid = 0
				nPid = 1
			if (aPid == nPid):
				if gameSelected == False:
					somethingChanged = True
					gameSelected = True
				if win32api.GetAsyncKeyState(toggleKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					rcson = not rcson
					sleep(0.2)
					error_code = [dontExecute.bcolors.YELLOW,"No-Recoil: Activate"]
					somethingChanged = True
				if win32api.GetAsyncKeyState(exitKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					somethingChanged = True
					print('RCS SHUTTING DOWN')
					sleep(1)
					os.system('cls')
					exit()
				if win32api.GetAsyncKeyState(rapidFireKey):
					rapidFire = not rapidFire
					somethingChanged = True
				while rcson is True:
					try:
						aPid = int(dontExecute.activeWindow())
						nPid = int(dontExecute.neededWindow(processname))
					except:
						aPid = 0
						nPid = 1
					if aPid != nPid:
						gameSelected = False
						rapidFire = False
						rcson = False
						aPid = 0
						nPid = 1
						somethingChanged = True
					else:
						count = 0
						drawScreen()
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
								if count <= 11 or count > 21:
								
									ammount = int(dontExecute.getRecoilValues((slot1 if activeSlot==1 else (slot2 if activeSlot==2 else slot1)))[0])
								else:
									ammount = int(dontExecute.getRecoilValues((slot1 if activeSlot==1 else (slot2 if activeSlot==2 else slot1)))[1])
								
								if rndopt == 1:
									ammount = ammount + randomized
								elif rndopt == 0:
									ammount = ammount - randomized
								ammountFinal = int(round(ammount))
								win32api.mouse_event(0x0001,0,ammountFinal)
								count = count + 1
							sleep(0.1) 
							
					if win32api.GetAsyncKeyState(toggleKey):
						error_code = [dontExecute.bcolors.ENDC,""]
						rcson = not rcson
						sleep(0.2)
						error_code = [dontExecute.bcolors.YELLOW,"No-Recoil: Deactivated"]
						activeSlot = 0
						somethingChanged = True
						
					if win32api.GetAsyncKeyState(exitKey):
						error_code = [dontExecute.bcolors.ENDC,""]
						somethingChanged = True
						print('RCS SHUTTING DOWN')
						sleep(1)
						os.system('cls')
						exit()
						
					if win32api.GetAsyncKeyState(rapidFireKey):
						rapidFire = not rapidFire
						somethingChanged = True
						
					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('1')) or win32api.GetAsyncKeyState(dontExecute.getValueFromKey('Numpad 1')):
						activeSlot = 1
						somethingChanged = True
					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('2')) or win32api.GetAsyncKeyState(dontExecute.getValueFromKey('Numpad 2')):
						activeSlot = 2
						somethingChanged = True

					if win32api.GetAsyncKeyState(leftKey):
						if activeSlot == 1:
							slot1 = dontExecute.getNextItem(slot1,True)
							dontExecute.saveConfig("Settings","slot1", slot1)
							somethingChanged = True
						if activeSlot == 2:
							slot2 = dontExecute.getNextItem(slot2,True)
							dontExecute.saveConfig("Settings","slot2", slot2)
							somethingChanged = True
					if win32api.GetAsyncKeyState(rightKey):
						if activeSlot == 1:
							slot1 = dontExecute.getNextItem(slot1,False)
							dontExecute.saveConfig("Settings","slot1", slot1)
							somethingChanged = True
						if activeSlot == 2:
							slot2 = dontExecute.getNextItem(slot2,False)
							dontExecute.saveConfig("Settings","slot2", slot2)
							somethingChanged = True
							
					if win32api.GetAsyncKeyState(downKey):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[0] = str(int(rcsValues[0]) - 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
							somethingChanged = True
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[0] = str(int(rcsValues[0]) - 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
							somethingChanged = True
					if win32api.GetAsyncKeyState(upKey):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[0] = str(int(rcsValues[0]) + 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
							somethingChanged = True
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[0] = str(int(rcsValues[0]) + 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
							somethingChanged = True
							
					if win32api.GetAsyncKeyState(page_down):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[1] = str(int(rcsValues[1]) - 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
							somethingChanged = True
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[1] = str(int(rcsValues[1]) - 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
							somethingChanged = True

					if win32api.GetAsyncKeyState(page_up):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[1] = str(int(rcsValues[1]) + 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
							somethingChanged = True
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[1] = str(int(rcsValues[1]) + 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
							somethingChanged = True
							
					if win32api.GetAsyncKeyState(reloadKey):
						error_code = [dontExecute.bcolors.ENDC,""]
						loadConfig()
						error_code = [dontExecute.bcolors.GREEN,"Info: Config successfull reloaded"]
						somethingChanged = True
						
					if win32api.GetAsyncKeyState(restartKey):
						print('RCS RESTARTING IN 2sec')
						sleep(2)
						restart()
					sleep(0.1)
			else:
				if gameSelected == True or rapidFire == True or rcson == True:
					gameSelected = False
					rapidFire = False
					rcson = False
					aPid = 0
					nPid = 1
					somethingChanged = True
				if win32api.GetAsyncKeyState(toggleKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					error_code = [dontExecute.bcolors.RED,"ERROR: Target Window is not selected"]
					somethingChanged = True
				if win32api.GetAsyncKeyState(exitKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					somethingChanged = True
					print('RCS SHUTTING DOWN')
					sleep(1)
					os.system('cls')
					exit()
				if win32api.GetAsyncKeyState(reloadKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					loadConfig()
					error_code = [dontExecute.bcolors.GREEN,"Info: Config successfull reloaded"]
					rcson = False
					somethingChanged = True
				if win32api.GetAsyncKeyState(restartKey):
					print('RCS RESTARTING IN 2sec')
					sleep(2)
					restart()
	else:
		if win32api.GetAsyncKeyState(reloadKey):
			error_code = [dontExecute.bcolors.ENDC,""]
			loadConfig()
			error_code = [dontExecute.bcolors.GREEN,"Info: Config successfull reloaded"]
			somethingChanged = True
		if win32api.GetAsyncKeyState(toggleKey):
			error_code = [dontExecute.bcolors.ENDC,""]
			error_code = [dontExecute.bcolors.RED,'ERROR: Target Process is not running']
			somethingChanged = True
		if win32api.GetAsyncKeyState(exitKey):
			error_code = [dontExecute.bcolors.ENDC,""]
			somethingChanged = True
			print('RCS SHUTTING DOWN')
			sleep(1)
			os.system('cls')
			exit()
		if win32api.GetAsyncKeyState(restartKey):
			print('RCS RESTARTING IN 2sec')
			sleep(2)
			restart()
		if dontExecute.processExists(processname):
			error_code = [dontExecute.bcolors.ENDC,""]
			procfound = True
			somethingChanged = True
		sleep(0.1)
	sleep(0.1)