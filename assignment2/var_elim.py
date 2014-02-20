#! /usr/bin/python

# Variable elimination algorithm for Bayesian networks

def restrict(factor, variable):
    restricted_factor = {}
    
    print "Restricting %s to %s..." % (factor, variable)

    for entry in factor.keys():
        if variable in entry:
            new_entry = entry.replace(variable,'')
            restricted_factor[new_entry] = factor[entry]
    if restricted_factor:
        print "Restricted factor: %s\n" % restricted_factor
        return restricted_factor
    else:
        print "Could not restrict factor to", variable
        return factor

def multiply(factor1, factor2):
    product_factor = {}
    
    print "Finding the pointwise product of factors:\n%s\nand\n%s" % (factor1, factor2)

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

    #print entries

    for entry in entries:
        key1 = entry[:2*len(f1)+2*len(common_vars)]
        key2 = entry[2*len(f1):]
        value1 = get_value(factor1, key1)
        value2 = get_value(factor2, key2) 
        product = value1 * value2
        product_factor[entry] = product
    
    print "Product:%s\n" % product_factor
    return product_factor

""" A function to find a value given the variables of the factor out of order """
def get_value(factor, key):
    # first, split the key into indivdual variable values
    var_list = [ key[2*i:2*i+2] for i in range(len(key)/2) ]

    # make a copy of the factor:
    f = dict(factor)
    
    # Delete all the factor entries but the right one
    for v in var_list:
        for k in f.keys():
            if v not in k:
                del f[k]

    # get the only remaining value
    value = f[ f.keys()[0] ]
    return value

def sum_out(factor, variable):
    result_factor = {}
    print "Summing variable %s out of factor %s..." % (variable, factor)
    for entry in factor.keys():
        new_entry = entry.replace('~'+variable, '').replace('+'+variable, '')
        if new_entry not in result_factor:
            result_factor[new_entry] = factor[entry]
        else:
            result_factor[new_entry] = result_factor[new_entry] + factor[entry]
    print "Result: %s\n" % result_factor
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
    print "Calculating Pr(%s|%s) using variable elimination..." % (query_vars, evidence_list)
    
    # First restrict the factors according to the evidence:
    restricted_factors = []
    for factor in factor_list:
        new_factor = factor
        for e in evidence_list:
            new_factor = restrict(new_factor, e)
        if new_factor:
            restricted_factors.append(new_factor)
    
    # find the product of all the factors:
    product = restricted_factors[0]
    index = [x+1 for x in range(len(restricted_factors)-1)]
    for i in index:
        product = multiply( product, restricted_factors[i] )
    
    # finally, sum out the hidden variables:
    result_factor = product
    for var in hidden_vars:
        result_factor = sum_out(result_factor, var)
    
    print "Unnormalized factor:"
    print result_factor

    return normalize(result_factor)
    
def main():
    """ Run some test cases here: """ 
    order = ['T', 'f', 'F', 'I', 'O', 'C']
    factor_list = [ {'+T':0.05, '~T':0.95 },
                    {'+f+T+F':0.9, '+f+T~F':0.9, '+f~T+F':0.1, '+f~T~F':0.01, '~f+T+F':0.1, '~f+T~F':0.1, '~f~T+F':0.9, '~f~T~F':0.99},
                    {'+F+T':0.01, '+F~T':0.004, '~F+T':0.99, '~F~T':0.996},
                    {'+I~F~O':0.001, '+I~F+O':0.01, '+I+F~O':0.011, '+I+F+O':0.02, '~I~F~O':0.999, '~I~F+O':0.99, '~I+F~O':0.989, '~I+F+O':0.98},
                    {'+O':0.7, '~O':0.3},
                    {'+C+O':0.1, '+C~O':0.001, '~C+O':0.99, '~C~O':0.999} ]
    print "P(F) given no evidence (prior probability):"
    query = 'F'
    evidence = []
    hidden_vars = list(order)
    hidden_vars.remove(query)
    print inference(factor_list, query, hidden_vars , evidence)

    print ''
    print "P(F|f,~I,C) given no evidence (prior probability):"
    query = 'F'
    evidence = ['+f', '~I', '+C']
    hidden_vars = ['T', 'O']
    print inference(factor_list, query, hidden_vars , evidence)
    
if __name__ == "__main__":
    main()
