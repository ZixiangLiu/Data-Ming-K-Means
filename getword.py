#!/usr/bin/env
# Python 
# Zixiang Liu

import feedparser
from nltk.corpus import words
word_list = words.words()
print(len(word_list))
from nltk.stem.wordnet import WordNetLemmatizer
wnl = WordNetLemmatizer()
# import numpy as np
# word_list is the list of all English words

def getwords(str_in, list_in, dropwords):
	'''
	Used to parse a long string of Html and recognize all the words in it
	count the total appearance time of each word and store in dictionary list_in

	Args:
		str_in (string): input string that need to be analyzed, will be splited by space
		list_in (dictionary): store the frequency, key is the word, value is the frequency in that blog
	'''
	record = False # initialize the recording situation
	string = "" # initialize string
	for i in str_in:
		if i=='>': # from > start recording the string
			record = True
		elif i=="<": # stop when met a <
			record = False
			for word in string.split(): # split the current string into words
				addwordtodic(word, list_in, dropwords) # add words to dictionary
			string = "" #reset string to empty

		if record:
			if i.isalpha() or i ==' ' or i == '\'': # only record the letters and space and '
				string += i


def addwordtodic(someword, list_in, dropwords=[]):
	'''
	function used to count the times of appearance of a word in the dictionary

	Args:
		someword:	input word that need to be added
		list_in:	a dictionary, store the frequency, key is the word, value is the frequency in that blog
		dropwords: 	a list of words that user wish to drop from the input
	Return:
		dropwords are added to the function
	'''
	word = someword.lower()
	word = wnl.lemmatize(word)
	if word in list_in.keys(): # if the dictionary has the key, count
		list_in[word]+=1
	else: # if not, add to the dictionary
		if word in word_list:
			list_in[word]=1


'''
read dropwords
'''
dropwords = []
dropwordfile = open("dropword.txt", "r")
with dropwordfile as filestream:
	for line in filestream:
		dropwords.append(line.lower()[:-1])

word_list = [word for word in word_list if not word in dropwords]
# print(len(word_list))

'''
The main functioning part
input a file, read all the urls, open and count their words
output to a txt
'''
all_dictionary = [] # initialize dictionary, a list of dictionaries
urls = [] # list to store urls

# input("\nDefault file feedlist.txt\nPress Enter to select default file.\nEnter the file name: ") or 
filename ="feedlist.txt"
url = open(filename, "r")
num_of_url = 0 # count the total number of urls
with url as filestream:
	for line in filestream:
		num_of_url += 1
		one_dictionary = {} # initialize dictionary for the current url
		d = feedparser.parse(line)
		for i in d['entries']: # get the entries
			if 'content' in i.keys():
				for x in range(0, len(i['content'])): # some blog has multiple contents
					if 'value' in i['content'][x].keys(): # if the content has value, or has an article
						getwords(i['content'][x]['value'], one_dictionary, dropwords)
		if(one_dictionary):
			urls.append(line)
			all_dictionary.append(one_dictionary) # add the current dictionary to the list
url.close()


def combinedictionary(all_dictionary):
	'''
	Combine a list of dictionaries into a large dictionary

	Args:
		all_dictionary:		a list of dictionaries of each blog
	Return:
		large_dictionary:	one dicionaries that has word as the key, and  a list of frequencies of that word in each blog
	'''
	large_dictionary = {}
	length = len(all_dictionary)
	for i in range(0, length): # i indicates the index of the blog
		for singleword, singlecount in all_dictionary[i].items():
			if singleword in large_dictionary.keys(): # if already in the list
				large_dictionary[singleword][i] = singlecount
			else: # if not initalize to a list
				large_dictionary[singleword] = [0]*length
				large_dictionary[singleword][i] = singlecount;
	return large_dictionary

large_dictionary = combinedictionary(all_dictionary)

# 
# Output to a file
# 
outputfile= open("output.txt", "w")

	
def rowWordcolTimes(outputfile, large_dictionary):
	'''
	this function write one word and its frequencies in each blog in rows
	and frequencies of each word in one blog in columns
	a transpose of the previous function
	
	Args:
		outputfile (file): the file to write
	Return:
		large_dictionary (dictionary): key is word, value is list of float
			discribe the frequncy of words in all dictionary
	'''
	for word, time in large_dictionary.items():
		outputfile.write("{:<30}".format(word))
		for i in time:
			outputfile.write("{:>5}".format(i))
		outputfile.write('\n')

	
def rowTimescolWord(outputfile, large_dictionary):
	'''
	this function write one word and its frequencies in each blog in columns
	and frequencies of each word in one blog in rows
	a transpose of the previous function

	Args:
		outputfile (file): the file to write
	Return:
		large_dictionary (dictionary): key is word, value is list of float
			discribe the frequncy of words in all dictionary
	'''
	for word in large_dictionary:
		outputfile.write("{:<30}".format(word))
	outputfile.write('\n')
	count = 0 
	while True:
		try:
			for temp, times in large_dictionary.items():
				outputfile.write("{:<30}".format(times[count]))
			outputfile.write('\n')
			count += 1 
		except IndexError:
			break;

# choose = input("Do you want to output words in rows(enter \'row\'') or columns(enter \'col\''):") or "col"
choose = "col"
while True:
	# choose = input("Do you want to output words in rows(enter \'row\'') or columns(enter \'col\''):") or "col"
	if(choose == "row"):
		rowWordcolTimes(outputfile, large_dictionary)
		break;
	elif(choose == "col"):
		rowTimescolWord(outputfile, large_dictionary)
		break;
	else:
		print("please enter \"row\" or \"col\"")


outputfile.close()
outputfile= open("url.txt", "w")
for i in range(0, len(urls)):
	outputfile.write("{} {}\n".format(i, urls[i]));
outputfile.close()

