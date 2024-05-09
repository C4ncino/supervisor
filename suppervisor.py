import os
import pyshark
import threading
from time import sleep
from datetime import datetime
from pyshark.packet.layers.xml_layer import XmlLayer
from database import DatabaseInterface, Node
from decimal import Decimal

# -----------------------------------------------------------------------------

db = DatabaseInterface()
fresh_nodes = {}
first = True

# -----------------------------------------------------------------------------

fresh_n_sem = threading.Semaphore(1)
bd_sem = threading.Semaphore(1)

# -----------------------------------------------------------------------------


def get_mbps():
    global fresh_n_sem
    global db
    global bd_sem

    while True:
        fresh_n_sem.acquire()
        bd_sem.acquire()

        mbps = 0.0

        for _, val in fresh_nodes.items():
            mbps += val / 1_000_000

        db.create_table_row('speeds', {
            'Speed': mbps,
            'Timestamp': datetime.now()
        })

        fresh_nodes.clear()

        fresh_n_sem.release()
        bd_sem.release()

        sleep(10)


def print_callback(packet):
    global db
    global fresh_nodes
    global first
    global fresh_n_sem
    global bd_sem

    try:
        ip_info: XmlLayer = packet.ip

        fresh_n_sem.acquire()

        if ip_info.src not in fresh_nodes:
            fresh_nodes[ip_info.src] = 0

        fresh_nodes[ip_info.src] += int(ip_info.len)

        fresh_n_sem.release()

        bd_sem.acquire()

        node: list[Node] = db.read_by_field('nodes', 'Ip', ip_info.src)

        package_len = Decimal((int(ip_info.len) / 1_000_000))

        if len(node):
            db.update_table_row('nodes', node[0].Id, {
                'Consumption': node[0].Consumption + package_len
            })
        else:
            db.create_table_row('nodes', {
                'Ip': ip_info.src,
                'Consumption': package_len
            })

        bd_sem.release()

        if first:
            mbps_thread = threading.Thread(target=get_mbps)
            mbps_thread.start()
            first = False

    except AttributeError:
        pass


def scan_network(ip):
    print("Scanning network...")
    global db
    global bd_sem

    ips = []

    tokens = ip.split(".")

    command = f"nmap -sn {tokens[0]}.{tokens[1]}.{tokens[2]}.0/24"
    command += " | awk '/Nmap scan report for/{print $NF}'"
    command += " | awk '{gsub(/[()]/,\"\")}1' > output"

    os.system(command)

    threading.Timer(120, scan_network).start()

    with open('output', 'r') as file:
        ips = file.readlines()

    bd_sem.acquire()

    ips = db.update_hosts(ips)

    for ip in ips:
        db.create_table_row(
            'nodes',
            {
                'Ip': ip,
                'Consumption': 0,
                'Active': True
            }
        )

    bd_sem.release()


def main():
    # scan_network('192.168.100.43')

    capture = pyshark.LiveCapture(interface='Wi-Fi')

    thread_capture = threading.Thread(
        target=capture.apply_on_packets,
        args=(print_callback,)
    )

    thread_capture.start()


if __name__ == '__main__':
    main()
