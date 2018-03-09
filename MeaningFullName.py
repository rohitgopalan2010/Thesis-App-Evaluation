import re
import nltk

class MeaningFullName:
    def __init__(self):
        pass

    def how_meaningfull(self, words_list):#In java variable names are meaningful if they follow camel case rules.
        if len(words_list)==0:
            return 0

        sum=0.0
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())

        for word in words_list:
            # print word
            if not isinstance(word, basestring) or word=='None':
                continue

            word = re.sub("([a-z])([A-Z])","\g<1> \g<2>", word)#put space in camel case variable names
            word=word.replace("'", "")
            word=word.replace('_', ' ')
            word=word.replace('-', ' ')
            word=re.findall(r'[A-Za-z]+|\d+', word)

            # dic = enchant.Dict("en_US")#set the dictionary to american english
            num_meaningfull_parts=0
            for w in word:
                if w.lower() in english_vocab:
                    num_meaningfull_parts+=1
                if self.is_number(w):
                    num_meaningfull_parts+=1

            if len(word)==0:
                sum+=0
            else:
                sum+=(num_meaningfull_parts/len(word))

        return sum/len(words_list)


    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False