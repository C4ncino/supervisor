import threading
import os

#os.system("nmap -sn 192.178.57.0/24 | awk '/Nmap scan/{gsub(/[()]/,,); print  > nmap_scanned_ips}'")
os.system("nmap -sn 192.178.57.0/24 > output")
