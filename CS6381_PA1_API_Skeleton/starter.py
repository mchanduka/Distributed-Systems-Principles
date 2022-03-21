import time

import brokerapp
import pubapp
import subapp
import threading
import argparse
import concurrent.futures

def parseCmdLineArgs():
    # instantiate a ArgumentParser object
    parser = argparse.ArgumentParser(description="Publisher Application")

    # Now specify all the optional arguments we support
    # At a minimum, you will need a way to specify the IP and port of the lookup
    # service, the role we are playing, what dissemination approach are we
    # using, what is our endpoint (i.e., port where we are going to bind at the
    # ZMQ level)

    # Here I am showing one example of adding a command line
    # arg for the dissemination strategy. Feel free to modify. Add more
    # options for all the things you need.
    parser.add_argument("-d", "--disseminate", choices=["direct", "broker"], default="direct",
                        help="Dissemination strategy: direct or via broker; default is direct")

    return parser.parse_args()
def main():
    args = parseCmdLineArgs()
    t1 = threading.Thread(target=brokerapp.main, args=[args])
    t1.start()

    t2 = threading.Thread(target=pubapp.main, args=[args])
    t2.start()
    time.sleep(10)
    t3 = threading.Thread(target=subapp.main, args=[args])
    t3.start()
    t3.join()
    t1.join()
    t2.join()



if __name__ == "__main__":
    main()



