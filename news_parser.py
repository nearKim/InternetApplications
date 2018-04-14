from bs4 import BeautifulSoup
from urllib.request import urlopen
import nltk



# 1-1. print title, author, date, video title, article content using BeautifulSoup
# TODO - fill in your team's url
url = ''

data = urlopen(url).read()
doc = BeautifulSoup(data, 'html.parser')

# TODO - print title
title = ''
print("Title: ", title)

# TODO - print author
author = ''
print("Author: ", author)

# TODO - print date
date = ''
print("Date: ", date)

# TODO - print video title
video_title = ''
print("Video title: ", video_title)

# TODO - print article content
content = ''
print("Content: ", content)


# 1-2. Tokenize news article content by words
# TODO - tokenize article content
tokenized_words = ''
print(tokenized_words)


# 1-3. POS-Tag tokenized words and sort POS by frequency
# TODO - POS_Tag tokenized words
tagged_list = ''
print(tagged_list)

# TODO - sort POS by frequency
for tag in tagged_list:
    pass