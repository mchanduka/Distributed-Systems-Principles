###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: API for the subscriber functionality in the middleware layer
#
# Created: Spring 2022
#
###############################################

# Please see the corresponding hints in the cs6381_publisher.py file
# to see how an abstract class is defined and then two specialized classes
# are defined based on the dissemination approach. Something similar
# may have to be done here. If dissemination is direct, then each subscriber
# will have to connect to each separate publisher with whom we match.
# For the ViaBroker approach, the broker is our only publisher for everything.

###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: API for the middleware layer for the publisher functionality
#
# Created: Spring 2022
#
###############################################

# ABC stands for abstract base class and this is how Python library
# defines the underlying abstract base class
from abc import ABC, abstractmethod
from time import time


# define an abstract base class for the publisher
import sys

import pandas as pd
import zmq
from random import randrange
import pickle
import zlib

from registerapp import RegisterApp


class Subscriber(ABC):

    # to be invoked by the publisher's application logic
    # to publish a value of a topic.
    @abstractmethod
    def get_Message(self, topic, value):
        pass

    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    # whether you are a publisher or subscriber, topic = <some string>, <some identification of who you are>
    def register (self, topic, identification):
        print("Registration called")
        pass

# a concrete class that disseminates info directly
class DirectSubscriber(Subscriber):

    # constructor. Add whatever class members you need
    # for the assignment
    def __init__(self):
        self.registerapp = RegisterApp.getInstance()
        print("DirectSubscriber constructor called")


    # to be invoked by the publisher's application logic
    # to publish a value of a topic.
    def get_Message(self,topic):

            # first parse the arguments
            print("Main: parse command line arguments")
            # args = parseCmdLineArgs()

            print("Current libzmq version is %s" % zmq.zmq_version())
            print("Current  pyzmq version is %s" % zmq.__version__)

            # In ZeroMQ, the first thing we do is get a context
            print("Acquire the context object")
            context = zmq.Context()

            # Get a poller object. Here we use a poller so that it can notify us of
            # an incoming event.
            print("Acquire the poller object")
            poller = zmq.Poller()

            # Now create the right kind of socket
            print("Get a REP socket for the server")
            socket = context.socket(zmq.REP)

            # now bind to the address
            url = self.registerapp.lookup(topic, "subscriber")

            connect_str = "tcp://*:" + "5556"

            print("Binding the message passing server at {}".format(connect_str))
            socket.bind(connect_str)

            # register with the poller
            print("register with the poller for incoming requests")
            poller.register(socket, zmq.POLLIN)

            # Now just wait for events to occur (forever)
            print("Running the event loop")
            while True:
                print("Wait for the next event")
                events = dict(poller.poll())

                # we are here means something showed up.  Make sure that the
                # event is on the registered socket
                if (socket in events):
                    print("Message arrived on our socket; so handling it")
                    handle_message(socket)
                else:
                    print("Message is not on our socket; so ignoring it")

    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    def start(self):
        print("I am the direct send  start method")

    # def get_Message(self, topic):
    #     pass

    def register (self, topic, identification):
        print("Registration called")
        pass
def handle_message(socket):
    # first thing is to receive whatever was received
    message = socket.recv_pyobj()
    message['received_time'] = pd.to_datetime('now').strftime("%Y-%m-%d %H:%M:%S")
    print("handing incoming message: {}".format(message))

    # check if the first characters are
    # if (str.find("GET ") == 0):
    #     print("Received a GET message, responding with what we received")
    #     # Technically, we could have looked up in a database for the received key
    #     # and sent the value but here we don't care. We just want to send something
    #     # back. So we send the same string we got
    #     socket.send_string(str)
    # elif (str.find("PUT ") == 0):
    #     print("Received a PUT message, responding with what we received")
    #     # Technically, we could have looked up in a database for the received key
    #     # and modifed its value or inserted a new record but here we don't care.
    #     # We just want to send something back. So we send the same string we got
    #     socket.send_string(str)
    # else:
    #     print("Unrecognized message type")
    #     socket.send_string("Sorry, unrecognized command")


# A concrete class that disseminates info via the broker
class ViaBrokerSubscriber(Subscriber):

    # constructor. Add whatever class members you need
    # for the assignment
    def __init__(self):
        self.registerapp = RegisterApp.getInstance()

    # to be invoked by the publisher's application logic
    # to publish a value of a topic.

    def get_Message(self, topic, value):
        print("I am the viabroker send sub's method")

    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    def start(self):
        # self.get_Message("message vaibroker")
     pass


    def register(self, topic, identification):
        print("Registration called")
        pass
    def get_Message(self, topic):
        #  Socket to talk to server
        context = zmq.Context()

        # Since we are the subscriber, we use the SUB type of the socket
        socket = context.socket(zmq.SUB)

        # Here we assume publisher runs locally unless we
        # send a command line arg like 10.0.0.1
        srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        # connect_str = "tcp://" + srv_addr + ":5556"
        url = self.registerapp.lookup("weather", "subscriber")
        socket.connect(url[0])

        print("Collecting updates from weather server...")
        # socket.connect(connect_str)
        while True:

            socket.setsockopt_string(zmq.SUBSCRIBE, '')

            # Process 10 updates
            total_temp = 0
            for update_nbr in range(10):
                message = socket.recv_pyobj()
                # records = message.to_records(index=False)
                message['received_time'] = pd.to_datetime('now').strftime("%Y-%m-%d %H:%M:%S")
                for row in message.itertuples():
                    print(row[1:])
