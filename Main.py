# Anirudh Jagdish
# Sridatt Bhamidipati
# ECS 152A project, phase 1
# 02/24/2017

import random
import math

# link processor = Server
# buffer = queue (holds at the most MAX_BUFFER number of elements)
# server transmits in FIFO style

# packet length (and transmission time) varies
# transmission time is negative exponentially distributed with rate mu pkt/sec

class Event(object):
    def __init__(self, eTime, servTime,eType):
        self.eTime = eTime
        self.servTime = servTime
        self.eType = eType

    def print_details(self):
        print ("Event: ", self.eType, "Time: ", self.eTime, ", Service Time: ", self.servTime)



# initialize
gel = []
bufferQ = []
length = 0  # length of number of packets in queue
time = 0    # current time
mu = 1
lam = 0.1   # lam = lambda
MAX_BUFFER = 100000
drop_count = 0


# both inter-arrival time and transmission time use this
def negative_exponential_dist_time_(rate):
    u = random.random()
    result = (-1/rate) * math.log10(1-u)
    return result


# first event set-up
event_time = time + negative_exponential_dist_time_(lam)
service_time = negative_exponential_dist_time_(mu)
event_type = "arrival"
first_Event = Event(event_time, service_time, event_type)

gel.append(first_Event)


i = 0
while i < 100000:
    # get first GEL event
    event = gel.pop(0)
    # if event is arrival-type, then process-time-arrival
    if event.eType == "arrival":
        time = event.eTime      # step 1
        next_arrival_time = time + negative_exponential_dist_time_(lam)    # step 2
        # schedule the next arrival event
        service_time = negative_exponential_dist_time_(lam)                # step 3
        departure_time = service_time + time
        new_event = Event(departure_time, service_time, "arrival")
        gel.append(new_event)   # step 4
        # Process the arrival event
        if length == 0:
            depart_time = time + service_time
            depart_event = Event(depart_time, service_time, "departure")
        elif length > 0:
            if length - 1 < MAX_BUFFER:
                bufferQ.append(new_event)
                length = length + 1
            else:
                drop_count = drop_count + 1
            # NOTE: add the stats update

    # else it's a departure event, so process-service-completion
    elif event.eType == "departure":
        time = event.eTime
        # NOTE: add the stats update
        length = length - 1
        if length > 0:
            ev = bufferQ.pop(0)
            newEv = Event(time, service_time, "departure")
    i += 1


# stats gonna go here lolz

# output the stats
