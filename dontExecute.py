import subprocess
from subprocess import check_output
from win32gui import GetWindowText, GetForegroundWindow, FindWindow
from win32process import GetWindowThreadProcessId
import configparser, os
import win32api, win32con

def writeConfig():
	config = configparser.ConfigParser()
	config['Settings'] = {
	'default_toggle_key' : int(0x6B), 
	'default_exit_key' : int(0x6D), 
	'default_reload_key' : int(0x77),
	'default_restart_key' : int(0x76),
	'default_select_key_up': int(0x26),
	'default_select_key_down': int(0x28),
	'default_select_key_left': int(0x25),
	'default_select_key_right': int(0x27),
	'default_select_key_second_up': int(0x21),
	'default_select_key_second_down': int(0x22),
	'default_rapidFireKey': int(0x23),
	'slot1' : 'akm',
	'slot2' : 'm249',
	'slot3' : 'p1911'
	}
	
	config['Weapons'] = {
	'AKM' : '13,14',
	'AUG_A3' : '13,14',
	'DP-28' : '13,14',
	'GROZA' : '13,14',
	'M16' : '13,14',
	'ScarL' : '13,14',
	'M249' : '13,14',
	'M4' : '13,14',
	'Mini14' : '13,14',
	'MK14' : '13,14',
	'Glock' : '13,14',
	'P1911' : '13,14',
	'P92' : '13,14',
	'QBZ95' : '13,14',
	'SKS' : '13,14',
	'SLR' : '13,14',
	'UMP' : '13,14',
	'Vector' : '13,14',
	'UZI' : '13,14',
	'TommyGun' : '13,14',
	'VSS' : '13,14'
	}
	
	with open('config.cfg','w') as configfile:
		config.write(configfile)
		return True
		
def getRecoilValues(option):
	config = configparser.ConfigParser()
	config.read("config.cfg")
	rcsValues = getConfig("Weapons",option)
	return rcsValues.split(',')
	
def checkConfig():
	config = configparser.ConfigParser()
	config.read("config.cfg")
	if sectionExists("Settings"):
		if (
				sectionHasOption("Settings",'default_toggle_key') and sectionHasOption("Settings",'default_exit_key') and sectionHasOption("Settings",'default_select_key_second_down') and 
				sectionHasOption("Settings",'default_reload_key') and sectionHasOption("Settings",'default_restart_key') and sectionHasOption("Settings",'default_select_key_up') and
				sectionHasOption("Settings",'default_select_key_down') and sectionHasOption("Settings",'default_select_key_left') and sectionHasOption("Settings",'default_select_key_right') and
				sectionHasOption("Settings",'slot1') and sectionHasOption("Settings",'slot2') and sectionHasOption("Settings",'slot3') and sectionHasOption("Settings",'default_select_key_second_up') and 
				sectionHasOption("Settings",'default_rapidFireKey')):
				str = "allright"
		else:
			return False
	else:
		return False
		
	if sectionExists("Weapons"):
		if(
			sectionHasOption("Weapons",'akm') and sectionHasOption("Weapons",'aug_a3') and sectionHasOption("Weapons",'dp-28') and sectionHasOption("Weapons",'groza') and 
			sectionHasOption("Weapons",'m16') and sectionHasOption("Weapons",'m249') and sectionHasOption("Weapons",'m4') and sectionHasOption("Weapons",'mini14') and 
			sectionHasOption("Weapons",'mk14') and sectionHasOption("Weapons",'glock') and sectionHasOption("Weapons",'p1911') and sectionHasOption("Weapons",'p92') and 
			sectionHasOption("Weapons",'qbz95') and sectionHasOption("Weapons",'sks') and sectionHasOption("Weapons",'slr') and sectionHasOption("Weapons",'ump') and 
			sectionHasOption("Weapons",'vector') and sectionHasOption("Weapons",'scarl') and sectionHasOption("Weapons",'uzi') and sectionHasOption("Weapons",'tommygun') and sectionHasOption("Weapons",'vss')):
			return True
		else:
			return False
	else:
		return False
		
		
def getConfig(section, item):
	config = configparser.ConfigParser()
	config.read("config.cfg")
	return (config[section][item])

def saveConfig(section, item, value):
	config = configparser.ConfigParser()
	config.read("config.cfg")
	config.set(section, item, value)
	with open('config.cfg','w+') as configfile:
		config.write(configfile)

def sectionHasOption(section,option):
	config = configparser.ConfigParser()
	config.read("config.cfg")
	if config.has_option(section,option): 
		return True
	else: 
		return False 
		
def sectionExists(section):
	config = configparser.ConfigParser()
	config.read("config.cfg")
	if config.has_section(section): 
		return True
	else: 
		return False
	
def processExists(searchname):
	n=0
	prog=[line.split() for line in subprocess.check_output("tasklist").splitlines()]
	[prog.pop(e) for e in [0,1,2]]
	for task in prog:
		progname = task[0].decode("utf-8")
		if progname==searchname+".exe":
			n=n+1
	if n>0:
		return True
	else:
		return False
	return
	
def neededWindow(name):
	n=0
	prog=[line.split() for line in subprocess.check_output("tasklist").splitlines()]
	[prog.pop(e) for e in [0,1,2]]
	for task in prog:
		progname = task[0].decode("utf-8")
		if progname==name+".exe":
			return task[1].decode("utf-8")

def activeWindow():
	try:
		title = GetWindowText(GetForegroundWindow())
		return get_window_pid(title)
	except:
		pass

def get_window_pid(title):
	hwnd = FindWindow(None,title)
	threadid,pid = GetWindowThreadProcessId(hwnd)
	return pid
	
def getKeyFromValue(searchvalue):
	for key, value in VK_CODE.items():
		if str(value) == str(searchvalue):
			return str(key)

def getValueFromKey(searchKey):
	for key, value in VK_CODE.items():
		if str(key) == str(searchKey):
			return int(value)

def lengthSection(section):
	length = 0
	config = configparser.ConfigParser()
	config.read("config.cfg")
	for key in config[section]:
		length += 1
	return length
	
def indexOfItem(section, item):
	pos = 0
	config = configparser.ConfigParser()
	config.read("config.cfg")
	for key in config[section]:
		if key != item:
			pos += 1
		else:
			break
	return pos
	
def getNextItem(curItem, up):
	config = configparser.ConfigParser()
	config.read("config.cfg")
	lenWeapons = lengthSection("Weapons")
	indCurr = indexOfItem("Weapons", curItem)
	if up:
		if indCurr == 0:
			indCurr = lenWeapons-1
		else:
			indCurr -= 1
	else:
		if indCurr == lenWeapons-1:
			indCurr = 0
		else:
			indCurr += 1
	return list(config["Weapons"].keys())[indCurr]
	
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

VK_CODE = {'backspace':int(0x08),'tab':int(0x09),'clear':int(0x0C),'enter':int(0x0D),'shift':int(0x10),'ctrl':int(0x11),'alt':int(0x12),'pause':int(0x13),'caps_lock':int(0x14),'esc':int(0x1B),'spacebar':int(0x20),'Page Up':int(0x21),'Page Down':int(0x22),'End':int(0x23),'home':int(0x24),'Arrow left':int(0x25),'Arrow up':int(0x26),'Arrow right':int(0x27),'Arrow down':int(0x28),'select':int(0x29),'print':int(0x2A),'execute':int(0x2B),'print_screen':int(0x2C),'ins':int(0x2D),'del':int(0x2E),'help':int(0x2F),'0':int(0x30),'1':int(0x31),'2':int(0x32),'3':int(0x33),'4':int(0x34),'5':int(0x35),'6':int(0x36),'7':int(0x37),'8':int(0x38),'9':int(0x39),'a':int(0x41),'b':int(0x42),'c':int(0x43),'d':int(0x44),'e':int(0x45),'f':int(0x46),'g':int(0x47),'h':int(0x48),'i':int(0x49),'j':int(0x4A),'k':int(0x4B),'l':int(0x4C),'m':int(0x4D),'n':int(0x4E),'o':int(0x4F),'p':int(0x50),'q':int(0x51),'r':int(0x52),'s':int(0x53),'t':int(0x54),'u':int(0x55),'v':int(0x56),'w':int(0x57),'x':int(0x58),'y':int(0x59),'z':int(0x5A),'Numpad 0':int(0x60),'Numpad 1':int(0x61),'Numpad 2':int(0x62),'Numpad 3':int(0x63),'Numpad 4':int(0x64),'Numpad 5':int(0x65),'Numpad 6':int(0x66),'Numpad 7':int(0x67),'Numpad 8':int(0x68),'Numpad 9':int(0x69),'Multiply':int(0x6A),'Numpad Add':int(0x6B),'separator_key':int(0x6C),'Numpad Subtract':int(0x6D),'decimal_key':int(0x6E),'Divide':int(0x6F),'F1':int(0x70),'F2':int(0x71),'F3':int(0x72),'F4':int(0x73),'F5':int(0x74),'F6':int(0x75),'F7':int(0x76),'F8':int(0x77),'F9':int(0x78),'F10':int(0x79),'F11':int(0x7A),'F12':int(0x7B),'F13':int(0x7C),'F14':int(0x7D),'F15':int(0x7E),'F16':int(0x7F),'F17':int(0x80),'F18':int(0x81),'F19':int(0x82),'F20':int(0x83),'F21':int(0x84),'F22':int(0x85),'F23':int(0x86),'F24':int(0x87),'num_lock':int(0x90),'scroll_lock':int(0x91),'left_shift':int(0xA0),'right_shift ':int(0xA1),'left_control':int(0xA2),'right_control':int(0xA3),'left_menu':int(0xA4),'right_menu':int(0xA5),'browser_back':int(0xA6),'browser_forward':int(0xA7),'browser_refresh':int(0xA8),'browser_stop':int(0xA9),'browser_search':int(0xAA),'browser_favorites':int(0xAB),'browser_start_and_home':int(0xAC),'volume_mute':int(0xAD),'volume_Down':int(0xAE),'volume_up':int(0xAF),'next_track':int(0xB0),'previous_track':int(0xB1),'stop_media':int(0xB2),'play/pause_media':int(0xB3),'start_mail':int(0xB4),'select_media':int(0xB5),'start_application_1':int(0xB6),'start_application_2':int(0xB7),'attn_key':int(0xF6),'crsel_key':int(0xF7),'exsel_key':int(0xF8),'play_key':int(0xFA),'zoom_key':int(0xFB),'clear_key':int(0xFE),'+':int(0xBB),'),':int(0xBC),'-':int(0xBD),'.':int(0xBE),'/':int(0xBF),'`':int(0xC0),';':int(0xBA),'[':int(0xDB),'\\':int(0xDC),']':int(0xDD),"'":int(0xDE),'`':int(0xC0)}



