>>> f = open("AChristmasCarol.txt")
>>> raw = f.read()
>>> f.close()
>>> tokens = nltk.word_tokenize(raw)
>>> words = [w.lower() for w in tokens]
>>> words[:20]
['title', ':', 'a', 'christmas', 'carol', 'author', ':', 'charles', 'dickens', 'illustrator', ':', 'arthur', 'rackham', 'release', 'date', ':', 'december', '24', ',', '2007']
>>> vocab = sorted(set(words))
>>> text = nltk.Text(tokens)
>>> text[:20]
['Title', ':', 'A', 'Christmas', 'Carol', 'Author', ':', 'Charles', 'Dickens', 'Illustrator', ':', 'Arthur', 'Rackham', 'Release', 'Date', ':', 'December', '24', ',', '2007']
