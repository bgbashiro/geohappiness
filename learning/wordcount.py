# Create the statistics 
# [word] -> [freq]
# of document

import getopt, sys
from sklearn.feature_extraction.text import CountVectorizer 
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import NOUN, ADJ, VERB
from sklearn.preprocessing import LabelBinarizer 

def stem_word(word):
    # get word into basic form
    # going -> go, greates -> great
    # it is rather trivial way to do it
    stem = wn._morphy(word, ADJ)
    if (stem != [] and stem[-1] != word):
        return stem[-1]
    stem = wn._morphy(word, VERB)
    if (stem != [] and stem[0] != word):
        return stem[0]
    stem = wn._morphy(word, NOUN)
    if (stem == []):
        return word
    return stem[-1]

def mk_words(sentence):
    # create our vectorizer
    vect = CountVectorizer(stop_words='english')
    analyze = vect.build_analyzer()
    # analyze sentence -> split into word tokens
    words = analyze(sentence)
    # words_stem = map(stem_word, words)
    return list(words)

class Stats(object):
    
    def __init__(self):
        self.dictionary = {}
    
    def add_word(self, word):
        try:
            self.dictionary[word] +=1
        except KeyError:
            self.dictionary[word] = 1
    
    def add_sentence(self, sentence):
        words = mk_words(sentence)
        for word in words:
            self.add_word(word)
    
    def process_file(self, filename, target):
        """read the <filename> text file, dump stats to <target>
        """
        with open(filename) as fp_file:
            for line in fp_file.readlines():
                self.add_sentence(line)
        with open(target, 'w') as fp_target:
            for key in self.dictionary:
                fp_target.write('{},{}\n'.format(key, self.dictionary[key]))
    
def main():
    """Run the script by wordcount.py <inputname> <outputname>
    """
    try:
        # document to be analyzed
        doc = sys.argv[1]
        # statististics file where results will be dumped
        statfile = sys.argv[2]
    except BaseException:
        print('Run command by "python wordcount.py <inputfilename> <outputfilename>"')
    
    stat = Stats()
    stat.process_file(doc, statfile)        

if __name__ == '__main__':
    main()