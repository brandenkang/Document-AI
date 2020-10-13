from collections import Counter

# 1. 이전 포스트에서 크롤링한 댓글파일을 읽기전용으로 호출함
file = open('sample_outputs/IBK.text','r',encoding='utf-8')
lines = file.readlines()

# 2. 변수 okja에 전체댓글을 다시저장
okja = []
for line in lines:
    okja.append(line)
file.close()

# 3. 트윗터 패키지 안에 konlpy 모듈호출
from konlpy.tag import Twitter
twitter = Twitter()

# 4. 각 문장별로 형태소 구분하기
sentences_tag = []
for sentence in okja:
    morph = twitter.pos(sentence)
    sentences_tag.append(morph)
    print(morph)
    print('-'*30)

print(sentences_tag)
print(len(sentences_tag))
print('\n'*3)

# 5. 명사 혹은 형용사인 품사만 선별해 리스트에 담기
noun_adj_list = []
for sentence1 in sentences_tag:
    for word, tag in sentence1:
        if tag in ['Noun','Adjective']:
            noun_adj_list.append(word)

# 6. 선별된 품사별 빈도수 계산 & 상위 빈도 10위 까지 출력
counts = Counter(noun_adj_list)
print(counts.most_common(10))

