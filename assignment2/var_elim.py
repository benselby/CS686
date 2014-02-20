#! /usr/bin/python

# Variable elimination algorithm for Bayesian networks

def restrict(factor, variable, value):
    restricted_factor = {}

    # build the target string for matching against the factor entries
    if value:
        target = '+' + variable
    else:
        target = '~' + variable

    # create a subset of the relevant entries
    for entry in factor.keys():
       #if value:
       #     if target in entry and not_target not in entry:
       #         #print "%s is in %s" %(target, entry)
       #         new_entry = entry.replace(target, '')
       #         restricted_factor[new_entry] = factor[entry]
       # else:
       #     if not_target in entry:
       #         #print "%s is in %s" %(not_target, entry)         
       #         new_entry = entry.replace(not_target, '')
       #         restricted_factor[new_entry] = factor[entry]
        if target in entry:
            new_entry = entry.replace(target,'')
            restricted_factor[new_entry] = factor[entry]


    return restricted_factor

def multiply(factor1, factor2):
    product_factor = {}
    # first, find all the common variables between the two factors:
    f1_vars = factor1.keys()[0].replace('~','').replace('+','')
    f2_vars = factor2.keys()[0].replace('~','').replace('+','')
    common_vars = []
    f1 = []
    f2 = []
    for char in f1_vars:
        if char in f2_vars:
            common_vars.append(char)
        else:
            f1.append(char)

    for char in f2_vars:
        if char not in f1_vars:
            f2.append(char)
    all_vars = f1+common_vars+f2
    num_vars = len(all_vars)

    entries = []

    for val in range(2**num_vars):
        new_entry = ''
        for i in range(num_vars):
            if (val >> i) % 2 == 0:
                new_entry = new_entry + '+' + all_vars[i] 
            else:
                new_entry = new_entry + '~' + all_vars[i] 

        entries.append(new_entry)

    print entries

    for entry in entries:
        key1 = entry[:2*len(f1)+2*len(common_vars)]
        key2 = entry[2*len(f1):]
        value1 = factor1[key1]
        value2 = factor2[key2]
        product = value1 * value2
        product_factor[entry] = product
    
    print product_factor
    return product_factor

def sum_out(factor, variable):
    result_factor = {}

    for entry in factor.keys():
        new_entry = entry.replace('~'+variable, '').replace('+'+variable, '')
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
    """ See page 528 for a guideline """
    pass

