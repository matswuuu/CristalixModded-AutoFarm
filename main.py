import time
from configparser import ConfigParser
from art import tprint
import win32gui, win32api
import pyautogui

tprint('AutoFarm')
config = ConfigParser()
pyautogui.PAUSE = 2

def check_answer(name):
    if name == 'да':
        return True
    else:
        return False

def new_config():
    save = input('Сохранить конфигурацию? (да/нет): ')
    save = check_answer(save)
    
    servers = [ 'NeoTech-1', 'Magica-1', 'Magica-2', 'Magica-3', 'DivinePVP-1', 'TechnoMagic-1', 'TechnoMagic-2', 'SkyVoid-1', 'SkyVoid-2', 'Galax-1' ]
    server = 1
    for i in servers:
        print(str(server) + '. ' + i)
        server = server + 1 

    server_input = input('Введите номер сервера: ')
    global server_name
    if server_input == '1': # NeoTech-1
        server_name = 'NeoTech'
    elif server_input == '2': # Magica-1
        server_name = 'Magica'
    elif server_input == '3': # Magica-2
        server_name = 'Magica'
    elif server_input == '4': # Magica-3
        server_name = 'Magica'
    elif server_input == '5': # DivinePVP-1
        server_name = 'DivinePVP'
    elif server_input == '6': # TechnoMagic-1
        server_name = 'Technomagic'
    elif server_input == '7': # TechnoMagic-2
        server_name = 'Technomagic'
    elif server_input == '8': # SkyVoid-1
        server_name = 'SkyVoid'
    elif server_input == '9': # SkyVoid-2
        server_name = 'SkyVoid'
    elif server_input == '10': # Galax-1
        server_name = 'Galax'

    global nickname
    nickname = input('Введите Ваш ник (с учетом расскладки!): ')
    
    global ores_warp
    ores_warp = input('Введите названия варпа с рудой: ')

    global ores_slot
    ores_slot = input('Введите номер слота с киркой: ')
    
    warps_amount = input('Введите количетсво варпов с мобами: ')
    for i in range(1, int(warps_amount) + 1):
        config['Config'][str(i) + '_mobs_warp'] = input('Введите название варпа: ')
        
        config['Config_1']['warps_amount'] = warps_amount

        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    
    global mobs_slot
    mobs_slot = input('Введите номер слота с мечом: ')
    
    global interval
    interval = input('Введите промежуток между подходами (в минутах): ')

    if save:
        config['Config']['save'] = str(save)
        config['Config']['server_name'] = server_name
        config['Config']['nickname'] = nickname
        config['Config']['ores_warp'] = ores_warp
        config['Config']['ores_slot'] = ores_slot
        config['Config']['mobs_slot'] = mobs_slot
        config['Config']['interval'] = interval
               
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

config.read_file(open(r'config.ini'))
save = eval(config.get('Config', 'save'))      
if save:  
    print('Последняя конфигурация: ')
    for con in config['Config']:
        print(con + ' = ' + config['Config'][con])

    choice = input('Загрузить прошлую конфигурацию? (да/нет): ')
    if check_answer(choice):
        server_name = config.get('Config', 'server_name')
        ores_warp = config.get('Config', 'ores_warp')
        ores_slot = config.get('Config', 'ores_slot')
        mobs_slot = config.get('Config', 'mobs_slot')
        interval = config.get('Config', 'interval')
        nickname = config.get('Config', 'nickname')
    else:
        new_config()
else:
    new_config()

def set_foreground():
    window = pyautogui.getWindowsWithTitle(f'Cristalix {server_name} » {nickname}')[0]
    window.maximize()
    window.restore()
    window.minimize()
    window.restore()
    window.activate()

def tp(name):
    for i in range(2):
        pyautogui.press('t')
        pyautogui.typewrite(name, interval=0.25)
        pyautogui.press('enter')

def click(slot, click_range, time_sleep):
    pyautogui.press(slot)
    for i in range(click_range):
        pyautogui.leftClick()
        time.sleep(time_sleep)

interval = int(interval) * 60
while True:
    for i in reversed(range(1, 11)):
        print('Фарм начнется через ' + str(i) + ' секунд.')
        time.sleep(1)
        
    WM_INPUTLANGCHANGEREQUEST = 0x0050
    window_handle = win32gui.GetForegroundWindow()
    win32api.SendMessage(window_handle, WM_INPUTLANGCHANGEREQUEST, 0, 0x04090409)

    set_foreground()

    tp('/warp ' + ores_warp)
    click(ores_slot, 6, 3)
    
    for i in range(1, int(config.get('Config_1', 'warps_amount')) + 1):
        tp('/warp ' + config.get('Config', str(i) + '_mobs_warp'))
        click(mobs_slot, 12, 10) 
    
    tp('/home')
    
    print('Фарм закончен.')
    time.sleep(interval)