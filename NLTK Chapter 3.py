>>> url = "http://www.gutenberg.org/files/2554/2554.txt"
>>> from urllib import urlopen
>>> raw = urlopen(url).read()
>>> type(raw)
<type 'str'>
>>> raw[1:20]
'he Project Gutenber'
>>> raw[:20]
'The Project Gutenber'
>>> # Converting to NLTK
... 
>>> tokens = nltk.word_tokenize(raw)
>>> len(tokens)
244484
>>> tokens[:20]
['The', 'Project', 'Gutenberg', 'EBook', 'of', 'Crime', 'and', 'Punishment', ',', 'by', 'Fyodor', 'Dostoevsky', 'This', 'eBook', 'is', 'for', 'the', 'use', 'of', 'anyone']
>>> 
>>> # Tokenization done, now convert to nltk.Text
... 
>>> text = nltk.Text(tokens)


>>> type(text)
<class 'nltk.text.Text'>
>>> text[1000:1010]
['in', 'which', 'he', 'lodged', 'in', 'S.', 'Place', 'and', 'walked', 'slowly']
>>> 
>>> 
>>> # Dealing with HTML
... 
>>> url = "http://news.bbc.co.uk"
>>> html = urlopen(url).read()
>>> html[:20]
'<!DOCTYPE html PUBLI'
>>> 
>>> # We can remove the HTML tags with nltk.clean_html
... 
>>> raw = nltk.clean_html(html)
>>> raw[:20]
'BBC News - Home \r\n  '
>>> text = nltk.Text(nltk.word_tokenize(raw))
>>> text[:20]
['BBC', 'News', '-', 'Home', 'For', 'a', 'better', 'experience', 'on', 'your', 'device', ',', 'try', 'our', 'mobile', 'site', '.', 'Accessibility', 'links', 'Skip']
>>> len(text)
2100
>>> text[2000:]
['the', 'BBC', 'Advertise', 'With', 'Us', 'Privacy', 'Accessibility', 'Help', 'Ad', 'Choices', 'Cookies', 'Contact', 'the', 'BBC', 'Parental', 'Guidance', 'BBC', '&', 'copy', ';', '2014', 'The', 'BBC', 'is', 'not', 'responsible', 'for', 'the', 'content', 'of', 'external', 'sites.', 'Read', 'more.', 'This', 'page', 'is', 'best', 'viewed', 'in', 'an', 'up-to-date', 'web', 'browser', 'with', 'style', 'sheets', '(', 'CSS', ')', 'enabled.', 'While', 'you', 'will', 'be', 'able', 'to', 'view', 'the', 'content', 'of', 'this', 'page', 'in', 'your', 'current', 'browser', ',', 'you', 'will', 'not', 'be', 'able', 'to', 'get', 'the', 'full', 'visual', 'experience.', 'Please', 'consider', 'upgrading', 'your', 'browser', 'software', 'or', 'enabling', 'style', 'sheets', '(', 'CSS', ')', 'if', 'you', 'are', 'able', 'to', 'do', 'so', '.']
>>> text.concordance('BBC')
Building index...
Displaying 25 of 25 matches:
                                      BBC News - Home For a better experience o
o local navigation Accessibility Help BBC navigation News Sport Weather Capital
 Reports Latest Stories BREAKING NEWS BBC learns British suicide bomber in Syri
mpics 2014 Sochi 2014 : Day five Live BBC Sport Dead heat in women & # 039 ; s 
ad heat in women & # 039 ; s downhill BBC Sport Vogt wins historic ski jumping 
t Vogt wins historic ski jumping gold BBC Sport Day-by-day guide to events BBC 


>>> f = open("AChristmasCarol.txt")
>>> raw = f.read()
>>> tokens = nltk.word_tokenize(raw)
>>> words = [w.lower() for w in tokens]
>>> words[:20]
['title', ':', 'a', 'christmas', 'carol', 'author', ':', 'charles', 'dickens', 'illustrator', ':', 'arthur', 'rackham', 'release', 'date', ':', 'december', '24', ',', '2007']
>>> vocab = sorted(set(words))
>>> text = nltk.Text(tokens)
>>> text[:20]
['Title', ':', 'A', 'Christmas', 'Carol', 'Author', ':', 'Charles', 'Dickens', 'Illustrator', ':', 'Arthur', 'Rackham', 'Release', 'Date', ':', 'December', '24', ',', '2007']






