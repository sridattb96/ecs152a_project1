
a = 0

def secondfunc(b):
	b += 3
	print "b: " + str(b)
	return b

def firstfunc():
	print secondfunc(a)

firstfunc()