from nltk.tokenize import word_tokenize

with open("bible.txt", 'r') as f:
    text = f.read()
#특수문자 제거(. , ? ! ; : 's)
for c in ['.', ',', '?', '!', ';', ':', '\'s']:
    text = text.replace(c, '')
# 소문자로 변환
text = text.lower()

tokenized_words = word_tokenize(text)       # 다른 tokenizer 사용 가능
total_word_count = len(tokenized_words)

word_count_dict = {}
# TODO - 단어를 key로, 단어의 등장 빈도를 value로 갖는 dictionary 생성: word_cout_dict[word] = freq

word_rank_list = []
# TODO - word_count_dict를 freq 높은 순으로 나열 하여 순서대로 word_rank_list에 추가
# index가 rank에 대응(index = rank - 1) : word_rank_list[rank-1] = word


col_head = "Word".ljust(20) + " Freq".ljust(11) + " r".ljust(7) + "Pr".ljust(20) + "r*Pr"
print(col_head)

for i in range(len(word_count_dict)):
    # TODO - word, freq에 알맞은 값 지정
    word = ''
    freq = ''
    ocur_prob = freq / total_word_count
    # freq가 같은 경우 rank도 같아야 하지만 현재 word_rank_list의 index는 1씩 증가하며 모두 다른 값을 가지므로
    # 바로 rank = i + 1을 적용할 수 없음
    # TODO - 조건문을 적용하여 같은 freq값을 갖는 단어가 여러 개일 경우 rank 처리(아래 if False에서 False 대신 적절한 조건문 적용)
    if False:
        pass
    else:
        rank = i + 1

    print(word.ljust(20), str(freq).ljust(10), str(rank).ljust(5), '%.17f' % ocur_prob, '%.6f' % (rank * ocur_prob))