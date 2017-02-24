# Anirudh Jagdish       (id: 914333546)
# Sridatt Bhamidipati   (id: 998993083)
# ECS 152A project, phase 1
# 02/24/2017

from Event import Event
import math
import random


def negative_exponential_dist_time_(rate):
    '''
    Used by both inter-arrival time and transmission time
    '''
    u = random.random()
    result = (-1 / rate) * math.log(1 - u)
    return result


def gel_insert(event, gel):
    '''
    Inserts an event into a list and sorts by time
    '''
    gel.append(event)
    gel.sort(key=lambda x: x.eTime)


def init(lam, mu, gel):
    '''
    create first event at time 0
    '''
    event_time = negative_exponential_dist_time_(lam)
    service_time = negative_exponential_dist_time_(mu)
    first_event = Event(event_time, service_time, "arrival")
    gel_insert(first_event, gel)


def step(lam, mu, maxbuff):
    maxBuffer = maxbuff
    drop_count = busy = total = length = time = 0
    gel = []
    bufferQ = []
    length = 0

    init(lam, mu, gel)

    i = 0
    while i < 10000:
        event = gel.pop(0)  # get the first event

        # process an arrival event
        if event.eType == "arrival":

            # Processing arrival
            time = event.eTime  # step 1
            next_Arr_time = time + negative_exponential_dist_time_(lam)  # step 2
            service_time = negative_exponential_dist_time_(mu)  # step 3
            new_event = Event(next_Arr_time, service_time, "arrival")
            gel_insert(new_event, gel)

            # Process the arrival event
            if length == 0:
                busy = busy + service_time
                length = length + 1
                bufferQ.append(time + service_time)
                depart_event = Event(time + service_time, 0, "departure")
                gel_insert(depart_event, gel)

            # the buffer is full
            elif maxBuffer == length:
                drop_count = drop_count + 1  # drop packet

            # there is space in the buffer for another packet
            elif length - 1 < maxBuffer:
                length = length + 1
                service_time = negative_exponential_dist_time_(mu)
                bufferQ.append(service_time + bufferQ[length - 2])
                busy = busy + service_time

            total = total + length

        # process a departure event
        else:
            length = length - 1
            bufferQ.pop(0)

            # if there is something in the buffer
            if length > 0:
                e = Event(bufferQ[0], service_time, "departure")
                gel_insert(e, gel)
                total = total + length

        i += 1

    # get finishing stats
    util = busy / time
    avg = total / time

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
            print '{:5}'.format(temp), "         " '{:<10.4}'.format(a), "         " '{:<11.4}'.format(
                u), "         " '{:<10}'.format(d)

    test_list = [0.1, 0.25, 0.4, 0.55, 0.65, 0.80, 0.90]
    print "\n\n(For mu = 1 pkt/sec and MAX_BUFFER = 100,000 (to model a very large or infinite buffer))"
    print "Lambda   |   Avg. Buffer Length  |        Util.        |   Packets Dropped"
    print "--------------------------------------------------------------------------"

    for temp in test_list:
        d, a, u = step(temp, 1, 100000)
        print '{:5}'.format(temp), "         " '{:<10.4}'.format(a), "         " '{:<11.4}'.format(
            u), "         " '{:<10}'.format(d)


phase_one = run_simulation()