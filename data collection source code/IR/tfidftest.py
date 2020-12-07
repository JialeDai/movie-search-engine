List = ['apple','iphone','apple','computer','computer','python','language','nature']

def count_word(content):
    word_dic ={}
    for word in content:
        if word in word_dic:
            word_dic[word] = word_dic[word]+1
        else:
            word_dic[word]=1
    return word_dic


print(max(count_word(List),key = lambda k:count_word(List)[k]))

def getMostFrequentWord(word_dic):
    w = max(word_dic,key=lambda x:word_dic[x])
    return word_dic[w]

print(count_word(List))
for k,v in  count_word(List).items():
    print(v)

# print(getMostFrequentWord(count_word(List)))