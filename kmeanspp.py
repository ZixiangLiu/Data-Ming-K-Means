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

# print("Press Enter to select default.")
# num_cluster = input("Please enter K(default {}):".format(num_cluster_default)) or num_cluster_default
# wordstart = input("Please enter word start index(default {}):".format(wordstart_default)) or wordstart_default
# wordend = input("Please enter word end index(default {}):".format(wordend_default)) or wordend_default
# filename = input("\nDefault file output.txt\nPress Enter to select default file.\nEnter the file name: ") or "output.txt"

def get_file_words(filename, cal_range = False, wordstart = 0, wordend = 100):
	'''
	get words into list from file

	Args:
		filename (string): name of the file from which we get words
		cal_range (boolean): True to get words from a start and an end, False to get all words
		wordstart (int): the index of word where we start reading
		wordend (int): the index of word where we end reading
	Return:
		wordlist (list of string): the words
		bloglist (list of list of float): the frequency of words in each blog
	'''
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
				if cal_range:
					for count in linelist[wordstart:wordend]:
						blog.append(float(count))
				else:
					for count in linelist:
						blog.append(float(count))
				bloglist.append(blog)
	return wordlist, bloglist

def blog_dist(blog1, blog2):
	'''
	calculate the distance between two blogs

	Args:
		blog1 (list of floats): each float represents the frequency of that word in the blog
		blog2 (list of floats): same as blog 1, but a different blog, has to be same length as blog1
	Return:	
		distance (float): sum of square of difference of each float
	'''
	if len(blog1) != len(blog2):
		return None;
	distance = 0
	for i in range(0, len(blog1)):
		distance += (blog1[i] - blog2[i])**2
	return distance


def tf(somelist):
	'''
	Term frequency:
	augmented frequency

	Args:
		somelist (list of floats): one list of floats, one blog in this program
	Return:	
		somelist (list of floats): normalized list
	'''
	for onelist in somelist:
		maxf = max(onelist)
		if maxf != 0:
			for i in range(0, len(onelist)):
				onelist[i] = 0.5 + 0.5 * onelist[i] / maxf
		else:
			break;
	return somelist


def tfidfs(somelist):
	'''
	tf–idf
	tf * idf
	Inverse document frequency:
	inverse document frequency smooth
	use tfidfs(tf(somelist)) to work

	Args:	
		somelist (list of floats): one list of floats, one blog in this program
	Return:	
		somelist (list of floats): normalized list using both tf & idf
	'''
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


def normalizer(totallist, debugging = False):
	'''
	normalize data
	(i-u)/std

	Args:	
		totallist (list of list of floats): list of smaller lists, each smaller list is a blog, containning numbers as frequencies
		debugging (boolean): default False, set true to print info while running
	Return: 
		totallist (list of list of floats): nomalized totallist using both tf and idf
	'''
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


def distsumer(pivots, inputlist, clusters):
	'''
	Sum of distance to pivot centers

	Args:
		pivots (list of list of floats): centers of the K-means algorithm
		inputlist (list of list of floats): list of smaller lists, each smaller list is a blog, containning numbers as frequencies
		group (dictionary): key is pivots index, value is list of inputlist indexes in that cluster
	Return: 
		sumofdist (float): summation of sum of distances in each group
	'''
	sumofdist = 0
	for key, value in clusters.items():
		for index in value:
			sumofdist += blog_dist(pivots[key], inputlist[index])
	return sumofdist


def maxdist(inputlist, pivots, dist):
	'''
	find a point with max distance to existing pivots

	Args:
		inputlist (list of list of floats): list of smaller lists, each smaller list is a blog, containning numbers as frequencies
		pivots (list of list of floats): centers of the K-means algorithm
		dist (function with args(list of floats, list of floats)):		function to calculate distance between two blogs
	Return:	
		somelist (list of floats): The list which is furthest to pivots
	'''
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


def centers(inputlist, num_cluster, dist):
	'''
	centers
	find the centers, the key in K-means++

	Args:	
		inputlist (list of list of floats): list of smaller lists, each smaller list is a blog, containning numbers as frequencies
		num_cluster (int): number of clusters
		dist (function with args(list of floats, list of floats)): function to calculate distance between two blogs
	Return:	
		pivots (list of list of floats): the calculated pivots
	'''
	pivots=[]
	pivots.append(inputlist[random.randint(0, num_cluster-1)])
	# if num_cluster >= 3:
	# 	print(num_cluster, "start with", pivots)
	for i in range(0, num_cluster-1):
		pivots.append(maxdist(inputlist, pivots, dist))
	# if num_cluster >= 3:
	# 	print("End with",pivots)
	return pivots


def init_cluster(num_cluster):
	'''
	initialize clusters
	Args:
		num_cluster (int): number of clusters
	Return:	
		clusters (dictionary): an dictionary with values as empty lists
	'''
	clusters = {}
	# initialize values to lists
	for i in range(0, num_cluster):
		clusters[i] = []
	return clusters


def kmeanpp_cal(num_cluster, inputlist, dist, max_iter = 300, debugging = False):
	'''
	calculate the k-means cluster
	Args:
		num_cluster (int): number of clusters
		inputlist (list of list of floats): list of smaller lists, each smaller list is a blog, containning numbers as frequencies
		dist (function with args(list of floats, list of floats)): function to calculate distance between two blogs
		max_iter (int): max times of iteration before abortion, default 300
		debugging (boolean): default False, true to print info while running
	Return:
		group (dicionary): key is pivots index, value is list of inputlist indexes in that cluster
		pivots (list of list of floats): centers of the K-means algorithm
		num_of_iter (int): total number of iteration to get the output
		distsum (float): sum of each blog's distance to its corresponding center of the result
		centert (float): time used in calculating centers
		calt (float): time used in calculating result
	'''
	length = len(inputlist)
	# each pivot is an list
	start = time.time()
	pivots = centers(inputlist, num_cluster, dist)
	centert = time.time()-start
	distsum = 0

	# clusters is a dictionary of clusters, key pivot index, value is a list of input list index
	clusters = init_cluster(num_cluster)

	old_clusters = {}
	num_of_iter = max_iter
	start = time.time()
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
	calt = time.time()-start
	return clusters, pivots, num_of_iter, distsum, centert, calt


def kmean_cal(num_cluster, inputlist, dist, max_iter = 300, debugging = False):
	'''
	calculate the k-means cluster
	similar to perious method, but not using K-means ++

	Args:
		num_cluster (int): number of clusters
		inputlist (list of list of floats): list of smaller lists, each smaller list is a blog, containning numbers as frequencies
		dist (function with args(list of floats, list of floats)): function to calculate distance between two blogs
		max_iter (int): max times of iteration before abortion, default 300
		debugging (boolean): default False, true to print info while running
	Return:
		group (dicionary): key is pivots index, value is list of inputlist indexes in that cluster
		pivots (list of list of floats): centers of the K-means algorithm
		num_of_iter (int): total number of iteration to get the output
		distsum (float): sum of each blog's distance to its corresponding center of the result
		centert (float): time used in calculating centers
		calt (float): time used in calculating result
	'''
	length = len(inputlist)
	# each pivot is an list
	start = time.time()
	pivots = [inputlist[i] for i in random.sample(range(0, length), num_cluster)]
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
	calt = time.time()-start
	return clusters, pivots, num_of_iter, distsum, calt

def write_group(file, groups):
	length = len(groups)
	file.write("K = {}:\n".format(length))
	# for i in range(0, length):
	# 	file.write("{:3d} ".format(i))
	# 	for j in groups[i]:
	# 		file.write("{:3d}".format(j))
	# 	file.write("\n")
	for i in range(0, length):
		file.write("{:3d} {}\n".format(i, groups[i]))
	file.write("\n\n")


def run_kmean(same_k_repeat, klist, write_group_file = True, write_time_file = True):
	'''
	run kmean several times and report result

	Args: 
		same_k_repeat (int): the times of repeat of same k 
		klist (list of int): list of k values that need to calculate
		write_group_file (boolean): true to write group information to a file
		write_time_file (boolean): true to write time information to a file
	Return:
		output (list of outputs of k_means algorithms): best outputs of K_means for each k
		outputpp (list of outputs of k_means++ algorithms): best outputs of K_means++ for each k
		distsumlist (list of min distance result of k_means algorithms): best distance sum of K_means for each k
		distsumlistpp (list of min distance result of k_means++ algorithms): best distance sum of K_means++ for each k
	'''
	output = []
	outputpp = []
	distsumlist = []
	distsumlistpp = []
	kppiter = []
	kiter = []
	centt = []
	calt = []
	kmeant = []
	if write_group_file:
		group_result = open("groups.txt", "w")
	for num_cluster in klist:
		start = time.time()
		outputtemp = []
		outputmin = [0, 0, 0, sys.maxsize]
		outputminpp = [0, 0, 0, sys.maxsize]

		for i in range(0,same_k_repeat): 
			outputtemppp = kmeanpp_cal(num_cluster, bloglist, blog_dist, debugging = False)
			if outputtemppp[3] < outputminpp[3]:
				outputminpp = outputtemppp

			outputtemp = kmean_cal(num_cluster, bloglist, blog_dist, debugging = False)
			if outputtemp[3] < outputmin[3]:
				outputmin = outputtemp
		
		outputpp.append(outputminpp)
		output.append(outputmin)

		if write_time_file:
			centt.append(outputminpp[4])
			calt.append(outputminpp[5])
			kppiter.append(outputminpp[2])
			kmeant.append(outputmin[4])
			kiter.append(outputmin[2])


		if write_group_file:
			group_result.write("K-means ++ ")
			write_group(group_result, outputminpp[0])
			group_result.write("K-means ")
			write_group(group_result, outputmin[0])

		distsumlistpp.append(outputminpp[3])
		distsumlist.append(outputmin[3])

	if write_group_file:
		group_result.close()

	if write_time_file:
		timefile= open("time_word{}_repeat{}_iterate.txt".format(wordend-wordstart, same_k_repeat), "w")
		for i in [j-1 for j in klist]:
			timefile.write("{:10} {:10.5f}\n".format(i, myt[i]))
		for i in range(0, len(centt)):
			timefile.write("{:10.5f} {:10.5f} {:10.5f} {:10.5f} {:10.5f} {:10.5f}\n".format(centt[i], calt[i], centt[i]+calt[i], kmeant[i], kppiter[i], kiter[i]))
		timefile.close()
	return output, outputpp, distsumlist, distsumlistpp


'''
initial parameters
default things
'''
num_cluster_default = 4
wordstart_default = 0
wordend_default = 9500
same_k_repeat = 10
cal_range = False
klist = range(1, len(bloglist)+1)

wordlist, bloglist =  get_file_words("output.txt")
bloglist = tfidfs(tf(bloglist))

temp = run_kmean(same_k_repeat, klist)












