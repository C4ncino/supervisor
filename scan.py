import threading
import os

def scan_network(ip):
    tokens = ip.split(".")
    # scan the network for alive hosts
    #os.system(f"nmap -sn {tokens[0]}.{tokens[1]}.{tokens[2]}.0/24  192.178.57.0/24 | awk '/Nmap scan report for/{print $NF}' | awk '{gsub(/[()]/,\"\")}1' > output")
    os.system(f"nmap -sn {tokens[0]}.{tokens[1]}.{tokens[2]}.0/24 | awk '/Nmap scan report for/{print $NF}' | awk '{gsub(/[()]/,\"\")}1' > output")
