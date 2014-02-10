
> TEXTFILE="nltktest.txt"
> if (!file.exists(TEXTFILE)) {
+ download.file("http://www.gutenberg.org/cache/epub/100/pg100.txt", destfile = TEXTFILE)
+ }
trying URL 'http://www.gutenberg.org/cache/epub/100/pg100.txt'
Content type 'text/plain; charset=utf-8' length 5589890 bytes (5.3 Mb)
opened URL
==================================================
downloaded 5.3 Mb
 
> shakespeare = readLines(TEXTFILE)
> shakespeare = shakespeare[-(1:173)]
> shakespeare = shakespeare[-(124195:length(shakespeare))]
> shakespeare = paste(shakespeare, collapse = " ")
> filename = "shakespeare.txt"
> writeLines(shakespeare, filename)
 
import nltk
 
>>> from nltk.corpus import PlaintextCorpusReader
>>> corpus_root='/Users/xbsd/python/complete’
>>> wordlists = PlaintextCorpusReader(corpus_root, 'shakespeare.txt')
>>> wordlists.fileids()
['shakespeare.txt']
>>> n = nltk.word_tokenize(wordlists.raw(fileids="shakespeare.txt"))
 
>>> complete_shakespeare = nltk.Text(n)
>>> complete_shakespeare.concordance("love")
Building index...
Displaying 25 of 1924 matches:
 unused the user so destroys it : No love toward others in that bosom sits Tha
 10 For shame deny that thou bear'st love to any Who for thy self art so unpro
ll hate be fairer lodged than gentle love ? Be as thy presence is gracious and
 
>>> complete_shakespeare.similar("king")
and but that man love duke what good lord the queen time you for so
this i to if world
>>> complete_shakespeare.similar("victory")
time i king maid soul be boy day devil fool he heart here horse house
law life night one people
