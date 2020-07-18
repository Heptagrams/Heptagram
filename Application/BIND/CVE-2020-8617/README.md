# CVE-2020-8617
PoC for CVE-2020-8617

For educational purposes only

![demo](imgs/CVE-2020-8617.gif)

## Run
This image runs a standard BIND server, which automatically generates a tkey "local-ddns".

```
$ docker run --rm --name cve-2020-8617 -it -p 53:53/udp knqyf263/cve-2020-8617
```

## Exploit

```
$ pipenv install
$ pipenv run python exploit.py
```

## Reference
- https://kb.isc.org/docs/cve-2020-8617

## Author
Teppei Fukuda
