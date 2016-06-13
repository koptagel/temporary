# %load distance.py

import numpy as np

def main():
    print('Function Prototypes: ')
    
    print('dist = distance(P, Q, div)')
    print('Divergence metric can be one of the following: \'euc\', \'kl\', \'is\' or \'hel\'')
    print('Example Usage:')
    print('dist = distance(P,Q,div=\'euc\')')  
          
    print('\nInstructions')
    print('In order to view the code, type: %load distance.py')
    print('In order to modify the code, to the first line of the cell add: %%writefile distance.py')
    print('Note that after modifying the code, you should run the cell again: %run distance.py')

if __name__ == "__main__": main()

def distance(P, Q, div='euc'):
    '''
    This function calculates the divergence between 2 matrices given the scalar divergence as a string.
    div must be one of the following: 
        'euc' for calculating Euclidean Distance. EUC(P,Q) = (1/2) * (P-Q) * (P-Q)
        'kl' for calculating Kullback-Leibler Divergence. KL(P,Q) = P * log(P/Q) - P + Q
        'is' for calculating Itakura-Saito Distance. IS(P,Q) = (P/Q) * log(P/Q) - 1
        'hel' for calculating Hellinger Distance. H(P,Q) = (1/sqrt(2)) * sqrt((sqrt(P) - sqrt(Q))*(sqrt(P) - sqrt(Q)))
    '''
    eps = 0.000001
    P = P + eps
    Q = Q + eps
    
    if div is 'kl':
        dist = np.sum( P * np.log(P/Q) - P + Q )
    elif div is 'is':
        dist = np.sum( P/Q - np.log(P/Q) - 1 )
    elif div is 'hel':
        dist = (1/np.sqrt(2)) * np.sqrt( np.sum( np.power(( np.sqrt(P) - np.sqrt(Q)), 2) )) 
    elif div is 'man':
        dist = np.sum( np.abs(P-Q) )
    elif div is 'ham':
        dist = 0 
        for i in range(len(P)):
            if P[i] != Q[i]:
                dist = dist + 1
    else: # 'euc'
        dist = np.sum( (1/2) * np.power((P-Q),2) )
        
    return dist