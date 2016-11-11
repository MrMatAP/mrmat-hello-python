from pyspark_cassandra import CassandraSparkContext
import re

sc = CassandraSparkContext(appName="tweet-analyze")
sc.setLogLevel('ERROR')
rdd = sc.cassandraTable('tweet', 'tweetcontent')

print "- Content structure"
first = rdd.select('content').first()
print first
print first['content']

print "- Tokenization"
tokenized = rdd.select('content').flatMap(lambda r: re.split('\W', r['content'])).collect()

print "- Word count"
wordCount = sc.parallelize(tokenized)\
    .map(lambda word: (word, 1))\
    .reduceByKey(lambda v1, v2: v1 + v2)\
    .sortBy(lambda v: v[1])\
    .collect()

#
# For some reason, this exits with an error about not being able to save to cassandra. Yet the table does
# get populated. It may be due to us writing a reserved word?

sc.parallelize(wordCount).map(lambda v: {'word': v[0], 'count': v[1]}).saveToCassandra('tweet', 'wordcount')



