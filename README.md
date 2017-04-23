# K-means implementation using Python
I am trying to implement K-means in Python and optimize as much as possible. 

The Data is acquired from 31 online blogs. The comtents of the blogs are splited, and only english words in the article is recognized. Upon counting the frequencies of each word in each blog, a matrix of word count is generated. Output.txt is the file that shores such information. 

tf-idf normalization is used to preprocess the data. The implemented K-means algorithm used random centers at the beginning and a K-means++ is also updated. The distance is the sum of square of the difference in two blogs of each word count(normalized). 

Interestingly, the K-means++ algorithm is significantly slower than random center K-means. It is highly possible that because of the small size, the time saved in reduced times of iteration cannot compensate the time used in calculating seed. 

### dropword.txt
These are the most common words used in English, copied from wiki
These words are dropped from the list to because they are too frequent to be a good indicator which split blogs into different categories.

### Week April 10

The getword.py is updated: used nltk to get only English words from nltk.corpus.words
The library has a total of 236736 words
By iterating through common words (dropwords) it reduced to 236594

The action reduced the output wordlist from 20787 to 9406 words
then updated nltk.stem.wordnet.WordNetLemmatizer to covert every word to its word root form
this further step increased word from 9406 to 9707
Manual check showed the some words originally in the third-person singular or past tense are translated to root form, then recognized by the library
Will use this updated output.txt for further computation
