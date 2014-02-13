
>>> from nltk.corpus import names

>>> type(names.words('male.txt'))
<type 'list'>
>>> def gender_features(word):
...     return {'last_letter':word[-1]}
... 

>>> gender_features('Shrek')
{'last_letter': 'k'}
>>> import random
>>> names = ([(name, 'male') for name in names.words('male.txt')] +
...     [(name, 'female') for name in names.words('female.txt')])

 
>>> random.shuffle(names)
>>> names[:10]
[('Everard', 'male'), ('Abbi', 'female'), ('Ariella', 'female'), ('Patin', 'male'), ('Tiebold', 'male'), ('Ted', 'male'), ('Susanne', 'female'), ('Polly', 'female'), ('June', 'female'), ('Lucia', 'female')]

>>> featuresets = [(gender_features(n), g) for (n,g) in names]
>>> featuresets[:10]
[({'last_letter': 'd'}, 'male'), ({'last_letter': 'i'}, 'female'), ({'last_letter': 'a'}, 'female'), ({'last_letter': 'n'}, 'male'), ({'last_letter': 'd'}, 'male'), ({'last_letter': 'd'}, 'male'), ({'last_letter': 'e'}, 'female'), ({'last_letter': 'y'}, 'female'), ({'last_letter': 'e'}, 'female'), ({'last_letter': 'a'}, 'female')]
>>> train_set, test_set = featuresets[500:], featuresets[:500]

>>> classifier = nltk.NaiveBayesClassifier.train(train_set)
>>> type(classifier)

<class 'nltk.classify.naivebayes.NaiveBayesClassifier'>
>>> classifier.classify(gender_features('Raj'))
'male'
>>> classifier.classify(gender_features('Suraiya'))
'female'
>>> print nltk.classify.accuracy(classifier, test_set)
0.748
>>> classifier.show_most_informative_features(5)
Most Informative Features
             last_letter = 'k'              male : female =     44.9 : 1.0
             last_letter = 'a'            female : male   =     37.4 : 1.0
             last_letter = 'p'              male : female =     19.7 : 1.0
             last_letter = 'f'              male : female =     16.6 : 1.0
             last_letter = 'd'              male : female =     10.1 : 1.0

>>> from nltk.classify import apply_features
>>> train_set = apply_features(gender_features, names[500:])
>>> train_set[:10]
[({'last_letter': 'p'}, 'male'), ({'last_letter': 'e'}, 'female'), ...]


>>> # Document Classification
... 
>>> from nltk.corpus import movie_reviews
>>> documents = [(list(movie_reviews.words(fileid)), category)
...     for category in movie_reviews.categories()
...     for fileid in movie_reviews.fileids(category)]

>>> 
>>> random.shuffle(documents)
>>> # Next, we define a feature extractor for documents, so the classifier will know which aspects of the data it 
should pay attention to (6.4). For document topic identification, we can define a feature for each word, indicating 
whether the document contains that word. To limit the number of features that the classifier needs to process, we 
begin by constructing a list of the 2000 most frequent words in the overall corpus [1]. We can then define a feature 
extractor [2] that simply checks whether each of these words is present in a given document.
... 
>>> all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000]
>>> word_features = all_words.keys()[:2000]
>>> 
>>> 
>>> type(all_words)
<class 'nltk.probability.FreqDist'>

>>> def document_features(document):
...     document_words = set(document)
...     features = {}
...     for word in word_features:
...             features['contains(%s)' % word] = (word in document_words)
...     return features
... 
>>> print document_features(movie_reviews.words('pos/cv957_8737.txt')) 
{'contains(waste)': False, 'contains(lot)': False, 'contains(*)': True, 'contains(black)': False, 
'contains(rated)': False, 'contains(potential)': False, 'contains(m)': False, 'contains(understand)': False, 
'contains(drug)': True, 'contains(case)': False, 'contains(created)': False, 'contains(kiss)': False, 'contains(needed)': False, 'co


>>> featuresets = [(document_features(d), c) for (d,c) in documents]
>>> train_set, test_set = featuresets[100:], featuresets[:100]
>>> classifier = nltk.NaiveBayesClassifier.train(train_set)
>>> print nltk.classify.accuracy(classifier, test_set)
0.67
>>> classifier.show_most_informative_features(5)
Most Informative Features
   contains(outstanding) = True              pos : neg    =     10.8 : 1.0
        contains(seagal) = True              neg : pos    =      8.2 : 1.0
         contains(mulan) = True              pos : neg    =      7.7 : 1.0
         contains(damon) = True              pos : neg    =      7.6 : 1.0
   contains(wonderfully) = True              pos : neg    =      7.2 : 1.0


>>> # Parts of Speech Tagging with Decision Trees
... 
>>> from nltk.corpus import brown
>>> suffix_fdist = nltk.FreqDist()
>>> for word in brown.words():
...     word = word.lower()
...     suffix_fdist.inc(word[-1:])
...     suffix_fdist.inc(word[-2:])
...     suffix_fdist.inc(word[-3:])
... 
>>> common_suffixes = suffix_fdist.keys()[:100]
