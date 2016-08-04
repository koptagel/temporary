# %load collapseTensor.py

import numpy as np

def main():
    print('Function Prototypes: ')
          
    print('newTensor = collapseTensor(tensor, dimensions, function)')
    print('Tensor must have 5 dimensions, corresponding Week,DoW,Hour,Items,Customers respectively')
    print('Indicate dimensions you want to sum over with 1, 0 otherwise')
    print('Function must be one of the following: \'sum\', \'binary\', \'count\'')
    print('Example Usage:')
    print('newTensor = collapseTensor(X, [0,0,1,1,0], \'sum\')')  
          
    print('\nInstructions')
    print('In order to view the code, type: %load collapseTensor.py')
    print('In order to modify the code, to the first line of the cell add: %%writefile collapseTensor.py')
    print('Note that after modifying the code, you should run the cell again: %run collapseTensor.py')

if __name__ == "__main__": main()
    

def collapseTensor(tensor, dimensions, function):
    '''
    Given the tensor, dimensions to be collapsed over and the function applied during collapsing,
    this function generates new tensor and keeps the dimensions.
    
    Inputs: tensor
            dimensions: an array in the form of an binary array
            function: a string whose value must be one of the following: 'sum', 'binary' or 'count'
                      'sum' sums the tensor over the given dimensions.
                      'binary' generates a tensor with values 0 or 1.
                      'count' sums up the number of occurences in the tensor.
                      
    Example: newTensor = collapseTensor(tensor, [1,0,1,0], 'sum')
             shape of tensor:    (2 x 3 x 4 x 5) 
             shape of newTensor: (1 x 3 x 1 x 5)
    '''
    
    dimensions = np.array(dimensions)
    
    if dimensions.shape[0] > len(tensor.shape):
        print('Invalid Parameter: Dimensions exceed the tensor size')
        return tensor
    
    indices = np.where(dimensions>0)[0]  
    
    for i in range(len(indices)):
        ax = indices[i]       
        
        if function is 'binary':
            tensor = np.sum(tensor, axis=ax, keepdims=True)
            tensor[np.where(tensor>0)]=1
        elif function is 'count':
            tensor[np.where(tensor>0)]=1
            tensor = np.sum(tensor, axis=ax, keepdims=True)
        else: # 'sum'
            tensor = np.sum(tensor, axis=ax, keepdims=True)

    return tensor

def collapseSlotTensor(tensor, ax1, ax2, timePoints, timePointsY, function):
    dimensions = np.array([1,1,1,1,1])
    if ax1==6:
        dimensions[2] = 0
        dimensions[ax2] = 0
    if ax2==6: 
        dimensions[ax1] = 0
        dimensions[2] = 0
    
    indices = np.where(dimensions>0)[0]  
    
    for i in range(len(indices)):
        ax = indices[len(indices)-i-1]  
        tensor = np.sum(tensor, axis=ax, keepdims=False)

    if ax1==3 or ax2==3:
        tensor = tensor.T
        
    newMatrix = np.zeros((tensor.shape[0],1))
    
    for i in range(len(timePoints)):
        asd = tensor[:,timePoints[i]:timePointsY[i]]
        aaa = np.sum(asd,axis=1,keepdims=True)
        newMatrix = np.hstack((newMatrix,aaa))

    if ax1 > ax2:
        newMatrix = newMatrix.T
        
    if ax1==6:    
        newMatrix = newMatrix[1:,:]  
    if ax2==6:    
        newMatrix = newMatrix[:,1:]
     
    if function is 'binary':
        newMatrix[np.where(newMatrix>0)]=1
        
    return newMatrix