###############################################
#
# Author: Aniruddha Gokhale
# Vanderbilt University
#
# Purpose: API for the subscriber proxy in the middleware layer
#
# Created: Spring 2022
#
###############################################

# A proxy for the subscriber will be used in a remote procedure call
# approach.  We envision its use on the broker side when
# it delegates the work to the proxy so the proxy can communicate with
# its real counterpart.  One may completely avoid this approach
# if pure message passing is going to be used and not have a higher level
# remote procedure call approach.
from cs6381_subscriber import DirectSubscriber, ViaBrokerSubscriber


class SubscriberProxy:
    pass

    def __init__(self, strategy):
        self.subscribers = []
        self.strategy = strategy
        if (self.strategy == "direct"):
            direct_subcriber = self.getDirectSubcriber()
            self.subscribers.append(direct_subcriber)
        else:
            viaborker_subcriber = ViaBrokerSubscriber()
            self.subscribers.append(viaborker_subcriber)

    def getDirectSubcriber(self):
        subscriber = DirectSubscriber()
        return subscriber

    def getViaBrokerSubcriber(self):
        subscriber = ViaBrokerSubscriber()
        return subscriber

    def get_Message(self):
        self.getDirectSubcriber().get_Message(self,"garbage")
