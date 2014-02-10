# Conditional Frequency Distributions can be applied to any list with tuples. Examples are shown below.
 
>>> from nltk.corpus import brown
>>> genre_word = [(genre, word)
...     for genre in ['news', 'romance']
...     for word in brown.words(categories=genre)]
>>> type(genre_word)
<type 'list'>
 
>>> genre_word[:10]
[('news', 'The'), ('news', 'Fulton'), ('news', 'County'), ('news', 'Grand'), ('news', 'Jury'), ('news', 'said'), ('news', 'Friday'), ('news', 'an'), ('news', 'investigation'), ('news', 'of')]
 
>>> cfd = nltk.ConditionalFreqDist(genre_word)
 
>>> cfd.conditions()
['news', 'romance']
 
>>> cfd['news']
<FreqDist with 14394 samples and 100554 outcomes>
 
# Works for any list
>>> test = [('cat1', 'a'), ('cat1', 'b'), ('cat2', 'a')]
 
>>> nltk.ConditionalFreqDist(test)
<ConditionalFreqDist with 2 conditions>
>>> # Conditional Frequency Distributions can be applied to any list containing tuples
... 
 
>>> languages = ['Chickasaw', 'English', 'German_Deutsch']
 
>>> from nltk.corpus import udhr
>>> cfd = nltk.ConditionalFreqDist(
...     (lang, len(word)) # Pass the tuples directly to create the ccd
...     for lang in languages
...     for word in udhr.words(lang + '-Latin1'))
 
>>> cfd.tabulate(conditions=['English', 'German_Deutsch'],
... samples=range(10), cumulative=True)
                  0    1    2    3    4    5    6    7    8    9
       English    0  185  525  883  997 1166 1283 1440 1558 1638
German_Deutsch    0  171  263  614  717  894 1013 1110 1213 1275
 
# Creating bi-grams
 
>>> sent = ['In', 'the', 'beginning', 'God', 'created', 'the', 'heaven',
... 'and', 'the', 'earth', '.']
>>> nltk.bigrams(sent)
[('In', 'the'), ('the', 'beginning'), ('beginning', 'God'), ('God', 'created'), ('created', 'the'), ('the', 'heaven'), ('heaven', 'and'), ('and', 'the'), ('the', 'earth'), ('earth', '.')]
>>> 
 
>>> text = nltk.corpus.genesis.words('english-kjv.txt')
>>> bigrams = nltk.bigrams(text)
>>> print cfd['living']
<FreqDist: u'creature': 7, u'thing': 4, u'substance': 2, u',': 1, u'.': 1, u'soul': 1>
