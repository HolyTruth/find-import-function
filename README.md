# find-import-function
Find out which lib the imported function belongs to

```py
┌──(root㉿kali)-[~]
└─# /bin/python /root/.code/search.py libuflua.so uf_client_call read
[*] read is not an import function!
[+] Found uf_client_call in libunifyframe.so!
[+] all done!
