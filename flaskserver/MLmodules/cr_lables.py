
"""
script that will pull sentences and labels out of labelled set, run the
script by feeding following inputs:
python cr_labels.py <datafile> <sentences> <labels> [<left/right> optional-whether labels are on left or right, default left] 
"""
import sys

def main():
    try:
        left_lbl = False if (sys.argv[4] == 'right') else True
    except BaseException:
        left_lbl = True
    
    data_file = open(sys.argv[1])
    with open(sys.argv[2], 'w')  as sent_file, open(sys.argv[3], 'w') as label_file:
        label_pos = 0 if left_lbl else 1
        sent_pos = 0 if label_pos==1 else 1
        for line in data_file.readlines():
            line_splitted = line.split('\t')
            sentence = line_splitted[sent_pos]
            label = line_splitted[label_pos]
            sent_file.write(sentence.rstrip() + '\n')
            label_file.write(label.rstrip() + '\n')

if __name__ == '__main__':
    main()