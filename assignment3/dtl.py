#!/usr/bin/python

# A decision tree program for classification of newsgroup postings
#
# Ben Selby, March 2014

import math

i_nodes = 1

class Node:

    def __init__( self, value ):
        self.value = value
        self.yes_child = None
        self.no_child = None

    def add_yes_child( self, yes_node ):
        self.yes_child = yes_node 

    def add_no_child( self, no_node ):
        self.no_child = no_node 
    
    def is_leaf(self):
        if type(self.value) is str:
            return True
        else:
            return False

def main():
    # First load all the training and test data and labels
    [words, train_data, train_labels, test_data, test_labels] = load_data_and_labels()
    
    train_data_sparse = sparsify( words, train_data, train_labels )
    test_data_sparse = sparsify( words, test_data, test_labels )
    # Build a decision tree using information gain:
    max_nodes = 100
    used_words = []
    tree = decision_tree_learning( train_data_sparse, train_labels, used_words, max_nodes  )
    print "Training percent correct:", test_decision_tree( tree, train_data_sparse, train_labels )
    print "Test percent correct:", test_decision_tree( tree, test_data_sparse, test_labels )

    # Build a decision tree using info gain times number of documents at each leaf
#   tree2 = decision_tree_learning2( train_data_sparse, train_labels )

    # Test each tree against the test datasets and print the results:

# returns the accuracy (% of documents correctly classified) of a tree given
# some data and labes
def test_decision_tree(tree, sparse_data, labels):
    # classify every document in data using the tree:
    classifications = []
    for doc in sparse_data:
        classifications.append( classify( tree, doc ) )
    correct = 0
    for i in range( len( labels )):
        if labels[i] == classifications[i]:
            correct = correct+1
    return float(correct) / len (labels)    
    
def classify( root, doc ):
    node = root
    while not node.is_leaf():
        # check if the word is in the document
        if doc[node.value] == 1: 
            node = node.yes_child
        else:
            node = node.no_child

    return node.value


def dtl_iterative( sparse_data, labels, max_nodes ):
    n_node = 0
    n_words = len(sparse_data[0])
    tree = Tree()
    used_words = []
    while n_node < max_nodes:
        # get the best word to add to the tree via information gain:
        info_list = []
        for word_index in range(n_words):
            if word_index in used_words: 
                gain = information_gain( word_index, spare_data, labels )
                info_list.append( gain )

        

# A recursive priority queue implementation of DTL - uses information gain
# to rank the attributes 
# Returns an ordered list of decisions based on the provided training data
def decision_tree_learning( train_data_sparse, train_labels, used_words, max_nodes ):
    global i_nodes
    print "Adding node %d of %d" %( i_nodes, max_nodes)
    # check to see if we've hit the maximum number of nodes:
    if i_nodes >= max_nodes:
        return Node( plurality_value( train_labels) ) 
    if all_labels_same( train_labels ):
        return Node( train_labels[0] )

    else:
        # we are going to add a node, so increment the node count:
        i_nodes = i_nodes+1
        
        # rank all the words by importance:
        importance_list = []
        for word_index in range(len(train_data_sparse[0])):
            if word_index not in used_words:
                importance_list.append( information_gain( word_index, train_data_sparse, train_labels ) )
        #for k in range(10):
        #    print importance_list[k]
        #print len(importance_list)
        best_word_index = importance_list.index( max( importance_list ) )
        print "Best word:", best_word_index
        used_words.append( best_word_index )
        new_node = Node( best_word_index )
        for value in [0,1]:
            # divide the training set documents based on whether they contain the word
            new_train_data = []
            new_train_labels = []
            for i in range(len(train_data_sparse)):
                doc = train_data_sparse[i]

                # check to see if the selected word is in the document
                if doc[best_word_index] == value:
                    new_train_data.append( doc )
                    new_train_labels.append( train_labels[i] )
            
            child_node = decision_tree_learning( new_train_data, new_train_labels, used_words, max_nodes )
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
def all_labels_same( labels ):
    for label in labels:
        if label != labels[0]:
            return False
    return True

# returns the entropy of a boolean random variable that is true with the probability q
# q must be a floating point value
def entropy(q):
    if q == 0 or q == 1:
        return 0
    entropy = -1* (q * math.log(q,2) + (1-q) * math.log(1-q, 2) ) 
    return entropy


def information_gain( word_index, train_data_sparse, labels ):
    
    p = labels.count('2')
    n = len(labels) - p
    H = entropy( float(p) / (p+n) )
    
    remainder = 0   
    for value in [0,1]:
        pk = 0
        nk = 0

        for doc in range(len(train_data_sparse)):
            if train_data_sparse[doc][word_index] == value:
                if labels[doc] == '2':
                    pk = pk+1
                else:
                    nk = nk+1
        # check to see if any of the documents contained the word value 
        if pk+nk != 0:
            remainder = remainder + (float(pk+nk) / (p+n)) * entropy( float(pk)/ (pk+nk) )
        else:
            remainder = remainder + 0 
    return H - remainder


# returns the information gain based on the method described in Russell Norvig, pg 704
def information_gain_shit( word_index, train_data_sparse, labels ):
    
    # count the number of documents the word occurs and does not occur in:
    p_indices = []
    n_indices = []
    for i in range(len(train_data_sparse)):
        if train_data_sparse[i][word_index]:
            p_indices.append(i)
        else:
            n_indices.append(i)
    p = len(p_indices)
    n = len(n_indices)
    H = entropy( float(p) / (p+n) )
    
    remainder = 0
    pk = 0
    nk = 0
    for i in p_indices:
        if labels[i] == '1':
            pk = pk + 1
        else:
            nk = nk + 1
    remainder = remainder + (float(pk+nk) / (p+n)) * entropy( float(pk)/ (pk+nk) )   
    
    for i in n_indices:
        if labels[i] == '1':                                                          
            pk = pk + 1
        else:
            nk = nk + 1
    remainder = remainder + (float(pk+nk) / (p+n)) * entropy( float(pk)/ (pk+nk) )   
   
    #p = labels.count('2')
    #n = len( labels ) - p 
    #H = entropy( float(p) / (p+n) )
    #remainder = 0

    #for value in [0,1]:
    #    pk = 0
    #    nk = 0
    #    for i in range(len(labels)):
    #        # check to see if each doc contains the word value
    #        if train_data_sparse[i][word_index] == value:
    #            if labels[i] == '1':
    #                nk = nk+1
    #            else:
    #                pk = pk+1
    #    print word_index,p, n, pk, nk 
    #    remainder = remainder + (float(pk+nk) / (p+n)) * entropy( float(pk)/ (pk+nk) )   
    
    gain = H - remainder
    return gain 

def info_gain_times_doc( word_index, train_data_sparse, labels ):
    pass

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
            digits = [int(x) for x in line.split()]
            test_data.append( digits )
    
    test_labels = []
    with open('testLabel.txt', 'r') as f:
        for line in f:
            test_labels.append( line.split()[0] )
    print "No. of test documents:", len(test_labels) 
      
    return [words, train_data, train_labels, test_data, test_labels]

def sparsify( words, data, labels ):
    # Pre-allocate sparse matrix                                              
    data_sparse = [ [0] * len(words) for i in range( len(labels) ) ] 
                                                                                 
    # arrange the data into sparse matrices for easier processing                
    for i in data:                                                         
        data_sparse[ i[0]-1 ][ i[1]-1 ] = 1                                
    
    return data_sparse

if __name__ == "__main__":
    main()
