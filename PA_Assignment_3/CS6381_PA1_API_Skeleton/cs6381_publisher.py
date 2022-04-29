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
import datetime
from abc import ABC, abstractmethod

import pandas
import pandas as pd
import time



# define an abstract base class for the publisherimport sys
import zmq
from registerapp import RegisterApp


class Publisher(ABC):

    # BROKER_HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    # BROKER_PORT = 8000  # Port to listen on (non-privileged ports are > 1023)
    # to be invoked by the publisher's application logic
    # to publish a value of a topic.
    @abstractmethod
    def publish(self, topic,port,value):
        pass

    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    @abstractmethod
    def start(self):
        pass


    @abstractmethod
    # "whether you are a publisher or subscriber, topic = <some string>, <some identification of who you are>"
    def register (self,topic,identification):
        pass

# a concrete class that disseminates info directly
class DirectPublisher(Publisher):

    # constructor. Add whatever class members you need
    # for the assignment
    def __init__(self):
        self.registerapp = RegisterApp.getInstance()
        # print("DirectPublisher constructor called")

    # to be invoked by the publisher's application logic
    # to publish a value of a topic.
    def publish(self, topic,port,value):
        print('sending message {}'.format(topic) )
        self.sendMessageToZMQ(topic)
        # print("I am the direct send publisher's publish method")

    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    def   start(self):
        pass
    def register(self, topic, identification):
        pass


    def sendMessageToZMQ(self,message):
        context = zmq.Context()

        # Now create the right kind of socket
        print("Get a REQ socket")
        socket = context.socket(zmq.REQ)

        # now connect to the message passing server
        connect_str = "tcp://" + "localhost" + ":" + "5556"
        # print("Connecting to message passing server at {}".format(connect_str))
        socket.connect(connect_str)

        # Now send 4 messages, two valid, two invalid.
        # For each one, we create a message and send it
        #
        # Say, in our system, only 2 types of messages are allowed: GET and PUT,
        # and there is a strict format where the message type must be in
        # uppercase followed by a single space and then some additional info.
        # Any deviation and the receiving party will not understand it.
        #
        # Note how the sender needs to create a message and ensure that
        # it is constructed in the correct manner. Moreover, if we create a
        # malformed packet, the other side is not going to understand.
        #
        # We demonstrate these cases below.
        #
        while True:
            # print("publishing message")
            arr = getData()
            socket.send_pyobj(arr)
            # socket.send_string(f"Sending message + {message}")

            reply = socket.recv_string()
            print("Received reply = {}".format(reply))



# A concrete class that disseminates info via the broker
class ViaBrokerPublisher(Publisher):

    # constructor. Add whatever class members you need
    # for the assignment
    def __init__(self):
        self.registerapp = RegisterApp.getInstance()
        print("ViaBroker constructor called")


    # to be invoked by the publisher's application logic
    # to publish a value of a topic.
    def publish(self, topic,port,value):

            self.sendMessageViaBrokerToZMQ(topic,port,value)

    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    def start(self): # register
        pass

    def register(self, topic, identification):
     pass
    def sendMessageViaBrokerToZMQ(self,topic,port,value):
        # print("Current libzmq version is %s" % zmq.zmq_version())
        # print("Current  pyzmq version is %s" % zmq.__version__)

         # context = zmq.Context()
        #
        # # The difference here is that this is a publisher and its aim in life is
        # # to just publish some value. The binding is as before.
        # socket = context.socket(zmq.PUB)
        # url = self.registerapp.lookup("weather","publisher")
        # # socket.bind(url[0])
        # # send_zipped_pickle(socket,getData1())
        # socket.bind("tcp://*:5556")
        # # keep publishing
        # while True:
        #      zipcode = randrange(10001,10005)
        #      temperature = randrange(-80, 135)
        #      relhumidity = randrange(10, 60)
        #      print(zipcode)
        #     # socket.send(getData1().tostring())
        #      socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))

        #  Socket to talk to server
        print("Current libzmq version is %s" % zmq.zmq_version())
        print("Current  pyzmq version is %s" % zmq.__version__)

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        # url = self.registerapp.lookup("weather","publisher")
        # socket.bind(url[0])

        # The difference here is that this is a publisher and its aim in life is
        # to just publish some value. The binding is as before.
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:"+port)

        # keep publishing
        while True:
            arr = getData(topic,value)
            socket.send_pyobj(arr)

def getData(topic,value):

    # data set link
       # data parameters
    names = ['zipcode', 'weather', 'humidity', 'airquality', 'light', 'pressure', 'temperature']

    # preparating of dataframe using the data at given link and defined columns list
    dataframe = pandas.read_csv("./weather.csv", names=names)

    array = dataframe.loc[dataframe[topic] == value]
    time.sleep(10)
    # array = dataframe
    # array['send_time'] = pd.to_datetime('now').strftime("%Y-%m-%d %H:%M:%S")
    print(array)
    return (array)


 # if __name__ == "__main__":
# #     # getData()
    #     getData1()

