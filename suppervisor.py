from time import sleep
import pyshark
from pyshark.packet.layers.xml_layer import XmlLayer
import threading

nodes = {}
first = True


def metrics():
    while True:
        for key, val in nodes.items():
            print(f"Host {key}: {val/1000000} MB")

        sleep(1)


def print_callback(packet):
    global nodes
    global first

    try:
        ip_info: XmlLayer = packet.ip

        # print('Source: ', ip_info.src)
        # print('Destination: ', ip_info.dst)
        # print('Length: ', ip_info.len)

        if ip_info.src not in nodes:
            nodes[ip_info.src] = 0

        nodes[ip_info.src] += int(ip_info.len)

        if first:
            theard = threading.Thread(target=metrics)
            theard.start()
            first = False

    except AttributeError:
        pass


def main():
    capture = pyshark.LiveCapture(interface='Wi-Fi')

    thread_capture = threading.Thread(target=capture.apply_on_packets, args=(print_callback,))
    thread_capture.start()


if __name__ == '__main__':
    main()
