###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: Skeleton code for the broker application
#
# Created: Spring 2022
#
###############################################

# Note that here I am lumping the discovery and dissemination into a 
# single capability. You could decide to keep the two separate to make
# the code cleaner and extensible

# The basic logic of the broker application will be as follows
#
# (1) Obtain a handle to the specialized broker object (which
# works only as a lookup service for the Direct dissemination
# strategy or the one that also is involved in dissemination)
#
# (2) Do any initialization steps as needed
#
# (3) Start the broker's event loop so that it keeps running forever
# accepting events and handling them at the middleware layer
#

import argparse  # for argument parsing

import socket
import threading
from cs6381_configurator import Configurator  # factory class
from zkclient import ZK_Driver




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
    parser.add_argument("-d", "--disseminate", choices=["direct", "broker"], default="broker",
                        help="Dissemination strategy: direct or via broker; default is direct")

    parser.add_argument("-a", "--zkIPAddr", default="127.0.0.1", help="ZooKeeper server ip address, default 127.0.0.1")
    parser.add_argument("-p", "--zkPort", type=int, default=2181, help="ZooKeeper server port, default 2181")
    parser.add_argument("-n", "--zkName", default="/broker", help="ZooKeeper znode name, default /broker")
    parser.add_argument("-v", "--zkVal", default="127.0.0.1:6500", help="ZooKeeper znode value at that node, default 'bar'")

    return parser.parse_args()
###################################
#
# Main program
#
###################################


def main():

    # first parse the arguments
    print("Main: parse command line arguments")
    args = parseCmdLineArgs()
    print("Demo program for ZooKeeper")
    # parsed_args = parseCmdLineArgs()

    zkd = ZK_Driver(args)
    zkd.create_znode()

    # initialize the driver
    zkd.init_driver()

    # start the driver
    zkd.run_driver()
    zkd.get_znode_value()


    # get hold of the configurator, which is the factory that produces
    # many kinds of artifacts for us
    config = Configurator(args)

    broker = config.get_broker()
    topic, url = reqister("weather",8000)
    broker[0].registerapp.register(topic,url,"broker")

    # broker.get_Message("weather")

    print('Broker main called')


def reqister(topic,port):
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    url = "tcp://" + host_ip + ":" + str(port)
    return topic, url


# def register():
#     # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     #     s.bind(('127.0.0.1',10000))
#     #     s.listen()
#     #     conn, addr = s.accept()
#     #     with conn:
#     #         print(f"Connected by {addr}")
#     #         while True:
#     #             data = conn.recv(1024)
#     #             print(data)
#     #             # if not data:
#     #             # break
#     #         conn.sendall(data)
#
#     # topic = "weather"
#     host_name = "localhost:2181"
#     # host_ip = socket.gethostbyname(host_name)
#     url = "tcp://" + host_name
#     print("localhost:2181")

if __name__ == "__main__":
      # args = "broker"

      main()




