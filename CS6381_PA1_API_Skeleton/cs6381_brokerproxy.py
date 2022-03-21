###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: API for the broker proxy at the middleware layer
#
# Created: Spring 2022
#
###############################################

# If you decide to do the RPC approach, you might need a proxy for the
# real broker.
#
# This is the proxy object for the broker which is held by both the
# publisher and subscriber-side middleware to store info about the
# whereabouts of the actual broker. The application level logic does not
# know that it is talking to a proxy object. It will simply invoke methods
# on the proxy, which then get translated under the hood into the appropriate
# serialization logic and sending to the real broker
from cs6381_broker import ViaBroker

import socket

class BrokerProxy:
    pass

    def __init__(self,strategy):
        self.brokers = []
        self.strategy = strategy
        if (self.strategy == "broker") :
            direct_broker = self.getViaBroker()
            self.brokers.append(direct_broker)

    def getViaBroker(self):
        broker = ViaBroker()

        return broker

    ###################################
    #
    # Main program
    #
    ###################################
    def main(self):
      pass

    if __name__ == "__main__":
       main()
