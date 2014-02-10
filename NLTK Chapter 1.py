>>> import nltk

>>> from nltk.book import *
*** Introductory Examples for the NLTK Book ***
Loading text1, ..., text9 and sent1, ..., sent9
Type the name of the text or sentence to view it.
Type: 'texts()' or 'sents()' to list the materials.
text1: Moby Dick by Herman Melville 1851
text2: Sense and Sensibility by Jane Austen 1811
text3: The Book of Genesis
text4: Inaugural Address Corpus
text5: Chat Corpus
text6: Monty Python and the Holy Grail
text7: Wall Street Journal
text8: Personals Corpus
text9: The Man Who Was Thursday by G . K . Chesterton 1908

>>> text1
<Text: Moby Dick by Herman Melville 1851>

>>> text1.concordance("monstrous")
Building index...
Displaying 11 of 11 matches:
ong the former , one was of a most monstrous size . ... This came towards us , 
ON OF THE PSALMS . " Touching that monstrous bulk of the whale or ork we have r
ll over with a heathenish array of monstrous clubs and spears . Some were thick
d as you gazed , and wondered what monstrous cannibal and savage could ever hav
that has survived the flood ; most monstrous and most mountainous ! That Himmal
they might scout at Moby Dick as a monstrous fable , or still worse and more de
th of Radney .'" CHAPTER 55 Of the Monstrous Pictures of Whales . I shall ere l
ing Scenes . In connexion with the monstrous pictures of whales , I am strongly
ere to enter upon those still more monstrous stories of them which are to be fo
ght have been rummaged out of this monstrous cabinet there is no telling . But 
of Whale - Bones ; for Whales of a monstrous size are oftentimes cast up dead u

>>> text2.concordance("monstrous")
Building index...
Displaying 11 of 11 matches:
#. " Now , Palmer , you shall see a monstrous pretty girl ." He immediately went
your sister is to marry him . I am monstrous glad of it , for then I shall have
ou may tell your sister . She is a monstrous lucky girl to get him , upon my ho
k how you will like them . Lucy is monstrous pretty , and so good humoured and 
 Jennings , " I am sure I shall be monstrous glad of Miss Marianne ' s company 
 usual noisy cheerfulness , " I am monstrous glad to see you -- sorry I could n
t however , as it turns out , I am monstrous glad there was never any thing in 
so scornfully ! for they say he is monstrous fond of her , as well he may . I s
possible that she should ." " I am monstrous glad of it . Good gracious ! I hav
thing of the kind . So then he was monstrous happy , and talked on some time ab
e very genteel people . He makes a monstrous deal of money , and they keep thei

>>> text1.similar("monstrous")
Building word-context index...
abundant candid careful christian contemptible curious delightfully
determined doleful domineering exasperate fearless few gamesome
horrible impalpable imperial lamentable lazy loving

>>> text2.similar("monstrous")
Building word-context index...
very exceedingly heartily so a amazingly as extremely good great
remarkably sweet vast
>>> # Observe that we get different results for different texts. Austen uses this word quite differently from Melville; for her, monstrous has positive connotations, and sometimes functions as an intensifier like the word very.
... 

>>> text2.common_contexts(["monstrous", "very"])
a_lucky a_pretty am_glad be_glad is_pretty

>>> text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

>>> text3.generate()
Building ngram index...
In the same is the fashion which thou hadst before I had seen the face
of the hazel and chesnut tree ; and of the first born ; I served thee
fourteen years for Rachel ? wherefore then hast thou broken forth ?
this breach be upon th therefore his name Shel and he rent his clothes
, and bare a son : only obey my voice , and he lifted up mine eyes .
And Joseph made ready his chariot , and called his name Moab : the
same is Hebron in the land of Goshen , and sin
>>> text3.generate()
In the beginning of my bones from hence . So he fled . And he carried
away my reproa And she spake unto the land which thou hast unto
thyself . And the waters from the face of his father ...
>>> len(text1)
260819

>>> sorted(set(text3)) # Get sorted text
['!', "'", '(', ')', ',', ',)', '.', '.)', ':', ';', ';)', '?', '?)', 'A', 'Abel', 'Abelmizraim', 'Abidah', 'Abide', 'Abimael', 'Abimelech', 'Abr', 'Abrah', 'Abraham', 'Abram', 'Accad', 'Achbor', 'Adah', 'Adam', 'Adbeel', 'Admah', 'Adullamite', 'After', 'Aholibamah', 'Ahuzzath', 'Ajah', 'Akan', 'All', 'Allonbachuth', 'Almighty', 'Almodad', 'Also', 'Alvah', 'Alvan', 'Am', 'Amal', 'Amalek', 'Amalekites', 'Ammon', 'Amorite', 'Amorites', 'Amraphel', 'An', 'Anah', 'Anamim', 'And', 'Aner', 'Angel', 'Appoint', 'Aram', 'Aran', 'Ararat', 'Arbah', 'Ard', 'Are', 'Areli', …
>>> len(text3) / len(set(text3)) # Now, let's calculate a measure of the lexical richness of the text. The next example shows us that each word is used 16 times on average (we need to make sure Python uses floating point division)
16.050197203298673

>>> text3.count("smote") # We can count how often a word occurs in a text, and compute what percentage of the text is taken up by a specific word
5

>>> text5.count("lol")
704

>>> text5.count("lol")/len(text5)
0.015640968673628082

>>> def lexical_diversity(text):
...     return len(text) / len(set(text))
... 

>>> def percentage(count, total):
...     return 100 * count / total
... 
>>> lexical_diversity(text3)
16.050197203298673

>>> sent1 = ['Call', 'me', 'Ishmael', '.']
>>> sent1
['Call', 'me', 'Ishmael', '.']

>>> test1 = ['this','is','a','test']
>>> test1
['this', 'is', 'a', 'test']

>>> len(test1)
4

>>> test1.count("this")
1

>>> test1 + sent1
['this', 'is', 'a', 'test', 'Call', 'me', 'Ishmael', '.']

>>> test1[0]
'this'

>>> test1.index("this")
0

>>> test1[0:2]
['this', 'is']

>>> test[:2]
Traceback (most recent call last):
&nbsp; File "<stdin>", line 1, in <module>
NameError: name 'test' is not defined

>>> test1[:2]
['this', 'is']

>>> test1[2:]
['a', 'test']

>>> test1[2]
'a'

>>> test1[2] = "one"
>>> test1
['this', 'is', 'one', 'test']

>>> sorted(test1)
['is', 'one', 'test', 'this']
>>> # Note that sorting is dependent also on case !!!
...&nbsp;

>>> test1 * 2
['this', 'is', 'one', 'test', 'this', 'is', 'one', 'test']

>>> ' '.join(test1)
'this is one test'

>>> (' '.join(test1)).split()
['this', 'is', 'one', 'test']

>>> test1[-1:]
['test']

>>> test1
['this', 'is', 'one', 'test']

>>> test1[:-1]
['this', 'is', 'one']

>>> test2 = test1 * 2

>>> test2
['this', 'is', 'one', 'test', 'this', 'is', 'one', 'test']

>>> set(test2) # Tokenize
set(['this', 'test', 'is', 'one'])

>>> # Frequency Distribution
...&nbsp;
>>> FreqDist(test2)
<FreqDist with 4 samples and 8 outcomes>
>>> fdist2 = FreqDist(test2)
>>> fdist2.keys()
['is', 'one', 'test', 'this']

>>> fdist2['this']
2
>>> test2
['this', 'is', 'one', 'test', 'this', 'is', 'one', 'test']
>>> fdist2.plot(4, cumulative=True)
>>> fdist2.plot(4, cumulative=False)

>>> V = set(test2)
>>> long_words = [word for word in V if len(word) > 2]
>>> sorted(long_words)
['one', 'test', 'this']
>
>> test2
['this', 'is', 'one', 'test', 'this', 'is', 'one', 'test']

>>> test2.append("this")
>>> test2
['this', 'is', 'one', 'test', 'this', 'is', 'one', 'test', 'this']
>>> # Now, test2 has 3 occurrences of the word "this"
...&nbsp;

>>> long_words = [word for word in set(test2) if len(word) > 2 and FreqDist(test2)[word] > 2]
>>> long_words
['this']

>>> # A collocation is a sequence of words that occur together unusually often. Thus red wine is a collocation, whereas the wine is not. A characteristic of collocations is that they are resistant to substitution with words that have similar senses; for example, maroon wine sounds definitely odd.
...&nbsp;

>>> text4.collocations() # from nltk.book
Building collocations list
United States; fellow citizens; four years; years ago; Federal
Government; General Government; American people; Vice President; Old
World; Almighty God; Fellow citizens; Chief Magistrate; Chief Justice;
God bless; every citizen; Indian tribes; public debt; one another;
foreign nations; political parties

>>> fdist2.keys()
['is', 'one', 'test', 'this']
>>> fdist2.items()
[('is', 2), ('one', 2), ('test', 2), ('this', 2)]

>>> # Example &nbsp;Description
... # fdist = FreqDist(samples) create a frequency distribution containing the given samples
... # fdist.inc(sample) increment the count for this sample
... # fdist['monstrous'] &nbsp; &nbsp; &nbsp; &nbsp;count of the number of times a given sample occurred
... # fdist.freq('monstrous') &nbsp; frequency of a given sample
... # fdist.N() total number of samples
... # fdist.keys() &nbsp; &nbsp; &nbsp;the samples sorted in order of decreasing frequency
... # for sample in fdist: &nbsp; &nbsp; &nbsp;iterate over the samples, in order of decreasing frequency
... # fdist.max() &nbsp; &nbsp; &nbsp; sample with the greatest count
... # fdist.tabulate() &nbsp;tabulate the frequency distribution
... # fdist.plot() &nbsp; &nbsp; &nbsp;graphical plot of the frequency distribution
... # fdist.plot(cumulative=True) &nbsp; &nbsp; &nbsp; cumulative plot of the frequency distribution
... # fdist1 < fdist2 &nbsp; test if samples in fdist1 occur less frequently than in fdist2
...&nbsp;
>>>&nbsp;

>>> # Some Word Comparison Operators
... #&nbsp;
... # Function &nbsp;Meaning
... # s.startswith(t) &nbsp; test if s starts with t
... # s.endswith(t) &nbsp; &nbsp; test if s ends with t
... # t in s &nbsp; &nbsp;test if t is contained inside s
... # s.islower() &nbsp; &nbsp; &nbsp; test if all cased characters in s are lowercase
... # s.isupper() &nbsp; &nbsp; &nbsp; test if all cased characters in s are uppercase
... # s.isalpha() &nbsp; &nbsp; &nbsp; test if all characters in s are alphabetic
... # s.isalnum() &nbsp; &nbsp; &nbsp; test if all characters in s are alphanumeric
... # s.isdigit() &nbsp; &nbsp; &nbsp; test if all characters in s are digits
... # s.istitle() &nbsp; &nbsp; &nbsp; test if s is titlecased (all words in s have have initial capitals)
...&nbsp;

>>> sorted([w for w in set(text1) if w.endswith('ableness')])
['comfortableness', 'honourableness', 'immutableness', 'indispensableness', 'indomitableness', 'intolerableness', 'palpableness', 'reasonableness', 'uncomfortableness']

>>> sorted([term for term in set(text4) if 'gnt' in term])
['Sovereignty', 'sovereignties', 'sovereignty']
>>> sorted([item for item in set(text6) if item.istitle()])
['A', 'Aaaaaaaaah', 'Aaaaaaaah', 'Aaaaaah', 'Aaaah', 'Aaaaugh', 'Aaagh', 'Aaah', 'Aaauggh', 'Aaaugh', 'Aaauugh', 'Aagh', 'Aah', 'Aauuggghhh', 'Aauuugh', 'Aauuuuugh', 'Aauuuves', 'Action', 'Actually', 'African', 'Ages', 'Aggh', 'Agh'

>>> sorted([w for w in set(text7) if '-' in w and 'index' in w])
['Stock-index', 'index-arbitrage', 'index-fund', 'index-options', 'index-related', 'stock-index']
>>> sorted([wd for wd in set(text3) if wd.istitle() and len(wd) > 10])
['Abelmizraim', 'Allonbachuth', 'Beerlahairoi', 'Canaanitish', 'Chedorlaomer', 'Girgashites', 'Hazarmaveth', 'Hazezontamar', 'Ishmeelites', 'Jegarsahadutha', 'Jehovahjireh', 'Kirjatharba', 'Melchizedek', 'Mesopotamia', 'Peradventure', 'Philistines', 'Zaphnathpaaneah']

>>> # [len(w) for w in text1]
... 

>>> # [w.upper() for w in text1]
... 

>>> len(text1)
260819
>>> len(set(text1))
19317
>>> len(set([word.lower() for word in text1]))
17231
>>> len(set([word.lower() for word in text1 if word.isalpha()]))
16948

>>> sent1 = ['Call', 'me', 'Ishmael', '.']
>>> sent1 = ['Call', 'me', 'Ishmael', '.']
>>> for x in sent1:
...     if x.endswith('e'):
...             print x
... 
me

>>> nltk.chat.chatbots()
Which chatbot would you like to talk to?
  1: Eliza (psycho-babble)
  2: Iesha (teen anime junky)
  3: Rude (abusive bot)
  4: Suntsu (Chinese sayings)
  5: Zen (gems of wisdom)

Enter a number in the range 1-5: 1
 Therapist
---------
Talk to the program by typing in plain English, using normal upper-
and lower-case letters and punctuation.  Enter "quit" when done.
========================================================================
Hello.  How are you feeling today?
>good
Please tell me more.
>I am fine
How long have you been  fine?
>100 years
Can you elaborate on that?
>no
 no.
>no
I see.  And what does that tell you?
>don't know
Please tell me more.
>quit
Thank you, that will be $150.  Have a good day!
 
