# Anirudh Jagdish       (id: 914333546)
# Sridatt Bhamidipati   (id: 998993083)
# ECS 152A project, phase 1
# 02/24/2017

# link processor = Server
# buffer = queue (holds at the most MAX_BUFFER number of elements)
# server transmits in FIFO style

# packet length (and transmission time) varies
# transmission time is negative exponentially distributed with rate mu pkt/sec

from Event import Event
import math
import random

def negative_exponential_dist_time_(rate):
    u = random.random()
    result = (-1 / rate) * math.log(1 - u)
    return result

def step(l, m, max):
    maxBuffer = max
    drop_count = busy = total = length = time = 0
    lam = l
    mu = m
    gel = []
    event_time = time + negative_exponential_dist_time_(lam)
    service_time = negative_exponential_dist_time_(mu)
    first_Event = Event(event_time, service_time, "arrival")
    gel.append(first_Event)
    bufferQ = []
    i = 0
    while i < 10000:
        event = gel.pop(0)
        if event.eType == "arrival":
            time = event.eTime  # step 1
            next_Arr_time = time + negative_exponential_dist_time_(lam)  # step 2
            service_time = negative_exponential_dist_time_(mu)  # step 3
            new_event = Event(next_Arr_time, service_time, "arrival")
            gel.append(new_event)  # step 4
            gel.sort(key = lambda temp: temp.eTime)

            # Process the arrival event
            if length == 0:
                busy = busy + service_time
                length = length + 1
                bufferQ.append(time + service_time)
                depart_event = Event(time + service_time, 0, "departure")
                gel.append(depart_event)
                gel.sort(key = lambda temp: temp.eTime)
            elif maxBuffer == length:
                drop_count = drop_count + 1
                #print "dropped"
            elif length - 1 < maxBuffer:
                length = length + 1
                service_time = negative_exponential_dist_time_(m)
                bufferQ.append(service_time + bufferQ[length - 2])
                busy = busy + service_time
            total = total + length
        # else it's a departure event, so process-service-completion
        else:
            length = length - 1
            bufferQ.pop(0)
            if length > 0:
                gel.append(Event(bufferQ[0], service_time, "departure"))
                gel.sort(key=lambda temp: temp.eTime)
                total = total + length
        i += 1
    # stats finalizing
    util = busy/time
    avg = total/time
    return drop_count, avg, util

def run_simulation():
    test_list = [0.2, 0.4, 0.6, 0.8, 0.9]
    max_list = [1, 20, 50]
    print "\n(For mu = 1 pkt/sec and MAX_BUFFER = 1,20, or 50)"
    print "Lambda   |   Avg. Buffer Length  |        Util.        |   Packets Dropped"
    print "--------------------------------------------------------------------------"
    for curr_buffer in max_list:
        print "                     "'{:<20}'.format("Current Buffer size ="), '{:5}'.format(curr_buffer)
        for temp in test_list:
            d, a, u = step(temp, 1, curr_buffer)
            print '{:5}'.format(temp), "         " '{:<10.4}'.format(a), "         " '{:<11.4}'.format(u), "         " '{:<10}'.format(d)
    test_list = [0.1, 0.25, 0.4, 0.55, 0.65, 0.80, 0.90]
    print "\n\n(For mu = 1 pkt/sec and MAX_BUFFER = 100,000 (to model a very large or infinite buffer))"
    print "Lambda   |   Avg. Buffer Length  |        Util.        |   Packets Dropped"
    print "--------------------------------------------------------------------------"
    for temp in test_list:
        d, a, u = step(temp, 1, 100000)
        print '{:5}'.format(temp), "         " '{:<10.4}'.format(a), "         " '{:<11.4}'.format(u), "         " '{:<10}'.format(d)

phase_one = run_simulation()