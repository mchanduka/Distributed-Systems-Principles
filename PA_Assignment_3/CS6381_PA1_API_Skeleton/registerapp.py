import socket

class RegisterApp():
    publisher = {}
    subscriber = {}
    broker = {}
    __instance = None




    @staticmethod
    def getInstance():
        """ Static access method. """
        if RegisterApp.__instance == None:
            RegisterApp()
        return RegisterApp.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if RegisterApp.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            RegisterApp.__instance = self

    def register(self,topic,url,pipelineType):

        if(pipelineType=='broker'):
            self.broker[topic] = url, pipelineType
        elif (pipelineType=='publisher'):
            self.publisher[topic] = url, pipelineType
        elif(pipelineType=='subscriber'):
            self.subscriber[topic] = url, pipelineType
        else:
           print( "Type not supported")
            # self.[topic] = url, pipelineType
        print("Registering the broker")

    def lookup(self,topic,pipelineType):

        if (pipelineType == 'broker'):
            return self.broker[topic]
        elif (pipelineType == 'publisher'):
            return self.publisher[topic]
        elif (pipelineType == 'subscriber'):
            return self.subscriber[topic]
        else:
            print("Type not supported")




def main():
    registerApp = RegisterApp()
    print(registerApp)
    registerApp = RegisterApp.getInstance()
    print(registerApp)
    registerApp = RegisterApp.getInstance()
    print(registerApp)
    registerApp.register("weather", "tcp://127.0.0.1:8000", "broker")
    registerApp.register("weather","tcp://127.0.0.1:8000","publisher")
    registerApp.register("weather", "tcp://127.0.0.1:8000", "subscriber")
    registerApp.lookup("weather")
    # topic = "weather"
    # host_name = socket.gethostname()
    # host_ip = socket.gethostbyname(host_name)
    # url = "tcp://"+host_ip+":8000"
    # registerApp.register(topic,url)
    # value = registerApp.lookup(topic)
    # print(value)

if __name__ == "__main__":
        main()
