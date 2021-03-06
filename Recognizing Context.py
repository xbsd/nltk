Exploiting Context

By augmenting the feature extraction function, we could modify this part-of-speech tagger to leverage a variety of 
other word-internal features, such as the length of the word, the number of syllables it contains, or its prefix. 
However, as long as the feature extractor just looks at the target word, we have no way to add features that depend 
on the context that the word appears in. But contextual features often provide powerful clues about the correct 
tag — for example, when tagging the word "fly," knowing that the previous word is "a" will allow us to determine that 
it is functioning as a noun, not a verb.

In order to accommodate features that depend on a word's context, we must revise the pattern that we used to define 
our feature extractor. Instead of just passing in the word to be tagged, we will pass in a complete (untagged) 
sentence, along with the index of the target word. This approach is demonstrated in 6.6, which employs a 
context-dependent feature extractor to define a part of speech tag classifier.

 	
def pos_features(sentence, i): [1]
    features = {"suffix(1)": sentence[i][-1:],
                "suffix(2)": sentence[i][-2:],
                "suffix(3)": sentence[i][-3:]}
    if i == 0:
        features["prev-word"] = "<START>"
    else:
        features["prev-word"] = sentence[i-1]
    return features
 	
>>> pos_features(brown.sents()[0], 8)
{'suffix(3)': 'ion', 'prev-word': 'an', 'suffix(2)': 'on', 'suffix(1)': 'n'}

>>> tagged_sents = brown.tagged_sents(categories='news')
>>> featuresets = []
>>> for tagged_sent in tagged_sents:
...     untagged_sent = nltk.tag.untag(tagged_sent)
...     for i, (word, tag) in enumerate(tagged_sent):
...         featuresets.append( (pos_features(untagged_sent, i), tag) )

>>> size = int(len(featuresets) * 0.1)
>>> train_set, test_set = featuresets[size:], featuresets[:size]
>>> classifier = nltk.NaiveBayesClassifier.train(train_set)

>>> nltk.classify.accuracy(classifier, test_set)
0.78915962207856782

Example 6.6 (code_suffix_pos_tag.py): Figure 6.6: A part-of-speech classifier whose feature detector examines the 
context in which a word appears in order to determine which part of speech tag should be assigned. In particular, the 
identity of the previous word is included as a feature.

Its clear that exploiting contextual features improves the performance of our part-of-speech tagger. For example, the 
classifier learns that a word is likely to be a noun if it comes immediately after the word "large" or the word 
"gubernatorial". However, it is unable to learn the generalization that a word is probably a noun if it follows an 
adjective, because it doesn't have access to the previous word's part-of-speech tag. In general, simple classifiers 
always treat each input as independent from all other inputs. In many contexts, this makes perfect sense. For example, 
decisions about whether names tend to be male or female can be made on a case-by-case basis. However, there are often 
cases, such as part-of-speech tagging, where we are interested in solving classification problems that are closely 
related to one another.

Sequence Classification

In order to capture the dependencies between related classification tasks, we can use joint classifier models, which 
choose an appropriate labeling for a collection of related inputs. In the case of part-of-speech tagging, a variety 
of different sequence classifier models can be used to jointly choose part-of-speech tags for all the words in a given 
sentence.

One sequence classification strategy, known as consecutive classification or greedy sequence classification, is to find
the most likely class label for the first input, then to use that answer to help find the best label for the next 
input. The process can then be repeated until all of the inputs have been labeled. This is the approach that was taken 
by the bigram tagger from 5.5, which began by choosing a part-of-speech tag for the first word in the sentence, and 
then chose the tag for each subsequent word based on the word itself and the predicted tag for the previous word.

This strategy is demonstrated in 6.7. First, we must augment our feature extractor function to take a history argument,
which provides a list of the tags that we've predicted for the sentence so far [1]. Each tag in history corresponds 
with a word in sentence. But note that history will only contain tags for words we've already classified, that is, 
words to the left of the target word. Thus, while it is possible to look at some features of words to the right of the 
target word, it is not possible to look at the tags for those words (since we haven't generated them yet).

Having defined a feature extractor, we can proceed to build our sequence classifier [2]. During training, we use the 
annotated tags to provide the appropriate history to the feature extractor, but when tagging new sentences, we generate
the history list based on the output of the tagger itself.

 	
 def pos_features(sentence, i, history): [1]
     features = {"suffix(1)": sentence[i][-1:],
                 "suffix(2)": sentence[i][-2:],
                 "suffix(3)": sentence[i][-3:]}
     if i == 0:
         features["prev-word"] = "<START>"
         features["prev-tag"] = "<START>"
     else:
         features["prev-word"] = sentence[i-1]
         features["prev-tag"] = history[i-1]
     return features

class ConsecutivePosTagger(nltk.TaggerI): [2]

    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = pos_features(untagged_sent, i, history)
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = pos_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)
 	
>>> tagged_sents = brown.tagged_sents(categories='news')
>>> size = int(len(tagged_sents) * 0.1)
>>> train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
>>> tagger = ConsecutivePosTagger(train_sents)
>>> print tagger.evaluate(test_sents)
0.79796012981
Example 6.7 (code_consecutive_pos_tagger.py): Figure 6.7: Part of Speech Tagging with a Consecutive Classifier
Other Methods for Sequence Classification

One shortcoming of this approach is that we commit to every decision that we make. For example, if we decide to label 
a word as a noun, but later find evidence that it should have been a verb, there's no way to go back and fix our 
mistake. One solution to this problem is to adopt a transformational strategy instead. Transformational joint 
classifiers work by creating an initial assignment of labels for the inputs, and then iteratively refining that 
assignment in an attempt to repair inconsistencies between related inputs. The Brill tagger, described in (1), is a 
good example of this strategy.

Another solution is to assign scores to all of the possible sequences of part-of-speech tags, and to choose the 
sequence whose overall score is highest. This is the approach taken by Hidden Markov Models. Hidden Markov Models are 
similar to consecutive classifiers in that they look at both the inputs and the history of predicted tags. However, 
rather than simply finding the single best tag for a given word, they generate a probability distribution over tags. 
These probabilities are then combined to calculate probability scores for tag sequences, and the tag sequence with the 
highest probability is chosen. Unfortunately, the number of possible tag sequences is quite large. Given a tag set 
with 30 tags, there are about 600 trillion (3010) ways to label a 10-word sentence. In order to avoid considering all 
these possible sequences separately, Hidden Markov Models require that the feature extractor only look at the most 
recent tag (or the most recent n tags, where n is fairly small). Given that restriction, it is possible to use dynamic 
programming (4.7) to efficiently find the most likely tag sequence. In particular, for each consecutive word index i, 
a score is computed for each possible current and previous tag. This same basic approach is taken by two more advanced 
models, called Maximum Entropy Markov Models and Linear-Chain Conditional Random Field Models; but different algorithms
are used to find scores for tag sequences.

6.2   Further Examples of Supervised Classification

Sentence Segmentation

Sentence segmentation can be viewed as a classification task for punctuation: whenever we encounter a symbol that 
could possibly end a sentence, such as a period or a question mark, we have to decide whether it terminates the 
preceding sentence.

The first step is to obtain some data that has already been segmented into sentences and convert it into a form that 
is suitable for extracting features:

 	
>>> sents = nltk.corpus.treebank_raw.sents()
>>> tokens = []
>>> boundaries = set()
>>> offset = 0
>>> for sent in nltk.corpus.treebank_raw.sents():
...     tokens.extend(sent)
...     offset += len(sent)
...     boundaries.add(offset-1)
Here, tokens is a merged list of tokens from the individual sentences, and boundaries is a set containing the indexes 
of all sentence-boundary tokens. Next, we need to specify the features of the data that will be used in order to 
decide whether punctuation indicates a sentence-boundary:

 	
>>> def punct_features(tokens, i):
...     return {'next-word-capitalized': tokens[i+1][0].isupper(),
...             'prevword': tokens[i-1].lower(),
...             'punct': tokens[i],
...             'prev-word-is-one-char': len(tokens[i-1]) == 1}

Based on this feature extractor, we can create a list of labeled featuresets by selecting all the punctuation tokens, 
and tagging whether they are boundary tokens or not:

 	
>>> featuresets = [(punct_features(tokens, i), (i in boundaries))
...                for i in range(1, len(tokens)-1)
...                if tokens[i] in '.?!']
Using these featuresets, we can train and evaluate a punctuation classifier:

 	
>>> size = int(len(featuresets) * 0.1)
>>> train_set, test_set = featuresets[size:], featuresets[:size]
>>> classifier = nltk.NaiveBayesClassifier.train(train_set)
>>> nltk.classify.accuracy(classifier, test_set)
0.97419354838709682
To use this classifier to perform sentence segmentation, we simply check each punctuation mark to see whether it's 
labeled as a boundary; and divide the list of words at the boundary marks. The listing in 6.8 shows how this can be 
done.

 	
def segment_sentences(words):
    start = 0
    sents = []
    for i, word in enumerate(words):
        if word in '.?!' and classifier.classify(punct_features(words, i)) == True:
            sents.append(words[start:i+1])
            start = i+1
    if start < len(words):
        sents.append(words[start:])
    return sents
Example 6.8 (code_classification_based_segmenter.py): Figure 6.8: Classification Based Sentence Segmenter
Identifying Dialogue Act Types

When processing dialogue, it can be useful to think of utterances as a type of action performed by the speaker. This 
interpretation is most straightforward for performative statements such as "I forgive you" or "I bet you can't climb 
that hill." But greetings, questions, answers, assertions, and clarifications can all be thought of as types of 
speech-based actions. Recognizing the dialogue acts underlying the utterances in a dialogue can be an important first 
step in understanding the conversation.

The NPS Chat Corpus, which was demonstrated in 2.1, consists of over 10,000 posts from instant messaging sessions.
These posts have all been labeled with one of 15 dialogue act types, such as "Statement," "Emotion," "ynQuestion", 
and "Continuer." We can therefore use this data to build a classifier that can identify the dialogue act types for 
new instant messaging posts. The first step is to extract the basic messaging data. We will call xml_posts() to get 
a data structure representing the XML annotation for each post:

 	
>>> posts = nltk.corpus.nps_chat.xml_posts()[:10000]
Next, we'll define a simple feature extractor that checks what words the post contains:

 	
>>> def dialogue_act_features(post):
...     features = {}
...     for word in nltk.word_tokenize(post):
...         features['contains(%s)' % word.lower()] = True
...     return features
Finally, we construct the training and testing data by applying the feature extractor to each post 
(using post.get('class') to get a post's dialogue act type), and create a new classifier:

 	
>>> featuresets = [(dialogue_act_features(post.text), post.get('class'))
...                for post in posts]
>>> size = int(len(featuresets) * 0.1)
>>> train_set, test_set = featuresets[size:], featuresets[:size]
>>> classifier = nltk.NaiveBayesClassifier.train(train_set)
>>> print nltk.classify.accuracy(classifier, test_set)
0.66
Recognizing Textual Entailment

Recognizing textual entailment (RTE) is the task of determining whether a given piece of text T entails another text 
called the "hypothesis" (as already discussed in 1.5). To date, there have been four RTE Challenges, where shared 
development and test data is made available to competing teams. Here are a couple of examples of text/hypothesis pairs 
from the Challenge 3 development dataset. The label True indicates that the entailment holds, and False, that it fails 
to hold.

Challenge 3, Pair 34 (True)

T: Parviz Davudi was representing Iran at a meeting of the Shanghai Co-operation Organisation (SCO), the fledgling 
association that binds Russia, China and four former Soviet republics of central Asia together to fight terrorism.

H: China is a member of SCO.

Challenge 3, Pair 81 (False)

T: According to NC Articles of Organization, the members of LLC company are H. Nelson Beavers, III, H. Chester Beavers 
and Jennie Beavers Stewart.

H: Jennie Beavers Stewart is a share-holder of Carolina Analytical Laboratory.

It should be emphasized that the relationship between text and hypothesis is not intended to be logical entailment, 
but rather whether a human would conclude that the text provides reasonable evidence for taking the hypothesis to be 
true.

We can treat RTE as a classification task, in which we try to predict the True/False label for each pair. Although it 
seems likely that successful approaches to this task will involve a combination of parsing, semantics and real world 
knowledge, many early attempts at RTE achieved reasonably good results with shallow analysis, based on similarity 
between the text and hypothesis at the word level. In the ideal case, we would expect that if there is an entailment, 
then all the information expressed by the hypothesis should also be present in the text. Conversely, if there is 
information found in the hypothesis that is absent from the text, then there will be no entailment.

In our RTE feature detector (6.9), we let words (i.e., word types) serve as proxies for information, and our features 
count the degree of word overlap, and the degree to which there are words in the hypothesis but not in the text 
(captured by the method hyp_extra()). Not all words are equally important — Named Entity mentions such as the names 
of people, organizations and places are likely to be more significant, which motivates us to extract distinct 
information for words and nes (Named Entities). In addition, some high frequency function words are filtered out as 
"stopwords".

[xx]	give some intro to RTEFeatureExtractor??
 	
def rte_features(rtepair):
    extractor = nltk.RTEFeatureExtractor(rtepair)
    features = {}
    features['word_overlap'] = len(extractor.overlap('word'))
    features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
    features['ne_overlap'] = len(extractor.overlap('ne'))
    features['ne_hyp_extra'] = len(extractor.hyp_extra('ne'))
    return features
Example 6.9 (code_rte_features.py): Figure 6.9: "Recognizing Text Entailment" Feature Extractor. The RTEFeatureExtractor 
class builds a bag of words for both the text and the hypothesis after throwing away some stopwords, then calculates 
overlap and difference.

To illustrate the content of these features, we examine some attributes of the text/hypothesis Pair 34 shown earlier:

 	
>>> rtepair = nltk.corpus.rte.pairs(['rte3_dev.xml'])[33]
>>> extractor = nltk.RTEFeatureExtractor(rtepair)
>>> print extractor.text_words 
set(['Russia', 'Organisation', 'Shanghai', 'Asia', 'four', 'at',
'operation', 'SCO', ...])
>>> print extractor.hyp_words
set(['member', 'SCO', 'China'])
>>> print extractor.overlap('word')
set([])
>>> print extractor.overlap('ne')
set(['SCO', 'China'])
>>> print extractor.hyp_extra('word')
set(['member'])
These features indicate that all important words in the hypothesis are contained in the text, and thus there is some 
evidence for labeling this as True.

The module nltk.classify.rte_classify reaches just over 58% accuracy on the combined RTE test data using methods like 
these. Although this figure is not very impressive, it requires significant effort, and more linguistic processing, 
to achieve much better results.



