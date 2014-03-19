#!/usr/bin/python

# A decision tree program for classification of newsgroup postings
#
# Ben Selby, March 2014

import math
import csv

i_nodes = 1

class Node:
    # value can be either a label (a string) for a leaf, or a word index
    # docs contains a list of all documents remaining at that node
    # labels is a list of classifications corresponding to the list of docs
    def __init__( self, value ):
        self.value = value
        self.yes_child = None
        self.no_child = None
        self.docs = []
        self.labels = []
        self.best_word_index = None
        self.info_gain = None

    def add_docs_and_labels(self, docs, labels):
        if len(docs) == len(labels):
            self.docs = docs
            self.labels = labels
        else:
            print "Labels don't match documents, abort!"
            return -1

    def add_yes_child( self, yes_node ):
        self.yes_child = yes_node 

    def add_no_child( self, no_node ):
        self.no_child = no_node 
    
    def get_leaves(self):
        leaves = []
        if self.is_leaf():
            leaves.append(self)
        else:
            [leaves.append(leaf) for leaf in self.yes_child.get_leaves() ]
            [leaves.append(leaf) for leaf in self.no_child.get_leaves() ]
        
        return leaves

    def is_leaf(self):
        if type(self.value) is str:
            return True
        else:
            return False
    
    def print_tree(self, prefix, words):
        if type(self.value) is str:
            print prefix, self.value
        else:
            print prefix, words[self.value]
        print "Info Gain:", self.info_gain 
        if self.yes_child and self.no_child:
            self.yes_child.print_tree('%s yes child:'%words[self.value], words)
            self.no_child.print_tree('%s no child:'%words[self.value], words)


def main():
    # First load all the training and test data and labels
    [words, train_data, train_labels, test_data, test_labels] = load_data_and_labels()
    
    train_data_sparse = sparsify( words, train_data, train_labels )
    test_data_sparse = sparsify( words, test_data, test_labels )
    # Build a decision tree using information gain:
    max_nodes = 10
    used_words = []

    tree = dtl_iterative(train_data_sparse, train_labels, max_nodes, test_data_sparse, test_labels, words )
    print "Final training percent correct:", test_decision_tree( tree, train_data_sparse, train_labels )
    print "Final test percent correct:", test_decision_tree( tree, test_data_sparse, test_labels )
    tree.print_tree('', words)
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

# Implements an iterative priority queue DTL algorithm
def dtl_iterative(sparse_data, labels, max_nodes, test_data, test_labels, words):
    # first, get the root node:
    info_list = []
    for word_index in range(len(sparse_data[0])):
        info_list.append( information_gain( word_index, sparse_data, labels ) )
    
    best_word = info_list.index( max(info_list) )
     
    root = Node(best_word)
    print "Selected word:", words[best_word]
    print "info gain:", max(info_list)
    
    yes_docs = []
    yes_labels = []
    no_docs = []
    no_labels = []
    for i in range(len(sparse_data)):
        label = labels[i]
        doc = sparse_data[i]
        if doc[best_word]:
            yes_docs.append(doc)
            yes_labels.append(label)
        else:
            no_docs.append(doc)
            no_labels.append(label)

    root.add_no_child( Node(path_plurality_value(best_word, no_docs, no_labels, 0)) )
    root.add_yes_child( Node(path_plurality_value(best_word, yes_docs, yes_labels, 1)) )
    
    root.yes_child.add_docs_and_labels( yes_docs, yes_labels )
    root.no_child.add_docs_and_labels( no_docs, no_labels )
    root.info_gain = max(info_list)
    n_nodes = 1
    test_percent = []
    train_percent = []
    while n_nodes < max_nodes:
        print "testing with %d nodes... " % n_nodes
        test_percent.append(test_decision_tree(root, test_data, test_labels))
        train_percent.append(test_decision_tree(root, sparse_data, labels))
        print "classified %f percent training documents correctly" % train_percent[n_nodes-1]
        print "classified %f percent training documents correctly" % test_percent[n_nodes-1]
        print "adding node %d of %d" % (n_nodes+1, max_nodes)       
        
        leaves = root.get_leaves()
        for leaf in leaves:
            # check if we've already calculated the gain for the leaf
            if leaf.info_gain == None:
                # find the best word at each leaf by calculating the gain for 
                # all words and then take the max
                info_list = []
                for i in range(len(sparse_data[0])):
                    # find the information gain or info gain times number of documents for each leaf
                    info_list.append( information_gain( i, leaf.docs, leaf.labels )*len(leaf.docs) )
                    #info_list.append( information_gain( i, leaf.docs, leaf.labels ) )
                leaf.info_gain = max(info_list) 
                leaf.best_word_index = info_list.index( max(info_list) )
        leaves_gain = [leaf.info_gain for leaf in leaves]
        # find the best leaf based on the info gain
        best_leaf = leaves[leaves_gain.index( max(leaves_gain) )]
        # expand the best leaf 
        best_leaf.value = best_leaf.best_word_index
        
        print "Selected word:", words[best_leaf.value]
        print "info gain:", best_leaf.info_gain
        

        yes_docs = []
        yes_labels = []
        no_docs = []
        no_labels = []
        for i in range(len(best_leaf.docs)):
            label = best_leaf.labels[i]
            doc = best_leaf.docs[i]
            if doc[best_leaf.best_word_index]:
                yes_docs.append(doc)
                yes_labels.append(label)
            else:
                no_docs.append(doc)
                no_labels.append(label)
        
        best_leaf.add_no_child( Node(path_plurality_value(best_leaf.best_word_index, best_leaf.docs, best_leaf.labels, 0) ))
        best_leaf.add_yes_child( Node(path_plurality_value(best_leaf.best_word_index, best_leaf.docs, best_leaf.labels, 1) ))
        
        best_leaf.yes_child.add_docs_and_labels( yes_docs, yes_labels )
        best_leaf.no_child.add_docs_and_labels( no_docs, no_labels )
        n_nodes = n_nodes+1
    # write the percentages correct to a .csv
   # with open('results_times_docs.csv', 'wb') as f:
   #     writer = csv.writer(f)
   #     writer.writerows([train_percent])
   #     writer.writerows([test_percent])
    
    return root

def path_plurality_value(word_index, sparse_data, labels, value):
    count1 = 0
    count2 = 0
    for i in range(len(sparse_data)):
        if sparse_data[i][word_index] == value:
            if labels[i] == '1':
                count1 = count1+1
            else:
                count2 = count2+1
    if count1 > count2:
        return '1'
    else:
        return '2'
    
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
    # if there are no documents left over, return 0 (nothing left to gain)
    if p+n == 0:
        return 0.0
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

# returns the information gain times the number of documents at the leaves
def info_gain_times_doc( word_index, train_data_sparse, labels ):
    gain = information_gain( word_index, train_data_sparse, labels)
    n_docs = 0

    return ndocs * gain

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
