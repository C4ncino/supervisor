from time import sleep
import pyshark
from pyshark.packet.layers.xml_layer import XmlLayer
import threading

from database import DatabaseInterface

# -----------------------------------------------------------------------------

db = DatabaseInterface()
fresh_nodes = {}
first = True

# -----------------------------------------------------------------------------

fresh_n_sem = threading.Semaphore(1)

# -----------------------------------------------------------------------------


def get_mbps():
    global fresh_n_sem
    global db

    while True:
        fresh_n_sem.acquire()

        mbps = 0.0

        for _, val in fresh_nodes.items():
            mbps += val / 1_000_000

        print(f"MBPS: {mbps}")

        db.create_table_row('speed', {
            'speed': mbps
        })

        fresh_nodes.clear()

        fresh_n_sem.release()
        sleep(1)


def print_callback(packet):
    global db
    global fresh_nodes
    global first
    global fresh_n_sem

    try:
        ip_info: XmlLayer = packet.ip

        fresh_n_sem.acquire()

        if ip_info.src not in fresh_nodes:
            fresh_nodes[ip_info.src] = 0

        fresh_nodes[ip_info.src] += int(ip_info.len)

        fresh_n_sem.release()

        # TODO: Change logic to try create a new row in the database
        # TODO: or to update an existing one

        # if ip_info.src not in nodes:
        #     nodes[ip_info.src] = 0

        # nodes[ip_info.src] += int(ip_info.len)

        if first:
            mbps_thread = threading.Thread(target=get_mbps)
            mbps_thread.start()
            first = False

    except AttributeError:
        pass


def main():
    capture = pyshark.LiveCapture(interface='Wi-Fi')

    thread_capture = threading.Thread(
        target=capture.apply_on_packets,
        args=(print_callback,)
    )

    thread_capture.start()


if __name__ == '__main__':
    main()
