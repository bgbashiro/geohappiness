import numpy as np
import csv, sys
from sklearn.naive_bayes import BernoulliNB
from sentence_sent import SentenceLabeler

def line_to_array(line):
    return list(map(float, line.split(' ')))

def cr_train_vector(filename):
    """filename -> source file of vectors
    """
    arr_l = []
    with open(filename) as xs_fp:
        for line in xs_fp.readlines():
            row = line_to_array(line)
            arr_l.append(row)
    return np.array(arr_l)

def cr_label_vector(filename):
    """filename -> source file of labels
    """
    arr_l = []
    with open(filename) as xs_fp:
        for line in xs_fp.readlines():
            arr_l.append(int(line))
    return np.array(arr_l)

def cr_test_vector(test_file, dictionary, test_vector):
   
    with open(dictionary) as dict_fp, open(test_file) as data_fp:
        sb = SentenceLabeler(dict_fp,data_fp)
        sb.init_dict()
        sb.label_data(test_vector)
    
    arr_l = []
    data_fp = open(test_vector)
    with open(test_vector) as xs_fp:
        for line in xs_fp.readlines():
            row = line_to_array(line)
            arr_l.append(row)
    
    return np.array(arr_l)


def main():
    """python sent_analyse.py <data vectors> <labels> <testdata> <dictionary> <test vectors> <results>
    data vectors -> whitespace seperated vectors of training set
    labels       -> labels corresponding to training vectors
    testdata     -> test set of sentences
    dictionary   -> dictionary used to vectorize the sentences
    test vectors -> whitespace seperated vectors of test set (will be created)
    results      -> csv file where the results of prediction will be dumped
    """
    # prepare the vectors of sentence as xs
    xs = cr_train_vector(sys.argv[1])
    # prepare the label file as vector ys
    ys = cr_label_vector(sys.argv[2])
    brnl = BernoulliNB()
    brnl.fit(xs, ys)
    # prepare the test dataset
    test_xs = cr_test_vector(sys.argv[3], sys.argv[4], sys.argv[5])
    results = brnl.predict(test_xs)
    with open(sys.argv[6], 'w') as prediction_fp, open(sys.argv[3]) as data_fp:
        csv_pen = csv.writer(prediction_fp)
        for x in results:
            sentence = data_fp.readline()
            csv_pen.writerow([sentence.rstrip(), x]) 


if __name__ == '__main__':
    main()