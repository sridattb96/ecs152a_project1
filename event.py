class Event(object):
    def __init__(self, eTime, servTime, eType):
        self.eTime = eTime
        self.servTime = servTime
        self.eType = eType
        self.print_details()

    def print_details(self):
        print ("Event: ", self.eType, "\tTime: ", self.eTime, "\tService Time: ", self.servTime)
