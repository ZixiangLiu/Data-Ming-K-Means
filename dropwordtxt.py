'''
python program to take a txt, and output a txt
change the form of words from "A · B · C"
to "A\nB\nC"
'''

defaultfilename = "wikidropwords.txt"
filename = input("\nDefault file {}\nPress Enter to select default file.\nEnter the file name: ".format(defaultfilename)) or defaultfilename

allwords = []
unprocessed = open(filename, "r")
with unprocessed as filestream:
	for line in filestream:
		wordlist = line.split(" · ")
		allwords.extend(wordlist)
unprocessed.close()

outputfile = open("output.txt", "w")
for someword in allwords:
	outputfile.write("{}\n".format(someword))
outputfile.close()