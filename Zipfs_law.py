from nltk.tokenize import word_tokenize

with open("bible.txt", 'r') as f:
    text = f.read()
# with open("war-and-peace.txt", 'r', encoding='utf-8') as f:
#    text = f.read()


# 특수문자 제거(. , ? ! ; : 's)
for c in ['.', ',', '?', '!', ';', ':', '\'s']:
    text = text.replace(c, '')
# 소문자로 변환
text = text.lower()

tokenized_words = word_tokenize(text)  # 다른 tokenizer 사용 가능
total_word_count = len(tokenized_words)

word_count_dict = {}

for word in tokenized_words:
    if word in word_count_dict:
        word_count_dict[word] += 1
    else:
        word_count_dict[word] = 1

import operator
word_frequency_list = sorted(word_count_dict.items(), key=operator.itemgetter(1), reverse=True)
# print(word_frequency_list)


word_rank_list = []
# index가 rank에 대응(index = rank - 1) : word_rank_list[rank-1] = word

for word in word_frequency_list:
    word_rank_list.append(word[0])
col_head = "Word".ljust(20) + " Freq".ljust(11) + " r".ljust(7) + "Pr".ljust(20) + "r*Pr"
print(col_head)

for i in range(len(word_count_dict)):
    word = word_rank_list[i]
    freq = word_count_dict[word]
    occur_prob = freq / total_word_count
    # freq가 같은 경우 rank도 같아야 하지만 현재 word_rank_list의 index는 1씩 증가하며 모두 다른 값을 가지므로
    # 바로 rank = i + 1을 적용할 수 없음
    if freq == word_count_dict[word_rank_list[i-1]]:
        pass
    else:
        rank = i + 1

    print(word.ljust(20), str(freq).ljust(10), str(rank).ljust(5), '%.17f' % occur_prob, '%.6f' % (rank * occur_prob))
