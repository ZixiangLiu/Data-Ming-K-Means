Readme
Week April 10

the getword.py is updated: used nltk to get only English words from nltk.corpus.words
the library has total of 236736 words
by iterate through common words (dropwords) it reduced to 236594

The action reduced the output wordlist from 20787 to 9406 words
then updated nltk.stem.wordnet.WordNetLemmatizer to covert every word to its word root form
this further step increased word from 9406 to 9707
Manual check showed the some words originally in the third-person singular or past tense are translated to root form, then recognized by the library
Will use this updated output.txt for further computation