import nltk
import re
import cgi
import cgitb
from nltk.corpus import brown
from pytrie import SortedStringTrie as Trie
from __future__ import print_function


test_sentence = "has been"
prefix_tries = Trie()
sentences = brown.sents()
# print len(sentences)
word_index = 0
for word in sentences:
    merged_sentence = " ".join(word)
    # print merged_sentence
    if test_sentence in merged_sentence:
        filtered_sentence = merged_sentence.split(test_sentence)
        filtered1_sentence = filtered_sentence[1:]
        for iter_sentence in filtered1_sentence:
            filtered2_sentence = re.sub(r'[^\w\s]','',iter_sentence)
            filtered2_sentence = filtered2_sentence.strip()
            predicted_menuitem = filtered2_sentence.partition(' ')[0]
            # print predicted_menuitem
            prefix_tries[predicted_menuitem.lower()] = word_index
            word_index = word_index + 1

print(prefix_tries.items(prefix='a'))
