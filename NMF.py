
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline


# Nonnegative Matrix Factorization: V ~ VHat = AB
# Inputs: V = s1 x s2 matrix, maxIter, rank
# Outputs: VHat = s1 x s2 matrix, errors = maxIter x 1 array, B = rank x s2 matrix
def nmf(V, maxIter, rank):
    eps = 1e-8
    errors = np.zeros((maxIter,1))

    s1, s2 = V.shape
    A = np.random.rand(s1,rank)
    B = np.random.rand(rank,s2)

    O = np.ones((s1,s2))

    for i in range(maxIter):
        VHat = np.dot(A,B) 
        VHat = VHat + eps

        # errors[i] = sum(sum( np.multiply(V,np.log(V)) - np.multiply(V,np.log(VHat)) - V + VHat ))
        errors[i] = sum(sum(np.multiply(V,np.log(VHat)) - VHat ))
        #print(errors[i])

        A = np.multiply(A, (np.dot((V/VHat), B.transpose() ) / (np.dot(O,B.transpose()))))
        
        #sA = np.sum(A, axis=0, keepdims=True)
        #A = A/sA
        #B = B*sA.transpose()

        VHat = np.dot(A,B) 
        VHat = VHat + eps

        B = np.multiply(B, (np.dot(A.transpose(), (V/VHat))) / (np.dot(A.transpose(),O)))  

    VHat = np.dot(A,B) 
    VHat = VHat + eps
    
    indices = np.argsort(A,axis=0)[::-1].flatten()
    
    tempA = A + np.ones((s1,rank))
    sortedA = np.sort(tempA,axis=0)[::-1].flatten()
    
    percentages = sortedA * 100 / np.max(tempA)
    
    return (VHat, errors, B, A, indices, percentages)


def nmfFixBasis(V,B, maxIter, rank):
    eps = 1e-8
    errors = np.zeros((maxIter,1))

    s1, s2 = V.shape
    A = 10*np.random.rand(s1,rank)
    #B = 100*np.random.rand(rank,s2)

    O = np.ones((s1,s2))

    for i in range(maxIter):
        VHat = np.dot(A,B) 
        VHat = VHat + eps

        # errors[i] = sum(sum( np.multiply(V,np.log(V)) - np.multiply(V,np.log(VHat)) - V + VHat ))
        errors[i] = sum(sum(np.multiply(V,np.log(VHat)) - VHat ))
        #print(errors[i])

        A = np.multiply(A, (np.dot((V/VHat), B.transpose() ) / (np.dot(O,B.transpose()))))
        
        #sA = np.sum(A, axis=0, keepdims=True)
        #A = A/sA
        #B = B*sA.transpose()

        VHat = np.dot(A,B) 
        VHat = VHat + eps

        #B = np.multiply(B, (np.dot(A.transpose(), (V/VHat))) / (np.dot(A.transpose(),O)))  

    VHat = np.dot(A,B) 
    VHat = VHat + eps
    
    indices = np.argsort(A,axis=0)[::-1].flatten()
    
    tempA = A + np.ones((s1,rank))
    sortedA = np.sort(tempA,axis=0)[::-1].flatten()
    
    percentages = sortedA * 100 / np.max(tempA)
    
    return (VHat, errors, B, A, indices, percentages)