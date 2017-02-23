# Anirudh Jagdish, Sridatt Bhamidipati
# ECS 152A project, Phase 1
# 02/24/2017

import random
import math
from event import Event

gel = [] # list of arrival and departure events
bufferQ = [] # queue of events that will be processed
length = 0  # length of number of packets in queue
time = 0  # current time
drop_count = 0 # number of dropped packets
MAX_BUFFER = 10

def gel_insert(event):
    '''
    Inserts an event into a list and sorts by time
    '''
    gel.append(event)
    gel.sort(key=lambda x: x.eTime)


def process_arrival(lam, mu, time):
    '''
    Handles process arrival by creating an arrival event and adding to list 
    '''
    global length

    next_arrival_time = time + negative_exponential_dist_time_(lam) 
    service_time = negative_exponential_dist_time_(mu)
    new_event = Event(next_arrival_time, service_time, "arrival")
    gel_insert(new_event)

    if length == 0:
        length += 1
        depart_time = time + service_time
        bufferQ.append(depart_time)
        depart_event = Event(depart_time, 0, "departure") # set service time to 0
        gel_insert(depart_event)
    else:
        if length - 1 < MAX_BUFFER:
            length += 1
            lastdeparturetime = bufferQ[length - 2]
            bufferQ.append(service_time + lastdeparturetime)
        else:
            drop_count += 1
            # NOTE: add the stats update


def service_packet(time):
    global length

    length -= 1
    bufferQ.pop(0)

    if length > 0:
        new_dep_time = bufferQ[0] # create new depart event for a time
        service_time = time + new_dep_time
        new_dep_event = Event(new_dep_time, service_time, "departure")
        gel_insert(new_dep_event)
    else:
        ### fix this shit pls
        busy_time = 0
        ### update your busy time here etc, to calculate the busy time


def negative_exponential_dist_time_(rate):
    '''
    Used by both inter-arrival time and transmission time
    '''
    u = random.random()
    res = (-1 / rate) * math.log10(1 - u)
    return res


def init(lam, mu):
    '''
    create first event at time 0
    '''
    next_arrival_time = negative_exponential_dist_time_(lam) 
    service_time = negative_exponential_dist_time_(mu)
    new_event = Event(next_arrival_time, service_time, "arrival")
    gel_insert(new_event)


def simulation(lam, mu):
    '''
    Simulates a Network Protocol and a Queue/Server system using negative 
    exponential distribution time as arrival and departure times for each
    packet
    '''

    sumQueueLength = 0

    init(lam, mu)

    i = 0
    while i < MAX_BUFFER:
        sumQueueLength += length

        event = gel.pop(0) # get first event
        time = event.eTime

        if event.eType == "arrival": # if event type is arrival
            process_arrival(lam, mu, time)

        elif event.eType == "departure":
            service_packet(time)

        i += 1


    print(drop_count)
    print(sumQueueLength/MAX_BUFFER)


def main():

    simulation(1, 0.1)

main()