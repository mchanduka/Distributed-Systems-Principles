###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: API for the Configurator in our middleware layer 
#
# Created: Spring 2022
#
###############################################

# The goal of the configurator is to maintain all the configuration of the
# experiment in one place and then serve as a factory to produce specialized
# objects that correspond to these supplied parameters.  These configuration
# parameters are expected to be supplied as a command line or in a file
# per experiment. 

# I am assuming there will be all these individual elements that this configurator
# is able to produce when asked by the caller

from cs6381_brokerproxy import BrokerProxy
from cs6381_pubproxy import PublisherProxy
from cs6381_subproxy import SubscriberProxy
from cs6381_topiclist import TopicList
import socket


# define the system configurator class that will be used as a factory object
# to supply the right objects to the caller based on supplied command line
# arguments


class Configurator:


    # constructor
    def __init__(self, args):
        self.tl = TopicList()
        self.disseminate = vars(args)['disseminate']

    # retrieve the right type of publisher depending on the cmd line argument
    def get_publisher(self):
        # check what our role is. If we are the publisher app, we get the concrete
        # publisher object else get a proxy. The publisher itself may be specialized
        # depending on the dissemination strategy
        self.publisher = PublisherProxy(self.disseminate)
        return self.publisher.publishers



# retrieve the right type of subscriber depending on the cmd line argument
    def get_subscriber(self):
        # check what our role is. If we are the subscriber app, we get the concrete
        # subscriber object else a proxy.  The subscriber itself may be specialized
        # depending on the dissemination strategy
        # self.subscriber.subcribers
        self.subscriber = SubscriberProxy(self.disseminate)
        return self.subscriber.subscribers


# retrieve the right type of broker depending on the cmd line argument
    def get_broker(self):
        # check what our role is. If we are the broker, we get the concrete
        # broker object else a proxy. The broker itself may be specialized
        # depending on the dissemination strategy
        # self.broker.brokers
        self.broker = BrokerProxy(self.disseminate)
        return self.broker.brokers


# A publisher and subscriber appln may decide to publish or subscribe to,
# respectively, a random set of topics. We provide such a helper in the
# cs6381_topiclist.py file
    def get_interest(self):
        # as the topic list object to send our interest
        return self.tl.interest()

    def proxy_Start(self):
        for bro in self.get_broker():
            bro.start()
        for pub in self.get_publisher():
            pub.start()
        for sub in self.get_subscriber():
             sub.start()

