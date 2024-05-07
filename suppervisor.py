import threading
from time import sleep
import pyshark
from pyshark.packet.layers.xml_layer import XmlLayer
from database import DatabaseInterface, Node

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

        db.create_table_row('speeds', {
            'Speed': mbps
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

        node: list[Node] = db.read_by_field('nodes', 'Ip', ip_info.src)

        if len(node):
            db.update_table_row('nodes', node[0].Id, {
                'Consumption': node[0].Consumption + int(ip_info.len)
            })
        else:
            db.create_table_row('nodes', {
                'Ip': ip_info.src,
                'Consumption': int(ip_info.len)
            })

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
