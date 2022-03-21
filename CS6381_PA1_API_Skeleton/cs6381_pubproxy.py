###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: API for the publisher proxy in the middleware layer
#
# Created: Spring 2022
#
###############################################

# A proxy for the publisher will be used in a remote procedure call
# approach.  We envision its use on the broker side when
# it delegates the work to the proxy to talk to its real counterpart. 
# One may completely avoid this approach if pure message passing is
# going to be used and not have a higher level remote procedure call approach.

from cs6381_publisher import DirectPublisher, ViaBrokerPublisher


class PublisherProxy:
    pass

    def __init__(self,strategy):
        self.publishers = []
        self.strategy = strategy
        if(self.strategy=='direct'):
            direct_publisher= self.getDirectPublisher()
            self.publishers.append(direct_publisher)
        else:
            via_broker = self.getViaBroker()
            self.publishers.append(via_broker)

    def getDirectPublisher(self):

        publisher = DirectPublisher()
        return publisher

    def getViaBroker(self):
        publisher = ViaBrokerPublisher()
        return publisher


    ###################################
    #
    # Main program
    #
    ###################################
    def main(self):
        pass


    if __name__ == "__main__":
        main()
