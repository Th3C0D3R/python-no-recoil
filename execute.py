import win32api
import mouse
from time import sleep
import random
from random import randint
import dontExecute
import os, time, sys

# vars
rcson = False
procfound = False
rapidFire = False
rndopt = randint(0,1)
lastKey, toggleKey, exitKey, reloadKey, restartKey, upKey, downKey, leftKey, rightKey, page_up, page_down, rapidFireKey, activeSlot, slot1, slot2, slot3, aPid, count = (0,)*18
nPid = 1
searchname = "TslGame" #PUBG = TlsGame
error_code = [dontExecute.bcolors.ENDC,""]

def loadConfig():
	global toggleKey, exitKey, reloadKey,restartKey, upKey, downKey, leftKey, rightKey, page_up, page_down, rapidFireKey, configLoaded, slot1, slot2, slot3
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
	slot1 = str(dontExecute.getConfig("Settings","slot1"))
	slot2 = str(dontExecute.getConfig("Settings","slot2"))
	slot3 = str(dontExecute.getConfig("Settings","slot3"))
	
def drawScreen():
	os.system('cls' if os.name=='nt' else 'clear')
	outStr  = "============No-Recoil-Script V3============\n"
	outStr += "\n"
	outStr += "Process found: " + str(procfound)+"\n"
	outStr += "Game selected: " + str(aPid == nPid)+"\n"
	outStr += "Recoil-Script: " + (str(True) if rcson else str(False))+"\n"
	outStr += "Rapidfire    : " + (str(True) if rapidFire else str(False))+"\n"
	outStr += "\n"
	outStr += "Keybinds:\n"
	outStr += "Toggle Recoil-Script	: " + dontExecute.getKeyFromValue(toggleKey)+"\n"
	outStr += "Toggle Rapidfire 	: " + dontExecute.getKeyFromValue(rapidFireKey)+"\n"
	outStr += "Change Weapon 	   	: " + dontExecute.getKeyFromValue(leftKey)+" and "+ dontExecute.getKeyFromValue(rightKey)+"\n"
	outStr += "for current Slot\n"
	outStr += "Lower Recoil 	   	: " + dontExecute.getKeyFromValue(downKey)+"\n"
	outStr += "Higher Recoil 	   	: " + dontExecute.getKeyFromValue(upKey)+"\n"
	outStr += "Lower Second Recoil 	: " + dontExecute.getKeyFromValue(page_up)+"\n"
	outStr += "Higher Second Recoil	: " + dontExecute.getKeyFromValue(page_down)+"\n"
	outStr += "Select Slot 1		: Numpad 1 or 1\n"
	outStr += "Select Slot 2		: Numpad 2 or 3\n"
	outStr += "Select Slot 3		: Numpad 2 or 3\n"
	outStr += "Exit Recoil-Script  	: " + dontExecute.getKeyFromValue(exitKey)+"\n"
	outStr += "Reload Config       	: " + dontExecute.getKeyFromValue(reloadKey)+"\n"
	outStr += "Restart Script      	: " + dontExecute.getKeyFromValue(restartKey)+"\n"
	outStr += "\n"
	outStr += "\n"
	outStr += "Weapon Slot 1:    	" + slot1 + ("       Active " if activeSlot==1 else "" )+"\n"
	outStr += "Recoil-Value:		" + str(dontExecute.getRecoilValues(slot1)[0])+"\n"
	outStr += "Recoil-Value Second:	" + str(dontExecute.getRecoilValues(slot1)[1])+"\n"
	outStr += "\n"
	outStr += "Weapon Slot 2:    	" + slot2 + ("       Active " if activeSlot==2 else "" )+"\n"
	outStr += "Recoil-Value:     	" + str(dontExecute.getRecoilValues(slot2)[0])+"\n"
	outStr += "Recoil-Value Second:	" + str(dontExecute.getRecoilValues(slot2)[1])+"\n"
	outStr += "\n"
	outStr += "Weapon Slot 3:    	" + slot3 + ("       Active " if activeSlot==3 else "" )+"\n"
	outStr += "Recoil-Value:     	" + str(dontExecute.getRecoilValues(slot3)[0])+"\n"
	outStr += "Recoil-Value Second:	" + str(dontExecute.getRecoilValues(slot3)[1])+"\n"
	outStr += "\n"
	outStr += error_code[0] + error_code[1] + dontExecute.bcolors.ENDC+"\n"
	outStr += "\n"
	outStr += "========================================\n"
	print(outStr)

	
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
	
while True:
	loadConfig()
	drawScreen()
	if procfound:
		if dontExecute.processExists(searchname) == False:
			procfound = False
		else:
			aPid = int(dontExecute.activeWindow())
			nPid = int(dontExecute.neededWindow(searchname))		
			if (aPid == nPid):
				error_code = [dontExecute.bcolors.ENDC,""]
				if win32api.GetAsyncKeyState(toggleKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					rcson = not rcson
					sleep(0.2)
					error_code = [dontExecute.bcolors.OKBLUE,"No-Recoil: Activate"]
				if win32api.GetAsyncKeyState(exitKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					print('RCS SHUTTING DOWN')
					sleep(1)
					os.system('cls')
					exit()
				if win32api.GetAsyncKeyState(rapidFireKey):
					rapidFire = not rapidFire
				while rcson is True:
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
							
								ammount = int(dontExecute.getRecoilValues((slot1 if activeSlot==1 else (slot2 if activeSlot==2 else (slot3 if activeSlot==3 else slot1))))[0])
							else:
								ammount = int(dontExecute.getRecoilValues((slot1 if activeSlot==1 else (slot2 if activeSlot==2 else (slot3 if activeSlot==3 else slot1))))[1])
							
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
						error_code = [dontExecute.bcolors.OKBLUE,"No-Recoil: Deactivated"]
						activeSlot = 0
						
					if win32api.GetAsyncKeyState(exitKey):
						error_code = [dontExecute.bcolors.ENDC,""]
						print('RCS SHUTTING DOWN')
						sleep(1)
						os.system('cls')
						exit()
						
					if win32api.GetAsyncKeyState(rapidFireKey):
						rapidFire = not rapidFire
						
					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('m')):
						if lastKey == 'm':
							rcson = True
						else:
							rcson = False
						lastKey  = "m"
					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('esc')):
						if lastKey == 'esc':
							rcson = True
						else:
							rcson = False
						lastKey  = "esc"
					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('tab')):
						if lastKey == 'tab':
							rcson = True
						else:
							rcson = False
						lastKey  = "tab"

					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('1')) or win32api.GetAsyncKeyState(dontExecute.getValueFromKey('Numpad 1')):
						activeSlot = 1
					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('2')) or win32api.GetAsyncKeyState(dontExecute.getValueFromKey('Numpad 2')):
						activeSlot = 2
					if win32api.GetAsyncKeyState(dontExecute.getValueFromKey('3')) or win32api.GetAsyncKeyState(dontExecute.getValueFromKey('Numpad 3')):
						activeSlot = 3
						
					if win32api.GetAsyncKeyState(leftKey):
						if activeSlot == 1:
							slot1 = dontExecute.getNextItem(slot1,True)
							dontExecute.saveConfig("Settings","slot1", slot1)
						if activeSlot == 2:
							slot2 = dontExecute.getNextItem(slot2,True)
							dontExecute.saveConfig("Settings","slot2", slot2)
						if activeSlot == 3:
							slot3 = dontExecute.getNextItem(slot3,True)
							dontExecute.saveConfig("Settings","slot3", slot3)
					if win32api.GetAsyncKeyState(rightKey):
						if activeSlot == 1:
							slot1 = dontExecute.getNextItem(slot1,False)
							dontExecute.saveConfig("Settings","slot1", slot1)
						if activeSlot == 2:
							slot2 = dontExecute.getNextItem(slot2,False)
							dontExecute.saveConfig("Settings","slot2", slot2)
						if activeSlot == 3:
							slot3 = dontExecute.getNextItem(slot3,False)
							dontExecute.saveConfig("Settings","slot3", slot3)
							
					if win32api.GetAsyncKeyState(downKey):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[0] = str(int(rcsValues[0]) - 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[0] = str(int(rcsValues[0]) - 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
						if activeSlot == 3:
							rcsValues = dontExecute.getRecoilValues(slot3)
							rcsValues[0] = str(int(rcsValues[0]) - 1)
							dontExecute.saveConfig("Weapons",slot3, ','.join(rcsValues))
					if win32api.GetAsyncKeyState(upKey):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[0] = str(int(rcsValues[0]) + 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[0] = str(int(rcsValues[0]) + 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
						if activeSlot == 3:
							rcsValues = dontExecute.getRecoilValues(slot3)
							rcsValues[0] = str(int(rcsValues[0]) + 1)
							dontExecute.saveConfig("Weapons",slot3, ','.join(rcsValues))
							
					if win32api.GetAsyncKeyState(page_down):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[1] = str(int(rcsValues[1]) - 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[1] = str(int(rcsValues[1]) - 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
						if activeSlot == 3:
							rcsValues = dontExecute.getRecoilValues(slot3)
							rcsValues[1] = str(int(rcsValues[1]) - 1)
							dontExecute.saveConfig("Weapons",slot3, ','.join(rcsValues))
					if win32api.GetAsyncKeyState(page_up):
						if activeSlot == 1:
							rcsValues = dontExecute.getRecoilValues(slot1)
							rcsValues[1] = str(int(rcsValues[1]) + 1)
							dontExecute.saveConfig("Weapons",slot1, ','.join(rcsValues))
						if activeSlot == 2:
							rcsValues = dontExecute.getRecoilValues(slot2)
							rcsValues[1] = str(int(rcsValues[1]) + 1)
							dontExecute.saveConfig("Weapons",slot2, ','.join(rcsValues))
						if activeSlot == 3:
							rcsValues = dontExecute.getRecoilValues(slot3)
							rcsValues[1] = str(int(rcsValues[1]) + 1)
							dontExecute.saveConfig("Weapons",slot3, ','.join(rcsValues))
							
					if win32api.GetAsyncKeyState(reloadKey):
						error_code = [dontExecute.bcolors.ENDC,""]
						loadConfig()
						error_code = [dontExecute.bcolors.OKGREEN,"Info: Config successfull reloaded"]
						
					if win32api.GetAsyncKeyState(restartKey):
						print('RCS RESTARTING IN 2sec')
						sleep(2)
						restart()
					sleep(0.1)
			else:
				if win32api.GetAsyncKeyState(toggleKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					error_code = [dontExecute.bcolors.FAIL,"ERROR: Target Window is not selected"]
				if win32api.GetAsyncKeyState(exitKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					print('RCS SHUTTING DOWN')
					sleep(1)
					os.system('cls')
					exit()
				if win32api.GetAsyncKeyState(reloadKey):
					error_code = [dontExecute.bcolors.ENDC,""]
					loadConfig()
					error_code = [dontExecute.bcolors.OKGREEN,"Info: Config successfull reloaded"]
					rcson = False
				if win32api.GetAsyncKeyState(restartKey):
					print('RCS RESTARTING IN 2sec')
					sleep(2)
					restart()
	else:
		if win32api.GetAsyncKeyState(reloadKey):
			error_code = [dontExecute.bcolors.ENDC,""]
			loadConfig()
			error_code = [dontExecute.bcolors.OKGREEN,"Info: Config successfull reloaded"]
		if win32api.GetAsyncKeyState(toggleKey):
			error_code = [dontExecute.bcolors.ENDC,""]
			error_code = [dontExecute.bcolors.FAIL,'ERROR: Target Process is not running']
		if win32api.GetAsyncKeyState(exitKey):
			error_code = [dontExecute.bcolors.ENDC,""]
			print('RCS SHUTTING DOWN')
			sleep(1)
			os.system('cls')
			exit()
		if win32api.GetAsyncKeyState(restartKey):
			print('RCS RESTARTING IN 2sec')
			sleep(2)
			restart()
		if dontExecute.processExists(searchname):
			error_code = [dontExecute.bcolors.ENDC,""]
			procfound = True
		sleep(0.1)
	sleep(0.1)
