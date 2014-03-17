#!/usr/bin/python

# A decision tree program for classification of newsgroup postings
#
# Ben Selby, March 2014

def main():
    # First load all the training and test data and labels
    [words, train_data, train_labels, test_data, test_labels] = load_data_and_labels()

def load_data_and_labels():
    print "Loading words, training and testing data..."
    words = []
    with open('words.txt', 'r') as f:
        for line in f:
            words.append( line.split()[0] )

    print "No. of words:", len(words) 
    
    train_data = []
    with open('trainData.txt', 'r') as f:
        for line in f:
            train_data.append( line.split() )
    
    train_labels = []
    with open('trainLabel.txt', 'r') as f:
        for line in f:
            train_labels.append( line.split() )
    print "No. of training documents:", len(train_labels) 
    
    test_data = []
    with open('testData.txt', 'r') as f:
        for line in f:
            test_data.append( line.split() )
    
    test_labels = []
    with open('testLabel.txt', 'r') as f:
        for line in f:
            test_labels.append( line.split() )
    print "No. of test documents:", len(test_labels) 
      
    return [words, train_data, train_labels, test_data, test_labels]

if __name__ == "__main__":
    main()
