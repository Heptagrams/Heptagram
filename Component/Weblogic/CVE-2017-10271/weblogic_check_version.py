#!/usr/bin/env python
#coding:utf-8
import re
import time
import socket
import requests
import sys

headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'}
timeout = 5

'''
check weblogic by 404
'''
def check_weblogic(host,port):
    url = 'http://{}:{}/conso1e'.format(host,port)
    try:
        r = requests.get(url,headers = headers ,timeout =timeout)
        #guess by headers:
        result1,msg1 = check_weblogic_by_header(r.headers)
        #check by t3:
        if r.status_code == 404 and 'From RFC 2068' in r.text:
            result2,msg2 = check_weblogic_by_t3(host,port)
        #set the result and version:
        if result2:
            result = result2
            msg = msg2
        else:
            result = result1
            msg = msg1 if result1 else msg2
        return result,msg
    except requests.exceptions.ConnectionError:
        return (False,'ConnectionError')
    except :
        #raise
        return (False,'request weblogic fail')

'''
get weblogic version by t3
modifide by weblogic-t3-info.nse of nmap script
'''
def check_weblogic_by_t3(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        # Send headers
        headers = 't3 11.1.2\nAS:2048\nHL:19\n\n'
        # print 'sending Hello'
        sock.sendall(headers)
        data = ''
        #receive data and check version:
        try:
            while True:
                data += sock.recv(1024).strip()
                #print data
                if not data.startswith('HELO'):
                    return (False, 'check version fail')
                m = re.findall(r'HELO:(\d+\.\d+\.\d+\.\d+)\.',data)
                if m:
                    return (True,m[0])
                time.sleep(0.1)
        except socket.timeout:
            return (False,'weblogic unknown version') 
    except Exception, e:
        #raise
        return (False, 'check version fail')
    finally:
        sock.close()

def check_weblogic_by_header(headers):
    status,msg = False,'may be not weblogic'
    if 'X-Powered-By' in headers:
        m = re.findall(r'Servlet/(.+)\s+JSP/(.+)',headers['X-Powered-By'])
        if m :
            Servlet,JSP = m[0]
            if Servlet == '2.4' and JSP == '2.0':
                status = True
                msg = 'weblogic 9.x'
            elif Servlet == '2.5' and JSP == '2.1':
                status = True
                msg = 'weblogic 10.x'
            elif Servlet == '3.0' and JSP == '2.2':
                status = True
                msg = 'weblogicc 12.x'
    return status,msg

def main():
    if len(sys.argv) != 3:
        print 'usage:{} <ip> <port>'.format(sys.argv[0])
        exit()
   
    result,msg = check_weblogic(sys.argv[1],int(sys.argv[2]))
    print '{}'.format(msg)
        
if __name__ == '__main__':
    main()
