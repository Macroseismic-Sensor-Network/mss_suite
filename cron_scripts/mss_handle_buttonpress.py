#!/usr/bin/env python3

import configparser
import signal
import subprocess
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO = None

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    subprocess.call(['sudo', 'systemctl', 'start', 'hostapd.service'])

    
def load_configuration(filename):
    ''' Load the configuration from a file.
    '''
    parser = configparser.ConfigParser()
    parser.read(filename)

    config = {}
    config['pcb'] = {}
    config['pcb']['pcb_version'] = int(parser.get('pcb', 'pcb_version').strip())

    return config

if __name__ == '__main__':
    config = load_configuration('/home/mss/config/mss_record.ini')
    if config['pcb']['pcb_version'] == 1:
        BUTTON_GPIO = 26
    elif config['pcb']['pcb_version'] == 2:
        BUTTON_GPIO = 4
        
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING,
                          callback=button_pressed_callback,
                          bouncetime=100)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
