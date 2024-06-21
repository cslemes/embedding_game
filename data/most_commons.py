import nltk
from nltk import word_tokenize

from nltk.probability import FreqDist
import pandas as pd
nltk.download('punkt')

## https://pt.wikipedia.org/wiki/Corpus_Mac-Morpho
## Download corpus 1M Words
nltk.download('mac_morpho')

dataset = list(nltk.corpus.mac_morpho.tagged_sents())

# Filtering by POS
filter_tags = ['ADJ', 'N', 'PROADJ', 'V', 'PCP', 'VAUX']

filtered_words = ""
for tup in dataset[:10000]:
    for word, pos in tup:
        if pos in filter_tags:
            filtered_words += word + '\n'
    #print(tup)

filtered_words

corpus_tokens = nltk.word_tokenize(filtered_words)

corpus_tokens


freq = FreqDist(corpus_tokens)

secret_words = freq.most_common(3000)

df = pd.DataFrame(secret_words, columns=['word', 'frequency'])

df.to_pickle('secret_words.pkl')
