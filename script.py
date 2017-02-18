
import Queue
import random
from math import *
from event import Event
from packet import Packet

# GLOBAL VARIABLES
MAX_BUFFER_SIZE = 1000 # temporary size
length = 0 # length of queue
curr_time = 0

# GLOBAL LISTS
gel = [] # maintain all events sorted in increasing order of time
dropped_packets = [] 

def gel_insert(e):
	# iterate through gel, insert in proper chronological order
	for i in range(len(gel))
		if gel[i].event_time > e.event_time:
			gel.insert(i-1, e)
			return

	gel.append(e)

def negative_exponenetially_distributed_time(rate):
     u = random.random()
     return (-1/rate) * log(1-u)


def init():
	arrival_rate = 0.1 # lambda
	service_rate = 1 # mu
	event_time = negative_exponenetially_distributed_time(arrival_rate)
	service_time = negative_exponenetially_distributed_time(service_rate)
	e = Event(event_time, service_time, "Arrival", arrival_rate, service_rate)
	gel_insert(e)


def process_arrival(e):
	arrival_rate = 0.1 # lambda
	service_rate = 1 # mu
	curr_time = e.event_time
	# 1) and 2)
	next_arrival_time = curr_time + negative_exponenetially_distributed_time(arrival_rate)
	service_time = negative_exponenetially_distributed_time(service_rate)
	# 3) create new arrival event
	next_event = Event(next_arrival_time, service_time, "Arrival", arrival_rate, service_rate)
	# 4) insert event into event list
	gel_insert(next_event)

	if length == 0:
		# 1)
		departure_time = curr_time + e.service_time
		departure_event = Event(departure_time, "Departure", )


def process_service():
	pass


###### MAIN ##########
init()
queue = Queue.Queue()


for i in range(1000000):
	e = gel.pop(0)
	if e.event_type == "Arrival":
		process_arrival(e)
	else:
		process_service(e)
