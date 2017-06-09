# Hierarchical implementation using Python
Used the same data as K-means, but Hierarchical clustering is easier when you do not know how many clusters to form. An optimized algorithm is already included in the python file and the running time is significantly lower than K-means(when K-means calculate K=2 to 32)

The three txt files are respectively outputs of two methods(intuitive one and optimized one, both hierarchical and both give the same result) and a record on time used. 

### feedlist.txt
The list of urls from which blogs are get. Some of them does not work.

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
