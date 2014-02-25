import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import time
import numpy as np
import math

hist_size = 20 # histogram

print "Generating random numbers. Lab 1 and 2"
print ""

def mega_input_better(variable_name, default, minvar, maxvar):
	print "Please enter {}: ".format(variable_name)
	var = raw_input()
	try:
			var = float(var)
	except ValueError:
			print "Good attempt!  {} = {}".format(variable_name, default)
			var = default
	if (var < minvar) or (var > maxvar):
		print "Good attempt!  {} = {}".format(variable_name, default)
		var = default
	return var  

n = int(mega_input_better("n", 100000, 0, 1e7))
a = mega_input_better("a", 17094, 0, 1e8)
m = mega_input_better("m", 62345234, 0, 1e8)
r0 = mega_input_better("r0", 27644437, 0, 1e8)

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

	i += 1

	if (num_1 == num_2):
		break

print "Aper = {}".format(period + i)

# HISTOGRAM

# plt.hist(numbers, hist_size, facecolor='green', alpha=0.5)
# plt.show()

def factory(raspr_name):
		if (raspr_name == 1): 
			return ravnomern
		if (raspr_name == 2): 
			return gauss
		if (raspr_name == 3): 
			return expon
		if (raspr_name == 4): 
			return gamma
		if (raspr_name == 5): 
			return triangle
		if (raspr_name == 6): 
			return simpson


def ravnomern(numbers):
		print "Ravnomern raspr"
		a = mega_input_better("a", 1, 0, n-1)
		b = mega_input_better("b", n, 0, n)

		if (b < a):
			temp = a
			a = b
			b = temp

		array = []

		for num in numbers:
			array.append(a+(b-a)*num)

		return array

def gauss(numbers):
	print "Gauss raspr"
	mx = mega_input_better("mx", 0.5, 0, 1)
	gx = mega_input_better("gx", 0.1, 0, 1)

	array = []
	i = 0
	for num in numbers:
		array.append(mx+gx*math.sqrt(2)*(gauss_sum(i, numbers) - 6))
		i += 1

	return array

def gauss_sum(i, numbers):
	sum = 0
	for j in np.arange(i, i+6):
		if j < n:
			sum += numbers[j]
	return sum

def expon(numbers):
	print "Expon raspr"
	lambd = mega_input_better("lambda", 0.1, -1, 1)

	array = []
	for num in numbers:
		array.append((-1/lambd)*np.log(num))

	return array

def gamma(numbers):
	print "Gamma raspr"
	nu = mega_input_better("nu", 3, 2, 50)
	lambd = mega_input_better("lambda", 0.1, 0, 1e6)
	nu = int(nu)

	array = []
	i = 0
	for num in numbers:
		array.append((-1/lambd)*np.log(gamma_mul(i, numbers, nu)))
		i += 1

	return array

def gamma_mul(i, numbers, nu):
	mul = 1
	for j in np.arange(i, i+nu):
		if j < n:
			mul *= numbers[j]
	return mul

def triangle(numbers):
	print "Triangle raspr"
	a = mega_input_better("a", 1, 0, n-1)
	b = mega_input_better("b", n, 0, n)

	array = []
	for i in np.arange(0, len(numbers) - 1):
		array.append(a+(b-a)*max(numbers[i], numbers[i+1]))
		i += 2

	return array

def simpson(numbers):
	print "Simpson raspr"
	a = mega_input_better("a", 1, 0, n-1)
	b = mega_input_better("b", n, 0, n)

	array_ravn = []

	for num in numbers:
		array_ravn.append(a/2+(b/2-a/2)*num)

	array = []

	for i in np.arange(0, len(array_ravn) - 1):
		array.append(array_ravn[i] + array_ravn[i+1])
		i += 2

	return array

def norm_array_better(mas):
	array = []
	m1 = max(mas)
	if (m1 < 0):
		m1 = min(mas)
	for i in mas:
		array.append(i/float(m1))
	return array

def mx(array):
	return sum(array)/n
def dx(array, mx):
	dx = 0
	for i in array:
		dx += (i - mx)**2
	dx = dx/(n-1)
	return dx
def gx(dx):
	return math.sqrt(dx)

print ""
print "Choose distribution:"
print "ravnomern - 1"
print "gauss - 2"
print "expon - 3"
print "gamma - 4"
print "triangle - 5"
print "simpson - 6"

dist = raw_input()
default = 6
try:
		dist = int(dist)
except ValueError:
		print "Good attempt!  distribution = {}".format(default)
		dist = default
if (dist < 1) or (dist > 6):
	print "Good attempt!  distribution = {}".format(default)
	dist = default

a = factory(dist)
raspr_array = a(numbers_before_norm)
raspr_array = norm_array_better(raspr_array)

mx = mx(raspr_array)
dx = dx(raspr_array, mx)
gx = gx(dx)

print ""
print "Parameters:"
print "mx = {}".format(mx)
print "dx = {}".format(dx)
print "gx = {}".format(gx)

plt.hist(raspr_array, hist_size, facecolor='green', alpha=0.5)
plt.show()
