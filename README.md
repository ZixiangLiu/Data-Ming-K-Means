# K-means implementation using Python

## modification in this branch (Week April 10)
The getword.py is updated: used nltk to get only English words from nltk.corpus.words. The library has a total of 236736 words. By iterating through common words (dropwords) it reduced to 236594.

The action reduced the output wordlist from 20787 to 9406 words. then updated nltk.stem.wordnet.WordNetLemmatizer to covert every word to its word root form. this further step increased word from 9406 to 9707. Manual check showed the some words originally in the third-person singular or past tense are translated to root form, then recognized by the library
I will use this updated output.txt for further computation. 

I also output iteration times and calculation times in files to find the reason why K-means ++ is slower. Here is the files:



## The below part is from master branch
K-means ++ is implemented in this branch, but it is extremely slow. I compared my K-means running time to sklearn's K-means under same data, my random center K-means used 32 seconds on average, sklearn used 1 second, my K-means ++ used 182 seconds. Covergency condition in my K-means ++ may need update.

The Data is acquired from 31 online blogs. The comtents of the blogs are splited, and only english words in the article is recognized. Upon counting the frequencies of each word in each blog, a matrix of word count is generated. Output.txt is the file that shores such information. 

tf-idf normalization is used to preprocess the data. The implemented K-means algorithm used random centers at the beginning and a K-means++ is also updated. The distance is the sum of square of the difference in two blogs of each word count(normalized). 

Interestingly, the K-means++ algorithm is significantly slower than random center K-means. It is highly possible that because of the small size, the time saved in reduced times of iteration cannot compensate the time used in calculating seed. 

### feedlist.txt
The list of urls from which blogs are get. Some of them does not work.

### dropword.txt
These are the most common words used in English, copied from wiki
These words are dropped from the list to because they are too frequent to be a good indicator which split blogs into different categories.
