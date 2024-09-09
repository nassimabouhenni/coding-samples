import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

conf = SparkConf()
sc = SparkContext(conf=conf)

#count words in wiki.txt
words = sc.textFile(sys.argv[1]).flatMap(lambda line:line.split(" "))
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a+b)
wordCounts.coalesce(1, shuffle=True).saveAsTextFile(sys.argv[2])

#count bigrams in wiki.txt
bigram = sc.textFile(sys.argv[1]).map(lambda line:line.split(" "))\
.flatMap(lambda xs: (tuple(x) for x in zip(xs, xs[1:])))\
.map(lambda bigram: (bigram, 1))\
.reduceByKey(lambda a,b:a+b)

print(wordCounts)
bigram.coalesce(1, shuffle=True).saveAsTextFile(sys.argv[3])

#count bigram conditionals
bigramJoin = bigram.map(lambda a: (a[0][0], a))\
.join(wordCounts)

#bigramProb = bigramJoin.map(lambda a: (a[1][0], a[1]))\
.mapValues(lambda x: x[0][1]/x[1])

bigramProb.coalesce(1, shuffle=True).saveAsTextFile(sys.argv[4])

sc.stop()

