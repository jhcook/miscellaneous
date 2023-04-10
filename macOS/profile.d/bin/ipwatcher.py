#!/usr/bin/env python3.10
#
# This code receives notification of a local IP address change and sends
# SIGUSR1 to all Bash processes. Bash needs to trap USR1 accordingly.
#
# Requires: 
# * pyobjc-framework-SystemConfiguration
# * psutil
#
# Author: Justin Cook
#         abarnert
#         Varun
#
# References: 
# * https://stackoverflow.com/questions/11532144/how-to-detect-ip-address-change-on-osx-programmatically-in-c-or-c
# * https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/

from Foundation import *
from SystemConfiguration import *
from os import kill
from signal import SIGUSR1
import psutil

def callback(store, keys, info):
  for key in keys:
    listOfProcessIds = findProcessIdByName('bash')
    if len(listOfProcessIds) > 0:
      for elem in listOfProcessIds:
        processID = elem['pid']
        try:
          kill(processID, SIGUSR1)
        except PermissionError:
          pass
			
def findProcessIdByName(processName):
    '''
    Create a list of all running process PIDs whose name contains the string
    processName.
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied,
               psutil.ZombieProcess):
           pass
    return listOfProcessObjects

if __name__ == '__main__':
    store = SCDynamicStoreCreate(None, "global-network-watcher", callback, None)
    SCDynamicStoreSetNotificationKeys(store, None,
                                      ['State:/Network/Global/IPv4'])
    CFRunLoopAddSource(CFRunLoopGetCurrent(),
                       SCDynamicStoreCreateRunLoopSource(None, store, 0),
                       kCFRunLoopCommonModes)
    CFRunLoopRun()
