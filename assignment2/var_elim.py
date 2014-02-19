#! /usr/bin/python

# Variable elimination algorithm for Bayesian networks

def restrict(factor, variable, value):
    restricted_factor = {}

    # build the target string for matching against the factor entries
    target = variable
    not_target = '~'+ variable

    # create a subset of the relevant entries
    for entry in factor.keys():
        print entry
        if value:
            if target in entry and not_target not in entry:
                #print "%s is in %s" %(target, entry)
                new_entry = entry.replace(target, '')
                restricted_factor[new_entry] = factor[entry]
        else:
            if not_target in entry:
                #print "%s is in %s" %(target, entry)         
                new_entry = entry.replace(not_target, '')
                restricted_factor[new_entry] = factor[entry]

    return restricted_factor

def multiply(factor1, factor2):
    product_factor = {}
    # first, find all the common variables between the two factors:
    f1_vars = factor1.keys()[0].replace('~','')
    f2_vars = factor2.keys()[0].replace('~','')
    common_vars = []
    for char in f1_vars:
        if char in f2_vars:
            common_vars.append(char)

    for 
    return product_factor

def sum_out(factor, variable):
    result_factor = {}

    for entry in factor.keys():
        tmp = entry.replace('~'+variable, '')
        new_entry = tmp.replace(variable, '')
        print "new entry:", new_entry 
        if new_entry not in result_factor:
            result_factor[new_entry] = factor[entry]
        else:
            result_factor[new_entry] = result_factor[new_entry] + factor[entry]
    
    return result_factor

def normalize(factor):
    total_sum = 0
    normalized_factor = {}

    for entry in factor.keys():
        total_sum = total_sum + factor[entry]
    
    for entry in factor.keys():
        normalized_factor[entry] = factor[entry]/total_sum
    
    return normalized_factor

def inference(factor_list, query_vars, hidden_vars, evidence_list):
    pass



#class Factor:():
#
#    def __init__():
#        pass

    
