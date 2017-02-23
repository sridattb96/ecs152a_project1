class Event(object):
    def __init__(self, eTime, servTime, eType):
        self.eTime = eTime
        self.servTime = servTime
        self.eType = eType

    def print_details(self):
        print ("Event: ", self.eType, "Time: ", self.eTime, ", Service Time: ", self.servTime)
