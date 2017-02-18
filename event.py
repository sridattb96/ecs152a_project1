class Event:

	def __init__(self, event_time, service_time, event_type, arrival_rate, service_rate):
		self.event_time = event_time
		self.service_time = service_time
		self.event_type = event_type
		self.arrival_rate = arrival_rate
		self.service_rate = service_rate