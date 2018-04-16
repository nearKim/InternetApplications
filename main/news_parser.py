from bs4 import BeautifulSoup
from urllib.request import urlopen
import nltk

print('-----------------------------------\n#1.1 Basic BeutifulSoup\n-----------------------------------')

# 1-1. BeutifulSoup을 이용하여 기사의 title, author, date, video title, article content 를 출력
url = 'http://money.cnn.com/2018/04/02/technology/mark-zuckerberg-tim-cook-facebook-apple/index.html'

data = urlopen(url).read()
doc = BeautifulSoup(data, 'html.parser')

title = doc.find("h1", class_="article-title speakable").string
print("Title: ", title)

author = doc.find("span", class_="byline").string
print("Author: ", author)

date = doc.find("span", class_="cnnDateStamp").string
print("Date: ", date)

video_title = doc.find(class_="js-vid-hed-vid0 cnnHeadline").string;
print("Video title: ", video_title)

content = ''
content_raw = doc.find(id="storytext")
content_sliced = content_raw.find_all("h2")
content_sliced.extend(content_raw.find_all("p"))
# print("Content: ", content)
for s in content_sliced:
    content += s.text
print("Content: ", content)

print('''


''')

# 1-2. 단어 단위로 뉴스 기사를 토큰화
print(
    '-----------------------------------\n#1.2 Tokenize article content by words\n-----------------------------------')
tokenized_words = nltk.tokenize.word_tokenize(content)
print(tokenized_words)

print('''



''')

# 1-3. 토큰화된 단어들을 POS-Tag 하고 빈도수 별로 정렬
print('--------------------------------\n#1.3 POS-tag tokenized words\n--------------------------------')
tagged_list = nltk.pos_tag(tokenized_words)
print(tagged_list)

print('''


''')

dictionary = dict()
for tag in tagged_list:
    if tag[1] in dictionary:
        # POS is in the dictionary
        pass
    else:
        # POS is not in the dictionary
        POScount = sum(x[1].count(tag[1]) for x in tagged_list)
        dictionary.update({tag[1]: POScount})

# dictionary 의 빠른 정렬을 위한 operator 모듈을 import
import operator

sortedArray = sorted(dictionary.items(),
                     key=operator.itemgetter(1),
                     reverse=True)

print("_______\nPOS : freq\n_________")
for d in sortedArray:
    print(d[0], ":", d[1])
