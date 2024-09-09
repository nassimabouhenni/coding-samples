#bigram.py

bigram.py is a script that, given a text file input (.txt), outputs (a) the word count of the text file, (b) the bigram count of a text file, and (c) the conditional bigram frequency distribution of a text file. 

#Usage

To run bigram.py, enter in terminal (Linux):
spark-submit path/to/bigram.py path/to/[textfile] path/to/[outputdirectory wordcount] path/to/[outputdirectory bigram count] path/to/[outputdirectory conditional bigram frequency]

Ex: 
spark-submit HW0/bigram.py HW0/wiki.txt HW0/output1 HW0/output2 HW0/output3

In each output directory, an automatically generated .txt file will contain
(key,value) pairs as follows:
(a) (word, wordcount)
(b) (bigram, bigram count)
(c) ((bigram, bigram count), conditional bigram frequency)

#Contributing
Nassima Bouhenni
Class: Data Science in the Wild
Prof. Rajalakshmi Nandakumar
Date: 09/23/20
