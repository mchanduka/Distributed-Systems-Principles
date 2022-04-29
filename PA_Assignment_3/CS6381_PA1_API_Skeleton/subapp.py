###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: Skeleton logic for the subscriber application
#
# Created: Spring 2022
#
###############################################


# The basic logic of the subscriber application will be as follows (see pubapp.py
# for additional details.
#
# (1) The subscriber app decides which all topics it is going to subscriber to.
# (see pubapp.py file for how the publisher gets its interest randomly chosen
# for it.
#
# (2) the application obtains a handle to the broker (which under the
# hood will be a proxy object but the application doesn't know it is a
# proxy).
#
# (3) Register with the broker letting it know all the topics it is interested in
# and any other details needed for the underlying middleware to make the
# communication happen via ZMQ
#
# (4) Obtain a handle to the subscriber object (which maybe a specialized
# object depending on whether it is using the direct dissemination or
# via broker)
#
# (5) Wait for the broker to let us know who our publishers are for the
# topics we are interested in. In the via broker approach, the broker is the
# only publisher for us.
#
#
# (5) Have a receiving loop. See scaffolding code for polling where
# we show how different ZMQ sockets can be polled whenever there is
# an incoming event.
#
#    In each iteration, handle all the events that have been enabled by
#    receiving the data. Get the timestamp and obtain the latency for each
#    received topic from each publisher and store this info possibly in a
#    time series database like InfluxDB
#
# (6) if you have logic that allows this forever loop to terminate, then
# go ahead and clean up everything.

import argparse  # for argument parsing
import socket
from zkclient import ZK_Driver
from cs6381_configurator import Configurator

class subapp():

   def __init__(self):
        args= parseCmdLineArgs()


###################################
#
# Parse command line arguments
#
###################################
def parseCmdLineArgs():
    # instantiate a ArgumentParser object
    parser = argparse.ArgumentParser(description="Subscriber Application")

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
    parser.add_argument("-n", "--zkName", default="", help="ZooKeeper znode name, default /topic")
    parser.add_argument("-t", "--topic", default="", help="ZooKeeper znode value at that node, default 'bar'")
    parser.add_argument("-v", "--zkVal", default="", help="ZooKeeper znode value at that node, default 'bar'")

    return parser.parse_args()


###################################
#
# Main program
#
###################################

def main(args):
    print("Main: parse command line arguments")
    args = parseCmdLineArgs()

    zk = None  # session handle to the zookeeper server
    zk = ZK_Driver(args)
    zk.init_driver()
    # zk.run_driver()
    host = zk.get_znode_value()
    host = host.decode()
    # var = host.split(":")
    # get hold of the configurator, which is the factory that produces
    # get hold of the configurator, which is the factory that produces
    # many kinds of artifacts for us
    config = Configurator(args)
    # print(args)


    # Ask the configurator to give us a random subset of topics that we can publish
    # my_topics = config.get_interest()

    my_topics = vars(args)['topic']

    # get a handle to our publisher object
    subscriber = config.get_subscriber()

    topic, url = reqister(my_topics, host)
    # print(url)

    # for topic in my_topics:
    # subscriber[0].registerapp.register(my_topics, url, "subscriber")

    # get a handle to our broker object (will be a proxy)
    # subscriber = config.get_broker()

    # for topic in my_topics:
    #         for sub in subscriber:
    subscriber[0].get_Message(my_topics,url)

def reqister(topic, host_ip):
        # host_name = socket.gethostname()
        # host_ip = socket.gethostbyname(host_name)
        url = "tcp://" + host_ip
        return topic, url

#
# Main entry point
#
###################################
if __name__ == "__main__":
        args = 'broker'
        main(args)
        # main()