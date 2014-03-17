#!/usr/bin/python

# A decision tree program for classification of newsgroup postings
#
# Ben Selby, March 2014

import math

class Node:

    def __init__( self, value ):
        self.value = value
        self.yes_child = None
        self.no_child = None

    def add_yes_child( self, yes_node ):
        self.yes_child = yes_node 

    def add_no_child( self, no_node ):
        self.no_child = no_node 


def main():
    # First load all the training and test data and labels
    [words, train_data, train_labels, test_data, test_labels] = load_data_and_labels()
    
    # Pre-allocate sparse matrices
    train_data_sparse = [ [0] * len(words) for i in range( len(train_labels) ) ]
    test_data_sparse = list(train_data_sparse)
    
    # arrange the data into sparse matrices for easier processing
    for i in train_data:
        train_data_sparse[ i[0]-1 ][ i[1]-1 ] = 1    

    # Build a decision tree using information gain:
    max_nodes = 100
    used_words = []
    tree = decision_tree_learning( train_data_sparse, train_labels, used_words, 1, max_nodes  )

    # Build a decision tree using info gain times number of documents at each leaf
#   tree2 = decision_tree_learning2( train_data_sparse, train_labels )

    # Test each tree against the test datasets and print the results:


# A priority queue implementation of DTL - uses information gain
# to rank the attributes 
# Returns an ordered list of decisions based on the provided training data
def decision_tree_learning( train_data_sparse, train_labels, used_words, i_nodes, max_nodes ):

    # check to see if we've hit the maximum number of nodes:
    if i_nodes >= max_nodes:
        return Node( plurality_value( train_labels) ) 
    if all_examples_same( train_labels ):
        return Node( train_labels[0] )

    else:
        # rank all the words by importance:
        importance_list = []
        for i in range(len(train_data_sparse[0])):
            word = train_data_sparse[0][i]
            if word not in used_words:
                importance_list.append( information_gain( i, train_data_sparse, train_labels ) )
        
        best_word_index = importance_list.index( max( importance_list ) )
        used_words.append( best_word_index )
        new_node = Node( best_word_index )
        for value in [0,1]:
            # divide the training set documents based on whether they contain the word
            new_train_data = []
            new_train_labels = []
            for i in range(len(train_data_sparse)):
                doc = train_data_sparse[i]
                if doc[best_word_index] == value:
                    new_train_data.append( doc )
                    new_train_labels.append( train_labels[i] ) 
                child_node = decision_tree_learning( new_train_data, new_train_labels, used_words, i_nodes+1, max_nodes )
                if value:
                    new_node.add_yes_child( child_node )
                else:
                    new_node.add_no_child( child_node )
        return new_node   


# Returns the most common occuring document type in a list of labels:
def plurality_value( labels ):
    p = labels.count('1')
    n = len(labels) - p

    if p > n:
        return '1'
    else:
        return '2'


# scans the label list to see if they're all the same classification
def all_examples_same( labels ):
    for label in labels:
        if label != labels[0]:
            return False
    return True

# returns the entropy of a boolean random variable that is true with the probability q
def entropy(q):
    if q == 0 or q == 1:
        return 0
    entropy = -1* (q * math.log(q,2) + (1-q) * math.log(1-q, 2) ) 
    return entropy


# returns the information gain based on the method described in Russell Norvig, pg 704
def information_gain( word_index, train_data_sparse, labels ):
    p = labels.count('2')
    n = len( labels ) - p 
    H = entropy( float(p) / (p+n) )
    remainder = 0
    for value in [0,1]:
        pk = 0
        for i in range(len(labels)):
            if labels[i] == '2' and train_data_sparse[i][word_index] == value:
                pk = pk+1 
        nk = len( labels ) - p
        remainder = remainder + (float(pk)+nk)/(p+n) * entropy( float(pk)/ (pk+nk) )   
    gain = H - remainder
    return gain 

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
            digits = [int(x) for x in line.split()] 
            train_data.append( digits )

    train_labels = []
    with open('trainLabel.txt', 'r') as f:
        for line in f:
            train_labels.append( line.split()[0] )
    print "No. of training documents:", len(train_labels) 
    
    test_data = []
    with open('testData.txt', 'r') as f:
        for line in f:
            test_data.append( line.split() )
    
    test_labels = []
    with open('testLabel.txt', 'r') as f:
        for line in f:
            test_labels.append( line.split()[0] )
    print "No. of test documents:", len(test_labels) 
      
    return [words, train_data, train_labels, test_data, test_labels]

if __name__ == "__main__":
    main()
