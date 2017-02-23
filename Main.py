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
    def __init__(self, eTime, servTime, eType):
        self.eTime = eTime
        self.servTime = servTime
        self.eType = eType

    def print_details(self):
        print ("Event: ", self.eType, "Time: ", self.eTime, ", Service Time: ", self.servTime)


def everything(lambdaa, muu, maxbuffer):
    maxBuffer = maxbuffer
    lam = lambdaa
    mu = muu

    # initialize
    gel = []
    bufferQ = []
    length = 0  # length of number of packets in queue
    time = 0  # current time
    # mu = 1
    # lam = 0.1   # lam = lambda
    MAX_BUFFER = 100000
    drop_count = 0

    # both inter-arrival time and transmission time use this
    def negative_exponential_dist_time_(rate):
        u = random.random()
        result = (-1 / rate) * math.log10(1 - u)
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
            time = event.eTime  # step 1
            next_arrival_time = time + negative_exponential_dist_time_(lam)  # step 2
            # schedule the next arrival event
            service_time = negative_exponential_dist_time_(mu)  # step 3
            ###### DONT NEED THIS CUZ YOU ADD LATER IN LENGTH == 0
            ###### departure_time = service_time + time
            new_event = Event(next_arrival_time, service_time, "arrival")
            gel.append(new_event)  # step 4
            ###### Gotta sort the gel based on event time
            gel.sort(key=lambda x: x.eTime)

            # Process the arrival event
            if length == 0:
                ### increment of length?
                length = length + 1
                depart_time = time + service_time
                bufferQ.append(depart_time)
                ### since length = 0, service time is then 0

                depart_event = Event(depart_time, 0, "departure")
                ### insert the event into GEL?
                gel.append(depart_event)
                ### again sort the gel
                gel.sort(key=lambda x: x.eTime)

            elif length > 0:
                if length - 1 < MAX_BUFFER:
                    length = length + 1
                    lastdeparturetime = bufferQ[length - 2]
                    bufferQ.append(service_time + lastdeparturetime)
                else:
                    drop_count = drop_count + 1
                    # NOTE: add the stats update

        # else it's a departure event, so process-service-completion
        elif event.eType == "departure":
            time = event.eTime
            # NOTE: add the stats update
            length = length - 1
            bufferQ.pop(0)
            if length > 0:
                ###ev = bufferQ.pop(0)
                ### follow 3.4 steps
                ### create new depart event for a time
                new_dep_time = bufferQ[0]
                new_dep_event = Event(new_dep_time, service_time, "departure")
                ### insert event to gel?
                gel.append(new_dep_event)
                gel.sort(key=lambda x: x.eTime)
                #### WHAT IS THIS: newEv = Event(time, service_time, "departure")
            else:
                ### fix this shit pls
                busy_time = 0
                ### update your busy time here etc, to calculate the busy time
        i += 1


        # stats gonna go here

        # output the stats
