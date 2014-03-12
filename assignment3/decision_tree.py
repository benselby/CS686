#!/usr/bin/python

# A decision tree program for classification of newsgroup postings
#
# Ben Selby, March 2014

def main():
    # First load all the training and test data and labels
    words = []
    with open('words.txt', 'r') as f:
        for line in f:
            words.append( line.split()[0] )

    #print( words )
    print( len(words) )
    
    train_data = []
    with open('trainData.txt', 'r') as f:
        for line in f:
            train_data.append( line.split() )
    #print train_data
    print( len(train_data) )
    
    train_labels = []
    with open('trainLabel', 'r') as f:
        for line in f:
            train_labels.append( line.split() )
    print( "No. of training documents:", len(train_labels) )
    
    test_data = []
    with open('testData.txt', 'r') as f:
        for line in f:
            test_data.append( line.split() )
    
    test_labels = []
    with open('testLabel', 'r') as f:
        for line in f:
            test_labels.append( line.split() )

def load_data_and_labels():
    pass

if __name__ == "__main__":
    main()
