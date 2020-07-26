# CVE-2020-3452 - Cisco ASA Scanner

Scanning for CVE-2020-3452 - unauth Path Traversal affecting Cisco ASA firewalls running anyconnect

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-3452

Supporting Documents:

https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-ro-path-KJuQhB86

https://twitter.com/aboul3la/status/1286012324722155525

Disclaimer:
I am not responsible for the use of this tool or any damages, DO NOT USE THIS FOR ILLEGAL PURPOSES.
This tool was designed to scan for authorised assets to automate the check for this vulnerability on multiple cisco instances

Introduction:

A vulnerability in the web services interface of Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to conduct directory traversal attacks and read sensitive files on a targeted system. The vulnerability is due to a lack of proper input validation of URLs in HTTP requests processed by an affected device. An attacker could exploit this vulnerability by sending a crafted HTTP request containing directory traversal character sequences to an affected device. A successful exploit could allow the attacker to view arbitrary files within the web services file system on the targeted device. The web services file system is enabled when the affected device is configured with either WebVPN or AnyConnect features

I created this script to allow a engineer to parse in a file of urls to test against.

Install:

git clone https://github.com/PR3R00T/CVE-2020-3452-Cisco-Scanner.git

chmod +x scanner.py

amend the urls.txt file with the urls https://XX.XX format.

python3 ./scanner.py

