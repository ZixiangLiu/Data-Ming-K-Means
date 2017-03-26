#!/usr/bin/env
# Python 
# Zixiang Liu

import numpy as np
import random
import sys

'''
This program read a output file that each row is a list of number of appearance in one blog
then use k-means to calculate it clusters
'''
num_cluster = 4

filename = input("\nDefault file output.txt\nPress Enter to select default file.\nEnter the file name: ") or "output.txt"
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
			for count in linelist:
				blog.append(float(count))
			bloglist.append(blog)

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
normalize data
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
calculate the k-means cluster
'''
def kmean_cal(num_cluster, inputlist, dist, max_iter = 300, debugging = False):
	length = len(inputlist)
	# each pivot is an list
	pivots = [inputlist[i] for i in random.sample(range(len(inputlist)), num_cluster)]

	# group is a dictionary of clusters, key pivot index, value is a list of input list index
	group = {}

	# initialize values to lists
	for i in range(0, num_cluster):
		group[i] = []

	old_group = {}
	num_of_iter = max_iter

	for i in range(0, max_iter):
		if debugging:
			print("Iteration No.{}".format(i))
		for k in range(0, length):
			min_dist = sys.maxsize
			min_index = 0
			for j in range(0, num_cluster):
				distance = dist(inputlist[k], pivots[j])
				if distance < min_dist:
					min_dist = distance
					min_index = j
			group[min_index].append(k)
			if debugging:
				print("blog No.{} is in cluster No.{}".format(k, min_index))

		# condition of convergence, if new iteration did not change items in cluster
		if group == old_group:
			num_of_iter = i
			if debugging:
				print("New iteration did not change cluster, end of iteration\n")
			break;

		old_group = {}

		for k in range(0, num_cluster):
			list_len = len(pivots[0])
			count_matrix = []
			for j in group[k]:
				count_matrix.append(inputlist[j])
			pivots[k] = [sum(np.array(count_matrix)[:, j])/float(len(group[k])) for j in range(0, list_len)]
			# save the current result in a seperate dictionary
			old_group[k] = [j for j in group[k]]
			group[k] = []

		if debugging:
			print("End of iteration No.{}\n\n".format(i))
	return group, num_of_iter

bloglist = normalizer(bloglist)
outputdict, num_of_iter = kmean_cal(num_cluster, bloglist, blog_dist, debugging = False)
for key, value in outputdict.items():
	print("Cluster No.{} has blog {}".format(key, value))


