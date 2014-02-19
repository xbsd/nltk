# INFORMATION EXTRACTION

7.2   Chunking

The basic technique we will use for entity detection is chunking, which segments and labels multi-token sequences 
as illustrated in 7.2. The smaller boxes show the word-level tokenization and part-of-speech tagging, while the large
boxes show higher-level chunking. Each of these larger boxes is called a chunk. Like tokenization, which omits 
whitespace, chunking usually selects a subset of the tokens. Also like tokenization, the pieces produced by a chunker
do not overlap in the source text.


In this section, we will explore chunking in some depth, beginning with the definition and representation of chunks. 
We will see regular expression and n-gram approaches to chunking, and will develop and evaluate chunkers using the 
CoNLL-2000 chunking corpus. We will then return in (5) and 7.6 to the tasks of named entity recognition and relation 
extraction.

Noun Phrase Chunking

We will begin by considering the task of noun phrase chunking, or NP-chunking, where we search for chunks 
corresponding to individual noun phrases. For example, here is some Wall Street Journal text with NP-chunks 
marked using brackets:

[ The/DT market/NN ] for/IN [ system-management/NN software/NN ] for/IN [ Digital/NNP ] [ 's/POS hardware/NN ] 
is/VBZ fragmented/JJ enough/RB that/IN [ a/DT giant/NN ] such/JJ as/IN [ Computer/NNP Associates/NNPS ] 
should/MD do/VB well/RB there/RB ./.

As we can see, NP-chunks are often smaller pieces than complete noun phrases. For example, the market for 
system-management software for Digital's hardware is a single noun phrase (containing two nested noun phrases), 
but it is captured in NP-chunks by the simpler chunk the market. One of the motivations for this difference is 
that NP-chunks are defined so as not to contain other NP-chunks. Consequently, any prepositional phrases or 
subordinate clauses that modify a nominal will not be included in the corresponding NP-chunk, since they almost 
certainly contain further noun phrases.

One of the most useful sources of information for NP-chunking is part-of-speech tags. This is one of the motivations
for performing part-of-speech tagging in our information extraction system. We demonstrate this approach using an 
example sentence that has been part-of-speech tagged in 7.3. In order to create an NP-chunker, we will first define
a chunk grammar, consisting of rules that indicate how sentences should be chunked. In this case, we will define a 
simple grammar with a single regular-expression rule [2]. This rule says that an NP chunk should be formed whenever 
the chunker finds an optional determiner (DT) followed by any number of adjectives (JJ) and then a noun (NN). Using 
this grammar, we create a chunk parser [3], and test it on our example sentence [4]. The result is a tree, which we 
can either print [5], or display graphically [6].

Tagging

>>> text = nltk.word_tokenize("And now for something completely different")
>>> nltk.pos_tag(text)
[('And', 'CC'), ('now', 'RB'), ('for', 'IN'), ('something', 'NN'),
('completely', 'RB'), ('different', 'JJ')]


>>> sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"), [1]
... ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]

>>> grammar = "NP: {<DT>?<JJ>*<NN>}" [2]

>>> cp = nltk.RegexpParser(grammar) [3]
>>> result = cp.parse(sentence) [4]
>>> print result [5]
(S
  (NP the/DT little/JJ yellow/JJ dog/NN)
  barked/VBD
  at/IN
  (NP the/DT cat/NN))
>>> result.draw()

A Simplified Part-of-Speech Tagset

Tagged corpora use many different conventions for tagging words. To help us get started, we will be looking at a 
simplified tagset (shown in 5.1).

Table 5.1:
Simplified Part-of-Speech Tagset

Tag	Meaning	Examples
ADJ	adjective	new, good, high, special, big, local
ADV	adverb	really, already, still, early, now
CNJ	conjunction	and, or, but, if, while, although
DET	determiner	the, a, some, most, every, no
EX	existential	there, there's
FW	foreign word	dolce, ersatz, esprit, quo, maitre
MOD	modal verb	will, can, would, may, must, should
N	noun	year, home, costs, time, education
NP	proper noun	Alison, Africa, April, Washington
NUM	number	twenty-four, fourth, 1991, 14:24
PRO	pronoun	he, their, her, its, my, I, us
P	preposition	on, of, at, with, by, into, under
TO	the word to	to
UH	interjection	ah, bang, ha, whee, hmpf, oops
V	verb	is, has, get, do, make, see, run
VD	past tense	said, took, told, made, asked
VG	present participle	making, going, playing, working
VN	past participle	given, taken, begun, sung
WH	wh determiner	who, which, when, what, where, how

Chunking with Regular Expressions

To find the chunk structure for a given sentence, the RegexpParser chunker begins with a flat structure in which no 
tokens are chunked. The chunking rules are applied in turn, successively updating the chunk structure. Once all of 
the rules have been invoked, the resulting chunk structure is returned.

7.4 shows a simple chunk grammar consisting of two rules. The first rule matches an optional determiner or possessive 
pronoun, zero or more adjectives, then a noun. The second rule matches one or more proper nouns. We also define an 
example sentence to be chunked [1], and run the chunker on this input [2].

 	
grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
      {<NNP>+}                # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)
sentence = [("Rapunzel", "NNP"), ("let", "VBD"), ("down", "RP"), [1]
                 ("her", "PP$"), ("long", "JJ"), ("golden", "JJ"), ("hair", "NN")]
 	
>>> print cp.parse(sentence) [2]
(S
  (NP Rapunzel/NNP)
  let/VBD
  down/RP
  (NP her/PP$ long/JJ golden/JJ hair/NN))



If a tag pattern matches at overlapping locations, the leftmost match takes precedence. For example, if we apply a 
rule that matches two consecutive nouns to a text containing three consecutive nouns, then only the first two nouns 
will be chunked:

*IMPORTANT* -- Helps to detect combinations of proper nouns

>>> nouns = [("money", "NN"), ("market", "NN"), ("fund", "NN")]
>>> grammar = "NP: {<NN><NN>}  # Chunk two consecutive nouns"
>>> cp = nltk.RegexpParser(grammar)
>>> print cp.parse(nouns)
(S (NP money/NN market/NN) fund/NN)
Once we have created the chunk for money market, we have removed the context that would have permitted fund to be 
included in a chunk. This issue would have been avoided with a more permissive chunk rule, e.g. NP: {<NN>+}.


*IMPORTANT*
Exploring Text Corpora

In 5.2 we saw how we could interrogate a tagged corpus to extract phrases matching a particular sequence of 
part-of-speech tags. We can do the same work more easily with a chunker, as follows:

 	
>>> cp = nltk.RegexpParser('CHUNK: {<V.*> <TO> <V.*>}')
>>> brown = nltk.corpus.brown
>>> for sent in brown.tagged_sents():
...     tree = cp.parse(sent)
...     for subtree in tree.subtrees():
...         if subtree.node == 'CHUNK': print subtree
...
(CHUNK combined/VBN to/TO achieve/VB)
(CHUNK continue/VB to/TO place/VB)
(CHUNK serve/VB to/TO protect/VB)
(CHUNK wanted/VBD to/TO wait/VB)
(CHUNK allowed/VBN to/TO place/VB)
(CHUNK expected/VBN to/TO become/VB)
...
(CHUNK seems/VBZ to/TO overtake/VB)
(CHUNK want/VB to/TO buy/VB)


Chinking

Sometimes it is easier to define what we want to exclude from a chunk. We can define a chink to be a sequence of 
tokens that is not included in a chunk. In the following example, barked/VBD at/IN is a chink:

 [ the/DT little/JJ yellow/JJ dog/NN ] barked/VBD at/IN [ the/DT cat/NN ]
Chinking is the process of removing a sequence of tokens from a chunk. If the matching sequence of tokens spans an 
entire chunk, then the whole chunk is removed; if the sequence of tokens appears in the middle of the chunk, these 
tokens are removed, leaving two chunks where there was only one before. If the sequence is at the periphery of the 
chunk, these tokens are removed, and a smaller chunk remains. These three possibilities are illustrated in 7.3.

Table 7.3:
Three chinking rules applied to the same chunk

` `	             Entire chunk	             Middle of a chunk	      End of a chunk

Input	           [a/DT little/JJ dog/NN]	[a/DT little/JJ dog/NN]	[a/DT little/JJ dog/NN]
Operation	Chink "DT JJ NN"	              Chink "JJ"	             Chink "NN"
Pattern	        }DT JJ NN{	              }JJ{	                   }NN{
Output	         a/DT little/JJ dog/NN	[a/DT] little/JJ [dog/NN]	[a/DT little/JJ] dog/NN

In 7.5, we put the entire sentence into a single chunk, then excise the chinks.

 	
grammar = r"""
  NP:
    {<.*>+}          # Chunk everything
    }<VBD|IN>+{      # Chink sequences of VBD and IN
  """
sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),
       ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]
cp = nltk.RegexpParser(grammar)
 	
>>> print cp.parse(sentence)
(S
  (NP the/DT little/JJ yellow/JJ dog/NN)
  barked/VBD
  at/IN
  (NP the/DT cat/NN))


*IMPORTANT*
Representing Chunks: Tags vs Trees  -- IOB Naming

As befits their intermediate status between tagging and parsing (8), chunk structures can be represented using 
either tags or trees. The most widespread file representation uses IOB tags. In this scheme, each token is tagged 
with one of three special chunk tags, I (inside), O (outside), or B (begin). A token is tagged as B if it marks the 
beginning of a chunk. Subsequent tokens within the chunk are tagged I. All other tokens are tagged O. The B and I 
tags are suffixed with the chunk type, e.g. B-NP, I-NP. Of course, it is not necessary to specify a chunk type for 
tokens that appear outside a chunk, so these are just labeled O. An example of this scheme is shown in 7.6.

Figure 7.6: Tag Representation of Chunk Structures
IOB tags have become the standard way to represent chunk structures in files, and we will also be using this format. 
Here is how the information in 7.6 would appear in a file:

We PRP B-NP
saw VBD O
the DT B-NP
little JJ I-NP
yellow JJ I-NP
dog NN I-NP


We can use the NLTK corpus module to access a larger amount of chunked text. The CoNLL 2000 corpus contains 270k 
words of Wall Street Journal text, divided into "train" and "test" portions, annotated with part-of-speech tags and 
chunk tags in the IOB format. We can access the data using nltk.corpus.conll2000. Here is an example that reads the 
100th sentence of the "train" portion of the corpus:

 	
>>> from nltk.corpus import conll2000
>>> print conll2000.chunked_sents('train.txt')[99]
(S
  (PP Over/IN)
  (NP a/DT cup/NN)
  (PP of/IN)
  (NP coffee/NN)
  ,/,
  (NP Mr./NNP Stone/NNP)
  (VP told/VBD)
  (NP his/PRP$ story/NN)
  ./.)


As you can see, the CoNLL 2000 corpus contains three chunk types: NP chunks, which we have already seen; VP chunks 
such as has already delivered; and PP chunks such as because of. Since we are only interested in the NP chunks right 
now, we can use the chunk_types argument to select them:

 	
>>> print conll2000.chunked_sents('train.txt', chunk_types=['NP'])[99]
(S
  Over/IN
  (NP a/DT cup/NN)
  of/IN
  (NP coffee/NN)
  ,/,
  (NP Mr./NNP Stone/NNP)
  told/VBD
  (NP his/PRP$ story/NN)
  ./.)



As you can see, the CoNLL 2000 corpus contains three chunk types: NP chunks, which we have already seen; VP chunks 
such as has already delivered; and PP chunks such as because of. Since we are only interested in the NP chunks right 
now, we can use the chunk_types argument to select them:

 	
>>> print conll2000.chunked_sents('train.txt', chunk_types=['NP'])[99]
(S
  Over/IN
  (NP a/DT cup/NN)
  of/IN
  (NP coffee/NN)
  ,/,
  (NP Mr./NNP Stone/NNP)
  told/VBD
  (NP his/PRP$ story/NN)
  ./.)
Simple Evaluation and Baselines

Now that we can access a chunked corpus, we can evaluate chunkers. We start off by establishing a baseline for the 
trivial chunk parser cp that creates no chunks:

 	
>>> from nltk.corpus import conll2000
>>> cp = nltk.RegexpParser("")
>>> test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
>>> print cp.evaluate(test_sents)
ChunkParse score:
    IOB Accuracy:  43.4%
    Precision:      0.0%
    Recall:         0.0%
    F-Measure:      0.0%
The IOB tag accuracy indicates that more than a third of the words are tagged with O, i.e. not in an NP chunk. 
However, since our tagger did not find any chunks, its precision, recall, and f-measure are all zero. Now let's 
try a naive regular expression chunker that looks for tags beginning with letters that are characteristic of noun 
phrase tags (e.g. CD, DT, and JJ).

 	
>>> grammar = r"NP: {<[CDJNP].*>+}"
>>> cp = nltk.RegexpParser(grammar)
>>> print cp.evaluate(test_sents)
ChunkParse score:
    IOB Accuracy:  87.7%
    Precision:     70.6%
    Recall:        67.8%
    F-Measure:     69.2%
As you can see, this approach achieves decent results. However, we can improve on it by adopting a more data-driven 
approach, where we use the training corpus to find the chunk tag (I, O, or B) that is most likely for each 
part-of-speech tag. In other words, we can build a chunker using a unigram tagger (5.4). But rather than trying to 
determine the correct part-of-speech tag for each word, we are trying to determine the correct chunk tag, given each 
word's part-of-speech tag.

In 7.8, we define the UnigramChunker class, which uses a unigram tagger to label sentences with chunk tags. Most of 
the code in this class is simply used to convert back and forth between the chunk tree representation used by NLTK's 
ChunkParserI interface, and the IOB representation used by the embedded tagger. The class defines two methods: a 
constructor [1] which is called when we build a new UnigramChunker; and the parse method [3] which is used to chunk 
new sentences.

 	
class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents): [1]
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data) [2]

    def parse(self, sentence): [3]
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)
        

The constructor [1] expects a list of training sentences, which will be in the form of chunk trees. It first converts 
training data to a form that suitable for training the tagger, using tree2conlltags to map each chunk tree to a list 
of word,tag,chunk triples. It then uses that converted training data to train a unigram tagger, and stores it in 
self.tagger for later use.

The parse method [3] takes a tagged sentence as its input, and begins by extracting the part-of-speech tags from that 
sentence. It then tags the part-of-speech tags with IOB chunk tags, using the tagger self.tagger that was trained in 
the constructor. Next, it extracts the chunk tags, and combines them with the original sentence, to yield conlltags. 
Finally, it uses conlltags2tree to convert the result back into a chunk tree.

Now that we have UnigramChunker, we can train it using the CoNLL 2000 corpus, and test its resulting performance:

 	
>>> test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
>>> train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
>>> unigram_chunker = UnigramChunker(train_sents)
>>> print unigram_chunker.evaluate(test_sents)
ChunkParse score:
    IOB Accuracy:  92.9%
    Precision:     79.9%
    Recall:        86.8%
    F-Measure:     83.2%
This chunker does reasonably well, achieving an overall f-measure score of 83%. Let's take a look at what it's learned,
by using its unigram tagger to assign a tag to each of the part-of-speech tags that appear in the corpus:

 	
>>> postags = sorted(set(pos for sent in train_sents
...                      for (word,pos) in sent.leaves()))
>>> print unigram_chunker.tagger.tag(postags)
[('#', 'B-NP'), ('$', 'B-NP'), ("''", 'O'), ('(', 'O'), (')', 'O'),
 (',', 'O'), ('.', 'O'), (':', 'O'), ('CC', 'O'), ('CD', 'I-NP'),
 ('DT', 'B-NP'), ('EX', 'B-NP'), ('FW', 'I-NP'), ('IN', 'O'),
 ('JJ', 'I-NP'), ('JJR', 'B-NP'), ('JJS', 'I-NP'), ('MD', 'O'),
 ('NN', 'I-NP'), ('NNP', 'I-NP'), ('NNPS', 'I-NP'), ('NNS', 'I-NP'),
 ('PDT', 'B-NP'), ('POS', 'B-NP'), ('PRP', 'B-NP'), ('PRP$', 'B-NP'),
 ('RB', 'O'), ('RBR', 'O'), ('RBS', 'B-NP'), ('RP', 'O'), ('SYM', 'O'),
 ('TO', 'O'), ('UH', 'O'), ('VB', 'O'), ('VBD', 'O'), ('VBG', 'O'),
 ('VBN', 'O'), ('VBP', 'O'), ('VBZ', 'O'), ('WDT', 'B-NP'),
 ('WP', 'B-NP'), ('WP$', 'B-NP'), ('WRB', 'O'), ('``', 'O')]
It has discovered that most punctuation marks occur outside of NP chunks, with the exception of # and $, both of which 
are used as currency markers. It has also found that determiners (DT) and possessives (PRP$ and WP$) occur at the 
beginnings of NP chunks, while noun types (NN, NNP, NNPS, NNS) mostly occur inside of NP chunks.

Having built a unigram chunker, it is quite easy to build a bigram chunker: we simply change the class name to 
BigramChunker, and modify line [2] in 7.8 to construct a BigramTagger rather than a UnigramTagger. The resulting 
chunker has slightly higher performance than the unigram chunker:

 	
>>> bigram_chunker = BigramChunker(train_sents)
>>> print bigram_chunker.evaluate(test_sents)
ChunkParse score:
    IOB Accuracy:  93.3%
    Precision:     82.3%
    Recall:        86.8%
    F-Measure:     84.5%

7.5   Named Entity Recognition

At the start of this chapter, we briefly introduced named entities (NEs). Named entities are definite noun phrases 
that refer to specific types of individuals, such as organizations, persons, dates, and so on. 7.4 lists some of the 
more commonly used types of NEs. These should be self-explanatory, except for "Facility": human-made artifacts in the 
domains of architecture and civil engineering; and "GPE": geo-political entities such as city, state/province, and 
country.


Another major source of difficulty is caused by the fact that many named entity terms are ambiguous. Thus May and 
North are likely to be parts of named entities for DATE and LOCATION, respectively, but could both be part of a 
PERSON; conversely Christian Dior looks like a PERSON but is more likely to be of type ORGANIZATION. A term like 
Yankee will be ordinary modifier in some contexts, but will be marked as an entity of type ORGANIZATION in the phrase 
Yankee infielders.

Further challenges are posed by multi-word names like Stanford University, and by names that contain other names 
such as Cecil H. Green Library and Escondido Village Conference Service Center. In named entity recognition, therefore,
we need to be able to identify the beginning and end of multi-token sequences.

Named entity recognition is a task that is well-suited to the type of classifier-based approach that we saw for noun 
phrase chunking. In particular, we can build a tagger that labels each word in a sentence using the IOB format, where 
chunks are labeled by their appropriate type. Here is part of the CONLL 2002 (conll2002) Dutch training data:

Eddy N B-PER
Bonte N I-PER
is V O
woordvoerder N O
van Prep O
diezelfde Pron O
Hogeschool N B-ORG
. Punc O
In this representation, there is one token per line, each with its part-of-speech tag and its named entity tag. Based 
on this training corpus, we can construct a tagger that can be used to label new sentences; and use the 
nltk.chunk.conlltags2tree() function to convert the tag sequences into a chunk tree.

NLTK provides a classifier that has already been trained to recognize named entities, accessed with the function 
nltk.ne_chunk(). If we set the parameter binary=True [1], then named entities are just tagged as NE; otherwise, the 
classifier adds category labels such as PERSON, ORGANIZATION, and GPE.

 	
>>> sent = nltk.corpus.treebank.tagged_sents()[22]
>>> print nltk.ne_chunk(sent, binary=True) [1]
(S
  The/DT
  (NE U.S./NNP)
  is/VBZ
  one/CD
  ...
  according/VBG
  to/TO
  (NE Brooke/NNP T./NNP Mossman/NNP)
  ...)
 	
>>> print nltk.ne_chunk(sent) 
(S
  The/DT
  (GPE U.S./NNP)
  is/VBZ
  one/CD
  ...
  according/VBG
  to/TO
  (PERSON Brooke/NNP T./NNP Mossman/NNP)
  ...)
7.6   Relation Extraction

Once named entities have been identified in a text, we then want to extract the relations that exist between them. 
As indicated earlier, we will typically be looking for relations between specified types of named entity. One way of 
approaching this task is to initially look for all triples of the form (X, α, Y), where X and Y are named entities of 
the required types, and α is the string of words that intervenes between X and Y. We can then use regular expressions 
to pull out just those instances of α that express the relation that we are looking for. The following example 
searches for strings that contain the word in. The special regular expression (?!\b.+ing\b) is a negative lookahead 
assertion that allows us to disregard strings such as success in supervising the transition of, where in is followed 
by a gerund.

 	
>>> IN = re.compile(r'.*\bin\b(?!\b.+ing)')
>>> for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
...     for rel in nltk.sem.extract_rels('ORG', 'LOC', doc,
...                                      corpus='ieer', pattern = IN):
...         print nltk.sem.show_raw_rtuple(rel)
[ORG: 'WHYY'] 'in' [LOC: 'Philadelphia']
[ORG: 'McGlashan &AMP; Sarrail'] 'firm in' [LOC: 'San Mateo']
[ORG: 'Freedom Forum'] 'in' [LOC: 'Arlington']
[ORG: 'Brookings Institution'] ', the research group in' [LOC: 'Washington']
[ORG: 'Idealab'] ', a self-described business incubator based in' [LOC: 'Los Angeles']
[ORG: 'Open Text'] ', based in' [LOC: 'Waterloo']
[ORG: 'WGBH'] 'in' [LOC: 'Boston']
[ORG: 'Bastille Opera'] 'in' [LOC: 'Paris']
[ORG: 'Omnicom'] 'in' [LOC: 'New York']
[ORG: 'DDB Needham'] 'in' [LOC: 'New York']
[ORG: 'Kaplan Thaler Group'] 'in' [LOC: 'New York']
[ORG: 'BBDO South'] 'in' [LOC: 'Atlanta']
[ORG: 'Georgia-Pacific'] 'in' [LOC: 'Atlanta']
Searching for the keyword in works reasonably well, though it will also retrieve false positives such as [ORG: House 
Transportation Committee] , secured the most money in the [LOC: New York]; there is unlikely to be simple string-based
method of excluding filler strings such as this.

As shown above, the conll2002 Dutch corpus contains not just named entity annotation but also part-of-speech tags. 
This allows us to devise patterns that are sensitive to these tags, as shown in the next example. The method 
show_clause() prints out the relations in a clausal form, where the binary relation symbol is specified as the value 
of parameter relsym [1].

 	
>>> from nltk.corpus import conll2002
>>> vnv = """
... (
... is/V|    # 3rd sing present and
... was/V|   # past forms of the verb zijn ('be')
... werd/V|  # and also present
... wordt/V  # past of worden ('become)
... )
... .*       # followed by anything
... van/Prep # followed by van ('of')
... """
>>> VAN = re.compile(vnv, re.VERBOSE)
>>> for doc in conll2002.chunked_sents('ned.train'):
...     for r in nltk.sem.extract_rels('PER', 'ORG', doc,
...                                    corpus='conll2002', pattern=VAN):
...         print  nltk.sem.show_clause(r, relsym="VAN") [1]
VAN("cornet_d'elzius", 'buitenlandse_handel')
VAN('johan_rottiers', 'kardinaal_van_roey_instituut')
VAN('annie_lennox', 'eurythmics')




