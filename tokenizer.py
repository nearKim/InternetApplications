def tokenizer(text):
    words = text.split(' ')
    tokenized_words = []
    for word in words:
        tokenized_words.append(word_tokenizer(word))
    return tokenized_words


def word_tokenizer(word):
    if ('.' not in word) and ('\'' not in word):
        return word
    else:
        if '\'' in word:
            # TODO - 따옴표로 시작해서 따옴표로 끝나는 단어의 따옴표 삭제, 단어 도중에 따옴표가 나오는 경우 따옴표 포함 뒤의 글자 모두 삭제
            pass
        if '.' in word:
            # TODO - ".com"으로 끝나는 단어는 토큰화되지 않도록
            # TODO - 마침표로 연결된 단어에서 마침표 앞, 뒤 및 사이에 있는 글자가 모두 1개일 경우 마침표 삭제, 0개 혹은 2개 이상이면 토큰화되지 않도록
            pass
        return word


if __name__ == '__main__':
    text = '''i've 'hello' 'hello'world' imlab's PH.D I.B.M snu.ac.kr 127.0.0.1 galago.gif ieee.803.99 naver.com gigabyte.tw pass..fail'''
    print(tokenizer(text))