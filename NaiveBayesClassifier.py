I am training the NaiveBayesClassifier in python using sentences, and it gives me the error below. I do not understand what the error might be, and any help would be good. I have tried many other input formats, but the error remains. The code given below:

from text.classifiers import NaiveBayesClassifier from text.blob import TextBlob
train = [('I love this sandwich.', 'pos'),

('This is an amazing place!', 'pos'),
('I feel very good about these beers.', 'pos'),
('This is my best work.', 'pos'),
("What an awesome view", 'pos'),
('I do not like this restaurant', 'neg'),
('I am tired of this stuff.', 'neg'),
("I can't deal with this", 'neg'),
('He is my sworn enemy!', 'neg'),
('My boss is horrible.', 'neg') ] test = [
('The beer was good.', 'pos'),
('I do not enjoy my job', 'neg'),
("I ain't feeling dandy today.", 'neg'),
("I feel amazing!", 'pos'),
('Gary is a friend of mine.', 'pos'),
("I can't believe I'm doing this.", 'neg') ] 
classifier = nltk.NaiveBayesClassifier.train(train)

I am including the traceback below.

Traceback (most recent call last):
  File "C:\Users\5460\Desktop\train01.py", line 15, in <module>
    all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
  File "C:\Users\5460\Desktop\train01.py", line 15, in <genexpr>
    all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
  File "C:\Python27\lib\site-packages\nltk\tokenize\__init__.py", line 87, in word_tokenize
    return _word_tokenize(text)
  File "C:\Python27\lib\site-packages\nltk\tokenize\treebank.py", line 67, in tokenize
    text = re.sub(r'^\"', r'``', text)
  File "C:\Python27\lib\re.py", line 151, in sub
    return _compile(pattern, flags).sub(repl, string, count)
TypeError: expected string or buffer
Any help would be appreciated!Thanks!

#############################################################################################


You need to change your data structure. Here is your train list as it currently stands:

>>> train = [('I love this sandwich.', 'pos'),
('This is an amazing place!', 'pos'),
('I feel very good about these beers.', 'pos'),
('This is my best work.', 'pos'),
("What an awesome view", 'pos'),
('I do not like this restaurant', 'neg'),
('I am tired of this stuff.', 'neg'),
("I can't deal with this", 'neg'),
('He is my sworn enemy!', 'neg'),
('My boss is horrible.', 'neg')]
The problem is, though, that the first element of each tuple needs to be hashable. Strings are not hashable. So I will change your list into a data structure that the classifier can work with:

>>> from nltk.tokenize import word_tokenize # or use some other tokenizer
>>> all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
>>> t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]
Your data should now be structured like this:

>>> t
[({'this': True, 'love': True, 'deal': False, 'tired': False, 'feel': False, 'is': False, 'am': False, 'an': False, 'sandwich': True, 'ca': False, 'best': False, '!': False, 'what': False, '.': True, 'amazing': False, 'horrible': False, 'sworn': False, 'awesome': False, 'do': False, 'good': False, 'very': False, 'boss': False, 'beers': False, 'not': False, 'with': False, 'he': False, 'enemy': False, 'about': False, 'like': False, 'restaurant': False, 'these': False, 'of': False, 'work': False, "n't": False, 'i': False, 'stuff': False, 'place': False, 'my': False, 'view': False}, 'pos'), . . .]
Note that the first element of each tuple is now a dictionary, which is hashable. Now that your data is in place and the first element of each tuple is hashable, you can train the classifier like so:

>>> import nltk
>>> classifier = nltk.NaiveBayesClassifier.train(t)
>>> classifier.show_most_informative_features()
Most Informative Features
                    this = True              neg : pos    =      2.3 : 1.0
                    this = False             pos : neg    =      1.8 : 1.0
                      an = False             neg : pos    =      1.6 : 1.0
                       . = True              pos : neg    =      1.4 : 1.0
                       . = False             neg : pos    =      1.4 : 1.0
                 awesome = False             neg : pos    =      1.2 : 1.0
                      of = False             pos : neg    =      1.2 : 1.0
                    feel = False             neg : pos    =      1.2 : 1.0
                   place = False             neg : pos    =      1.2 : 1.0
                horrible = False             pos : neg    =      1.2 : 1.0
If you want to use the classifier, you can do it like this. First, you begin with a test sentence:

>>> test_sentence = "This is the best band I've ever heard!"
Then, you tokenize the sentence and figure out which words the sentence shares with all_words. These constitute the sentence's features.

>>> test_sent_features = {word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_words}
Your features will now look like this:

>>> test_sent_features
{'love': False, 'deal': False, 'tired': False, 'feel': False, 'is': True, 'am': False, 'an': False, 'sandwich': False, 'ca': False, 'best': True, '!': True, 'what': False, 'i': True, '.': False, 'amazing': False, 'horrible': False, 'sworn': False, 'awesome': False, 'do': False, 'good': False, 'very': False, 'boss': False, 'beers': False, 'not': False, 'with': False, 'he': False, 'enemy': False, 'about': False, 'like': False, 'restaurant': False, 'this': True, 'of': False, 'work': False, "n't": False, 'these': False, 'stuff': False, 'place': False, 'my': False, 'view': False}
Then you simply classify those features:

>>> classifier.classify(test_sent_features)
'pos' # note 'best' == True in the sentence features above


#############################################################################################

@275365's tutorial on the data structure for NLTK's bayesian classifier is great. From a more high level, we can look at it as,

We have inputs sentences with sentiment tags:

training_data = [('I love this sandwich.', 'pos'),
('This is an amazing place!', 'pos'),
('I feel very good about these beers.', 'pos'),
('This is my best work.', 'pos'),
("What an awesome view", 'pos'),
('I do not like this restaurant', 'neg'),
('I am tired of this stuff.', 'neg'),
("I can't deal with this", 'neg'),
('He is my sworn enemy!', 'neg'),
('My boss is horrible.', 'neg')]
Let's consider our feature sets to be individual words, so we extract a list of all possible words from the training data (let's call it vocabulary) as such:

from nltk.tokenize import word_tokenize
from itertools import chain
vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
Essentially, vocabulary here is the same @275365's all_word

>>> all_words = set(word.lower() for passage in training_data for word in word_tokenize(passage[0]))
>>> vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
>>> print vocabulary == all_words
True
From each data point, (i.e. each sentence and the pos/neg tag), we want to say whether a feature (i.e. a word from the vocabulary) exist or not.

>>> sentence = word_tokenize('I love this sandwich.'.lower())
>>> print {i:True for i in vocabulary if i in sentence}
{'this': True, 'i': True, 'sandwich': True, 'love': True, '.': True}
But we also want to tell the classifier which word don't exist in the sentence but in the vocabulary, so for each data point, we list out all possible words in the vocabulary and say whether a word exist or not:

>>> sentence = word_tokenize('I love this sandwich.'.lower())
>>> x =  {i:True for i in vocabulary if i in sentence}
>>> y =  {i:False for i in vocabulary if i not in sentence}
>>> x.update(y)
>>> print x
{'love': True, 'deal': False, 'tired': False, 'feel': False, 'is': False, 'am': False, 'an': False, 'good': False, 'best': False, '!': False, 'these': False, 'what': False, '.': True, 'amazing': False, 'horrible': False, 'sworn': False, 'ca': False, 'do': False, 'sandwich': True, 'very': False, 'boss': False, 'beers': False, 'not': False, 'with': False, 'he': False, 'enemy': False, 'about': False, 'like': False, 'restaurant': False, 'this': True, 'of': False, 'work': False, "n't": False, 'i': True, 'stuff': False, 'place': False, 'my': False, 'awesome': False, 'view': False}
But since this loops through the vocabulary twice, it's more efficient to do this:

>>> sentence = word_tokenize('I love this sandwich.'.lower())
>>> x = {i:(i in sentence) for i in vocabulary}
{'love': True, 'deal': False, 'tired': False, 'feel': False, 'is': False, 'am': False, 'an': False, 'good': False, 'best': False, '!': False, 'these': False, 'what': False, '.': True, 'amazing': False, 'horrible': False, 'sworn': False, 'ca': False, 'do': False, 'sandwich': True, 'very': False, 'boss': False, 'beers': False, 'not': False, 'with': False, 'he': False, 'enemy': False, 'about': False, 'like': False, 'restaurant': False, 'this': True, 'of': False, 'work': False, "n't": False, 'i': True, 'stuff': False, 'place': False, 'my': False, 'awesome': False, 'view': False}
So for each sentence, we want to tell the classifier for each sentence which word exist and which word doesn't and also give it the pos/neg tag. We can call that a feature_set, it's a tuple made up of a x (as shown above) and its tag.

>>> feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
[({'this': True, 'love': True, 'deal': False, 'tired': False, 'feel': False, 'is': False, 'am': False, 'an': False, 'sandwich': True, 'ca': False, 'best': False, '!': False, 'what': False, '.': True, 'amazing': False, 'horrible': False, 'sworn': False, 'awesome': False, 'do': False, 'good': False, 'very': False, 'boss': False, 'beers': False, 'not': False, 'with': False, 'he': False, 'enemy': False, 'about': False, 'like': False, 'restaurant': False, 'these': False, 'of': False, 'work': False, "n't": False, 'i': False, 'stuff': False, 'place': False, 'my': False, 'view': False}, 'pos'), ...]
Then we feed these features and tags in the feature_set into the classifier to train it:

from nltk import NaiveBayesClassifier as nbc
classifier = nbc.train(feature_set)
Now you have a trained classifier and when you want to tag a new sentence, you have to "featurize" the new sentence to see which of the word in the new sentence are in the vocabulary that the classifier was trained on:

>>> test_sentence = "This is the best band I've ever heard! foobar"
>>> featurized_test_sentence = {i:(i in word_tokenize(test_sentence.lower())) for i in vocabulary}
NOTE: As you can see from the step above, the naive bayes classifier cannot handle out of vocabulary words since the foobar token disappears after you featurize it.

Then you feed the featurized test sentence into the classifier and ask it to classify:

>>> classifier.classify(featurized_test_sentence)
'pos'
Hopefully this gives a clearer picture of how to feed data in to NLTK's naive bayes classifier for sentimental analysis. Here's the full code without the comments and the walkthrough:

from nltk import NaiveBayesClassifier as nbc
from nltk.tokenize import word_tokenize
from itertools import chain

training_data = [('I love this sandwich.', 'pos'),
('This is an amazing place!', 'pos'),
('I feel very good about these beers.', 'pos'),
('This is my best work.', 'pos'),
("What an awesome view", 'pos'),
('I do not like this restaurant', 'neg'),
('I am tired of this stuff.', 'neg'),
("I can't deal with this", 'neg'),
('He is my sworn enemy!', 'neg'),
('My boss is horrible.', 'neg')]

vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))

feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]

classifier = nbc.train(feature_set)

test_sentence = "This is the best band I've ever heard!"
featurized_test_sentence =  {i:(i in word_tokenize(test_sentence.lower())) for i in vocabulary}

print "test_sent:",test_sentence
print "tag:",classifier.classify(featurized_test_sentence)

########################



