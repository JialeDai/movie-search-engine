from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
example_sent = 'This is a sample sentence, showing of the stop word filtration'
stop_words=set(stopwords.words('english'))
word_tokens = word_tokenize(example_sent)
filtered_sentence=[w for w in word_tokens if not w in stop_words]
filtered_sentence=[]
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)
        
print(word_tokens)
print(filtered_sentence)
print(type(stopwords.words('english')))
