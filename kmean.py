#!/usr/bin/env
# Python 
# Zixiang Liu

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import random
import sys
import time

'''
This program read a output file that each row is a list of number of appearance in one blog
then use k-means to calculate it clusters
'''
num_cluster_default = 4
wordstart_default = 0
wordend_default = 100
same_k_repeat = 10

# print("Press Enter to select default.")
# num_cluster = input("Please enter K(default {}):".format(num_cluster_default)) or num_cluster_default
# wordstart = input("Please enter word start index(default {}):".format(wordstart_default)) or wordstart_default
# wordend = input("Please enter word end index(default {}):".format(wordend_default)) or wordend_default
# filename = input("\nDefault file output.txt\nPress Enter to select default file.\nEnter the file name: ") or "output.txt"

num_cluster = num_cluster_default
wordstart = wordstart_default
wordend = wordend_default
filename = "output.txt"

inputfile = open(filename, "r")
wordlist = []
bloglist = []
with inputfile as filestream:
	first = True
	for line in filestream:
		linelist = line.split();
		if first:
			for word in linelist:
				wordlist.append(word)
			first = False
		else:
			blog = []
			for count in linelist[wordstart:wordend]:
				blog.append(float(count))
			bloglist.append(blog)

print(blog[30])

'''
calculate the distance between two blogs
'''
def blog_dist(blog1, blog2):
	if len(blog1) != len(blog2):
		return None;
	distance = 0
	for i in range(0, len(blog1)):
		distance += (blog1[i] - blog2[i])**2
	return distance


'''
Term frequency:
augmented frequency
'''
def tf(somelist):
	for onelist in somelist:
		maxf = max(onelist)
		if maxf != 0:
			for i in range(0, len(onelist)):
				onelist[i] = 0.5 + 0.5 * onelist[i] / maxf
		else:
			break;
	return somelist


'''
tf–idf
tf * idf
Inverse document frequency:
inverse document frequency smooth
use tfidfs(tf(somelist)) to work
'''
def tfidfs(somelist):
	N = len(somelist)
	somelist = np.array(somelist)
	for i in range(0, len(somelist[0])):
		# start with 1 to make it smooth and none zero
		nt = 1
		for j in range(0, N):
			if somelist[:,i][j] != 0.5:
				nt += 1
		idfs = np.log(N/nt)
		for j in range(0, N):
			somelist[:,i][j] += idfs
	return somelist

'''
normalize data
(i-u)/std
'''
def normalizer(totallist, debugging = False):
	totallength = len(totallist[0])
	if debugging:
		print("start normaling")
	for i in range(0, totallength):
		if debugging:
			print("normalizing column No.{}".format(i))
		listavg = sum(np.array(totallist)[:,i])/float(totallength)
		liststd = np.std(np.array(totallist)[:,i], dtype=np.float64)
		for k in range(0, len(totallist)):
			totallist[k][i] = (totallist[k][i]-listavg)/liststd
	return totallist

'''
Sum of distance to pivot centers
'''
def distsumer(pivots, inputlist, clusters):
	sumofdist = 0
	for key, value in clusters.items():
		for index in value:
			sumofdist += blog_dist(pivots[key], inputlist[index])
	return sumofdist

'''
mindist
find a point with max distance to pivots
'''
def maxdist(inputlist, pivots, dist):
	totalmax = 0
	index = 0
	for i in range(0, len(inputlist)):
		distancemax = 0
		for j in pivots:
			onedist = dist(inputlist[i], j) 
			if onedist > distancemax:
				distancemax = onedist
		if distancemax > totalmax:
			totalmax = distancemax
			index = i
	# print(index)
	return inputlist[index]

'''
centers
'''
def centers(inputlist, num_cluster, dist):
	pivots=[]
	pivots.append(inputlist[random.randint(0, num_cluster-1)])
	# if num_cluster >= 3:
	# 	print(num_cluster, "start with", pivots)
	for i in range(0, num_cluster-1):
		pivots.append(maxdist(inputlist, pivots, dist))
	# if num_cluster >= 3:
	# 	print("End with",pivots)
	return pivots

'''
'''
def init_cluster(num_cluster):
	clusters = {}
	# initialize values to lists
	for i in range(0, num_cluster):
		clusters[i] = []
	return clusters

'''
calculate the k-means cluster
'''
def kmean_cal(num_cluster, inputlist, dist, max_iter = 300, debugging = False):
	length = len(inputlist)
	# each pivot is an list
	pivots = centers(inputlist, num_cluster, dist)
	distsum = 0

	# clusters is a dictionary of clusters, key pivot index, value is a list of input list index
	clusters = init_cluster(num_cluster)

	old_clusters = {}
	num_of_iter = max_iter

	for i in range(0, max_iter):
		# if debugging:
		# 	print("Iteration No.{}".format(i))
		for k in range(0, length):
			min_dist = sys.maxsize
			min_index = 0
			for j in range(0, num_cluster):
				distance = dist(inputlist[k], pivots[j])
				if distance < min_dist:
					min_dist = distance
					min_index = j
			clusters[min_index].append(k)
			# if debugging:
			# 	print("blog No.{} is in cluster No.{}".format(k, min_index))

		# condition of convergence, if new iteration did not change items in cluster
		if clusters == old_clusters:
			num_of_iter = i
			distsum = distsumer(pivots, inputlist, clusters)
			# if debugging:
			# 	print("k=",num_cluster, "iter No.", i, "does not change cluster, end of iteration\n")
			break;

		for k in range(0, num_cluster):
			list_len = len(pivots[0])
			count_matrix = []
			for j in clusters[k]:
				count_matrix.append(inputlist[j])
			# if debugging:
			# 	print("k=",num_cluster, "iter No.", i, "cluster No.", k, "has member", len(count_matrix))
			# unless the cluster is empty
			if clusters[k]:
				pivots[k] = [sum(np.array(count_matrix)[:, j])/float(len(clusters[k])) for j in range(0, list_len)]
			# save the current result in a seperate dictionary
			old_clusters[k] = [j for j in clusters[k]]
			clusters[k] = []

		# if debugging:
		# 	print("End of iteration No.{}\n\n".format(i))
		distsum = distsumer(pivots, inputlist, clusters)
	return clusters, pivots, num_of_iter, distsum

bloglist = tfidfs(tf(bloglist))

for l in range(0, 5):
	start = time.time()
	output = []
	klist = range(1, len(bloglist))
	distsumlist = []
	for num_cluster in klist:
		outputtemp = []
		outputmin = [0, 0, 0, sys.maxsize]
		for i in range(0,same_k_repeat): 
			outputtemp = kmean_cal(num_cluster, bloglist, blog_dist, debugging = False)
			if outputtemp[3] < outputmin[3]:
				outputmin = outputtemp
		distsumlist.append(outputmin[3])
	end = time.time()
	mykmean_time = end-start
	print("My function runs {:.5f}s".format(mykmean_time))

	packageoutput = []
	start = time.time()
	for num_cluster in klist:
		kmeans = KMeans(n_clusters=num_cluster).fit(bloglist)
		packageoutput.append(kmeans.inertia_)
	end = time.time()
	packagekmean_time = end-start
	print("Sklearn function runs {:.5f}s".format(packagekmean_time))

	# outputfile= open("time_word{}_repeat{}.txt".format(wordend-wordstart, same_k_repeat), "a")
	# outputfile.write("{:.5f} {:.5f}\n".format(mykmean_time, packagekmean_time))
	# outputfile.close()

# plt.plot(klist, distsumlist, label="My function")
# plt.plot(klist, packageoutput, label = "Sklearn.KMeans")
# plt.title("repeat {} times for each K".format(same_k_repeat))
# plt.xlabel("k")
# plt.ylabel("sum of distance")
# plt.legend()
# plt.show()
# outputdict, pivots, num_of_iter, sumofdist = output
# for key, value in outputdict.items():
# 	print("Cluster No.{} has blog {}".format(key, value))
# print("Went through {} iterations.".format(num_of_iter))

