import sys
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import paramiko

import logInfo

class Client():
    def __init__(self, name, IP, userName, passWord, exit_event):
        self.name = name
        self.hostname = IP
        self.username=userName
        self.password=passWord
        self.exitevent = exit_event
        self.alive = True
        
        self.monitorURL()
        

    def softReboot(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh_client.connect(hostname=self.hostname,username=self.username,password=self.password)
        except:
            ssh_client.close
            ssh_client = None
            errmsg = "Failed to connect: %s, username: %s, password: %s" % (self.hostname, self.username, self.password)
            return

        ssh_client.exec_command("shutdown /t 0 /r")
        ssh_client.close
        self.alive = True # soft reboot success.
        
    def exceptionHandling(self):
        self.softReboot()    
                
    def monitorURL(self):
        url = '****************'
        
        while not self.exitevent.is_set():
            try:
                req = urlopen(url, data=None)
                status = "Status Code: %d" %(req.getcode())
                print(req.getcode())
                
            except HTTPError as e:
                self.alive = False
                errmsg = "Error code: %d" % (e.code)
                self.exceptionHandling()
            
            except URLError as e:
                self.alive = False
                errmsg = "Reason: %s" % (e.reason)
                self.exceptionHandling()
                                        
            self.exitevent.wait(300) #wait for 15 minutes
              
        self.exitevent.clear()
        sys.exit(0)
            
        

        
        














    
