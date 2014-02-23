import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import time
import numpy as np
import math

hist_size = 20 # histogram

def mega_input(variable_name):
	print "Please enter {}: ".format(variable_name)
	var = raw_input()
	try:
			var = float(var)
	except ValueError:
			print "Nice attempt =) But your number is incorrect"
			var = default_value(variable_name)
			print "New value of {} will be {}".format(variable_name, var)
	if (((var > 1e8)or(var < 0))and(variable_name != "n")):
		var = default_value(variable_name)
		print "Nice attempt =) But your number is too big or too small"
		print "New value of {} will be {}".format(variable_name, var)
	if (((var > 1e7)or(var < 0))and(variable_name == "n")):
		var = default_value(variable_name)
		print "Nice attempt =) But your number is too big or too small"
		print "New value of {} will be {}".format(variable_name, var)
	return var

def default_value(variable_name):
	if (variable_name == "a"):
		var = 17094
	if (variable_name == "m"):
		var = 62345234
	if (variable_name == "r0"):
		var = 27644437
	if (variable_name == "n"):
		var = 100000
	return var

# def default_value(variable_name):
# 	if (variable_name == "a"):
# 		var = 17094
# 	if (variable_name == "m"):
# 		var = 22597
# 	if (variable_name == "r0"):
# 		var = 7436
# 	if (variable_name == "n"):
# 		var = 30000
# 	return var

n = int(mega_input("n"))
a = mega_input("a")
m = mega_input("m")
r0 = mega_input("r0")

if (m <= a):
	m = 10000
	print "Nice attempt =) But m < a. Now m = {}".format(m)
	time.sleep(1)

if (n < 1e3):
	if (r0 > 2**n):
		r0 = (2**n)-1
		print "Nice attempt =) But r0 > 2^n. Now r0 = {}".format(r0)
	

numbers = []
numbers.append(r0)

def lemer(n):
	rn = float(a*n % m)
	return rn

def norm_array(mas):
	array = []
	for i in mas:
		array.append(i/float(m))
	return array

i = 1

while (i<=n):
	num = lemer(numbers[i-1])
	numbers.append(num)
	i += 1

del numbers[0]
numbers_before_norm = numbers
numbers = norm_array(numbers)


def mx():
	return sum(numbers)/n
def dx(mx):
	dx = 0
	for i in numbers:
		dx += (i - mx)**2
	dx = dx/(n-1)
	return dx

mx = mx()
dx = dx(mx)

def ravnomern():
	i = 0
	num = 0
	while(i<n-1):
		n1 = numbers[i]
		n2 = numbers[i+1]

		if ((n1**2 + n2**2)<1):
			num += 1

		i += 2
	return num

ravn = ravnomern()

print "Mx = {}".format(mx)
print "Dx = {}".format(dx)
print "Gx = {}".format(math.sqrt(dx))
print "K = {}".format(ravn)
print "2K/n = {}, ideal = {}".format(2*float(ravn)/n, np.pi/4)

# PERIOD

i = 0
xv = lemer(numbers_before_norm[int(n-1)/2])
flag = 0
prev = xv
k = 0
while (1):
	num = lemer(prev)
	prev = num
	i += 1
	if (xv == num): 
		flag += 1
		if (flag == 2):
			period = i - k
			break
		k = i

print "Period = {}".format(period)
if (period > n):
	print "Period > n"

# APERIOD

prev = lemer(r0)
i = 0
while(i<period-1):
	num = lemer(prev)
	prev = num
	i += 1
xp = num

i = 0
prev_1 = lemer(r0)
prev_2 = lemer(xp)

while (1):
	num_1 = lemer(prev_1)
	num_2 = lemer(prev_2)

	prev_1 = num_1
	prev_2 = num_2

	# print "{} {}".format(num_1, num_2)
	# time.sleep(0.1)

	if (num_1 == num_2):
		break

	i += 1

print "Aper = {}".format(period + i)

# HISTOGRAM

plt.hist(numbers, hist_size, facecolor='green', alpha=0.5)
plt.show()