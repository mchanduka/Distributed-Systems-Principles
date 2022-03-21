###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: API for the broker functionality in the middleware layer
#
# Created: Spring 2022
#
###############################################

# See the cs6381_publisher.py file for how an abstract Publisher class is
# defined and then two specialized classes. We may need similar things here.
# I am also assuming that discovery and dissemination are lumped into the
# broker. Otherwise keep them in separate files.



from abc import ABC, abstractmethod
from time import time
import socket
import threading

import registerapp
from registerapp import RegisterApp



# define an abstract base class for the publisher
import sys
import zmq
from random import randrange


def __init__(self):
    registerapp = RegisterApp()

class Broker(ABC):
    BROKER_HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    BROKER_PORT = 65432


    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    @abstractmethod
    def start(self):
        pass
    @abstractmethod
    def register (self, topic, identification):
     pass
# a concrete class that disseminates info directly
class ViaBroker(Broker):

    # constructor. Add whatever class members you need
    # for the assignment
    def __init__(self):
        self.registerapp = RegisterApp.getInstance()
        print("ViaBroker constructor called")

    # to be invoked by a broker to kickstart the publisher
    # so it can start publishing.  This method is for Assignment #1
    # where we want all publishers and subscribers deployed
    # before the publishers can start publishing.
    def start(self):
        print("I am the Via Broker start method")

    def register(self, topic, identification,type):
        self.registerapp.register(topic,identification,type)
