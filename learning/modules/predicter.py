from sklearn.naive_bayes import BernoulliNB
from labeler import Labeler

class Predicter(BernoulliNB):
    
    # accept training data set as 2-column DataFrame
    
    def __init__(self):
        super().__init__()
    
    # give dictionary to the labeler to be initiated
    def init_labeler(self, dictionary):
        self.labeler = Labeler(dictionary)
    
    # now that labeler can vectorize our sentences
    # we are ready to train our model
    # df[0] -> sentences
    # df[1] -> scores
    def train(self, sentence_list, labels):
        
        feature_vector = (self.labeler.label_sentence_list(sentence_list))
        super().fit(feature_vector, labels)
    
    def test(self, sentences, real_values):
        # sentences -> pandas Series of sentences
        test_vector = self.labeler.label_sentence_list(sentences)
        test_results = super().predict(test_vector)
        # analyze the results
        real_pred = zip(real_values, test_results)
        correct_lbl = sum(list(map(lambda x:1 if x[0]==x[1] else 0, real_pred)))
        return correct_lbl *1.0/ len(real_values)
    
    def predict_sentence(self, sentence):
        s = [sentence]
        vector = self.labeler.label_sentence_list(s)
        return super().predict(vector)[0]