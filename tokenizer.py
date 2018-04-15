def tokenizer(text):
    words = text.split(' ')
    tokenized_words = []
    for word in words:
        tokenized_words.append(word_tokenizer(word))
    return tokenized_words


# 2-3에서 마침표 앞,뒤,중간에 한글자만 있는지 확인하기 위한 메소드
# 짝수번째 글자가 모두 '.'가 아니면 'false'이고
# 홀수번째 글자가 모두 '.'면 'false'반환,
# 단어의 글자수가 홀수개이면 'false'반환
def acronym(word):
    a = 'true'
    if len(word) % 2 == 0:
        a = 'false'
    else:
        for i in range(1, int((len(word) - 1) / 2) + 1):
            if word[2 * i - 1] != '.':
                # 짝수번째 자리 중 마침표가 아닌 문자 존재
                a = 'false'
        for i in range(0, int((len(word) - 1) / 2) + 1):
            if word[2 * i] == '.':
                # 모든 홀수번째 자리가 마침표
                a = 'false'
    return a


def word_tokenizer(word):
    if ('.' not in word) and ('\'' not in word):
        return word
    else:
        if '\'' in word:
            # 2-1
            if word[0] == '\'' and word[len(word) - 1] == '\'':
                # 단어 맨 처음과 끝이 따옴표면 따옴표 삭제
                word = word[1:len(word) - 1]
                if '\'' in word:
                    word = word[0:word.find('\'')]
                    # 맨 앞과 뒤의 따옴표 삭제후 남아있는 따옴표 뒤의 글자 삭제
            else:
                word = word[0:word.find('\'')]
                # 따옴표 뒤의 글자 삭제
        if '.' in word:
            # 2-2
            if word[len(word) - 4:len(word)] == '.com':
                pass
                # 맨뒤에 .com이 오면 pass
            # 2-3
            elif acronym(word) == 'true':
                word = word.replace('.', '')
            else:
                pass
        return word


if __name__ == '__main__':
    text = '''i've 'hello' 'hello'world' imlab's PH.D I.B.M snu.ac.kr 127.0.0.1 galago.gif ieee.803.99 naver.com gigabyte.tw pass..fail'''
    print(tokenizer(text))
