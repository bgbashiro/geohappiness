from wordcount import mk_words
from sklearn.preprocessing import LabelBinarizer
from functools import reduce

class Labeler(LabelBinarizer):
    
    def __init__(self, dictionary):
        super().__init__()
        super().fit(dictionary)
    
    def label_sentence(self, sentence):
        words = mk_words(sentence)
        if words:
            lbl_words = super().transform(words)
            return reduce(lambda x,y:x+y, lbl_words)
        else:
            return super().transform([''])[0]
        
    def label_sentence_list(self, xs):
        return [self.label_sentence(x) for x in xs]