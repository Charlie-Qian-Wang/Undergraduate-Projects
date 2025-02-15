import sys
import numpy as np
import math
import time
from numpy.linalg import inv, norm, det

lamda = int(sys.argv[1])
train = np.loadtxt("zip.train")
count_prior = [0] * 10
train_class = []
train_vector = []
for obj in train:
	count_prior[int(obj[0])] += 1
	train_class.append(int(obj[0]))
	train_vector.append(obj[1:])
train_num = len(train_class)
for k in range(10):
	count_prior[k] = math.log(count_prior[k])
right = 0
result_class = []

for i in range(train_num):
	print "Now is the {}th train vector.".format(i)
	start = time.time()
	K = np.zeros(train_num)
	mu = np.zeros((10, 256))
	muN = np.zeros(10)
	sigma = np.zeros((256, 256))
	sigmaN = 0
	prob = np.zeros(10)
	for j in range(train_num):
		if j == i:
			continue
		d = norm(train_vector[i] - train_vector[j], 2) / lamda
		#K[j] = math.exp(- d**2 / 2) / (math.sqrt(2*math.pi))
		K[j] = math.exp(- d**2 / 2)
		mu[train_class[j]] += K[j] * train_vector[j]
		muN[train_class[j]] += K[j]
	for k in range(10):
		if muN[k] == 0:
			sys.exit("Too small lambda!")
		mu[k] = mu[k] / muN[k]
		sigmaN += muN[k]
	for j in range(train_num):
		if j == i:
			continue
		temp = train_vector[j] - mu[train_class[j]]
		sigma += K[j] * temp[:, None] * temp[None, :]
	sigma = sigma / sigmaN
	print "After {}s get mu and sigma.".format(time.time() - start)
	inv_sigma = inv(sigma)
	for k in range(10):
		temp = train_vector[i] - mu[k]
		temp = - (temp.dot(inv_sigma)).dot(temp) / 2
		#temp = temp - 128 * math.log(2*math.pi) - math.log(det(sigma))/2
		prob[k] = count_prior[k] + temp
	print "After {}s get prob.".format(time.time() - start)
	maxk = np.where(prob == np.max(prob))[0][0]
	result_class.append(maxk)
	if maxk == train_class[i]:
		right += 1
		print "Hit!"
	else:
		print "Miss! Predict {} while the ground truth is {}.".format(maxk, train_class[i])
	end = time.time()
	print "Cost {}s for this train vector.".format(end - start)

accuracy = float(right) / train_num * 100
miss = float(train_num-right) / train_num * 100
print "Total accuracy is {}% while miss rate is {}%.".format(accuracy, miss)
