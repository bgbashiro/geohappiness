# using scikit learn label_binarize to generate binary vectors of sentences
# then use sklearn naive bayes to train the model
# then predict the happiness level of the sentence
# WHY NOT tensorflow word2vec and ANN? --> idk, maybe in the future

from sklearn.preprocessing import LabelBinarizer
import numpy as np
from wordcount import mk_words
import sys

def array_to_line(arr):
    """get np array turn it into line that can be dumped to file
    """
    return ' '.join(map(str, arr)) + '\n'

class SentenceLabeler(LabelBinarizer):

    def __init__(self, dict_fp, data_fp):
        """create object with dictionary file pointer and data file pointer
        """
        self.dict_fp = dict_fp
        self.data_fp = data_fp
        super().__init__()

    def init_dict(self):
        """initialize labelbinarizer to use dictionary
        """
        dict_l = []
        for line in self.dict_fp.readlines():
            dict_l.append(line.strip())
        super().fit(dict_l)

    def label_sentence(self, sent):
        words = mk_words(sent)
        word_labels = super().transform(words)
        # CAREFUL 0 index means label is befo
        sent_label = word_labels[0]
        for i in range(1, len(word_labels)):
            sent_label = sent_label+word_labels[i]
        # if there are any >1 values in vector, turn them into 1
        aux_convert = np.vectorize(lambda x:0 if x==0 else 1)
        return aux_convert(sent_label)
    
    def label_data(self,result_filename):
        """label the document pointed by data_fp, dump results
        to filename.txt
        """
        result_fp = open(result_filename, 'w')
        for line in self.data_fp.readlines():
            vect_s = self.label_sentence(line)
            result_fp.write(array_to_line(vect_s))
        result_fp.close()

def main():
    """python sentence_sent.py <dict> <document> <target>
    dict -> dictionary of words to use
    document -> document containing sentences to turn into vectors
    target -> file to dump the results
    """
    dict_fp = open(sys.argv[1])
    data_fp = open(sys.argv[2])
    sb = SentenceLabeler(dict_fp, data_fp)
    sb.init_dict()
    sb.label_data(sys.argv[3])
    

if __name__ == '__main__':
    main()