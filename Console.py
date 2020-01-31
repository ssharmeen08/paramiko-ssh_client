#!/usr/bin/env python3

import sys
import logInfo
import signal
import threading
import array as arr
from Client import Client

exit_event = threading.Event()

def exitFunc(signum, frame):
    global exit_event
    exit_event.set()
    print('Signal handler called with signal [%s]' % signum)

def main():
    
    print('To close the app press Ctrl+C')
    config = []

    with open('config', 'r') as file:
        for line in file:
            fields = line.strip().split()
            config.append(fields[2])
            
    print(config)
    global exit_event
    
    signal.signal(signal.SIGINT, exitFunc)

    aClient = Client('client', config[0], config[1], config[2], exit_event)
    

if __name__ == "__main__":
    main()
