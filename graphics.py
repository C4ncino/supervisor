import time

from database import DatabaseInterface, Node

# -----------------------------------------------------------------------------

db = DatabaseInterface()


def main():

    while True:

        speeds = db.read_all_table('speeds')

        time.sleep(3)


if __name__ == '__main__':
    main()