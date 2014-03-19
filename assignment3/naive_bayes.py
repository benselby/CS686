#! /usr/bin/python

# A naive bayes learning algorithm for document classification
#
# Ben Selby, March 2014

import math
import dtl

def main():
    [words, train_data, train_labels, test_data, test_labels] = dtl.load_data_and_labels()
    sparse_data = dtl.sparsify(words, train_data, train_labels)
    sparse_test = dtl.sparsify(words, test_data, test_labels)

    net = build_bayes_net( sparse_data, train_labels, words )
    #print "Training set performance: %f\%", test_bayes_classifier( net, sparse_data, train_labels)    
    #print "Test set performance: %f\%", test_bayes_classifier( net, sparse_test, test_labels)    


def build_bayes_net(sparse_data, labels, words ):
    
    # split the training set into two based on labels:
    docs1 = []
    docs2 = []
    for i in range(len(labels)):
        if labels[i] == '1':
            docs1.append(sparse_data[i])
        else:
            docs2.append(sparse_data[i])

    # calculate the likelihood of each word given the label:
    word_likelihood1 = [0] * len(sparse_data[0])
    word_likelihood2 = [0] * len(sparse_data[0])
    
    for word in range(len(sparse_data[0])):
        # Laplacian smoothing - start the word count at 1
        count = 1 
        for i in range(len(docs1)):
            count = count + docs1[i][word]
        word_likelihood1[word] = float(count)/len(docs1)

        count = 1
        for i in range(len(docs2)):
            count = count + docs2[i][word]
        word_likelihood2[word] = float(count)/len(docs2)

    log_likelihood = [0]*len(sparse_data[0])
    
    for i in range(len(log_likelihood)):
        log_likelihood[i] = abs( math.log(word_likelihood1[i]) - math.log(word_likelihood2[i]) )
    
    # make a copy that can be butchered:
    ll_list = list(log_likelihood)
    for i in range(10):
        best_l = max(ll_list)
        best_word = ll_list.index(best_l)
        print "Word:", words[best_word]
        print "log likelihood:", best_l
        ll_list[best_word] = 0 
    
    return log_likelihood


# returns the percentage of documents correctly classified by the naive bayes
# net defined by 'net'. In this case, net is 
def test_bayes_classifier( net, sparse_data, labels  ):
    classifications = [0] * len(labels)
    for i in range(len(classifications)):
        classifications[i] = classify( net, sparse_data[i] )
        if classifications[i] == labels[i]:
            correct = correct + 1
    
    return float(correct)/len(labels)


def classify ( net, document ):
    h1 = 1
    h2 = 1
    for i in range(len(document)):
        h1 = h1*document[i]*net[0][i]
        h2 = h2*document[i]*net[1][i]

    if h1 > h2:
        return '1'
    else:
        return '2'

if __name__ == '__main__':
    main()
