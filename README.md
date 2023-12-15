# find-import-function
Finding which dynamic library a specific imported function belongs to in a binary file.

Search in current directory by default.

## usage
```sh
┌──(root㉿kali)-[~]
└─# /bin/python /root/.code/search.py
[*] usage: python /root/.code/search.py <binary> <first_expect_fun> [ second_expect_fun ...]
```

## example
```sh
┌──(root㉿kali)-[~]
└─# /bin/python /root/.code/search.py libuflua.so uf_client_call read
[*] read is not an import function!
[+] Found uf_client_call in libunifyframe.so!
[+] all done!
```
