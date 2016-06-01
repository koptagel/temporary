# %load plotTensor.py

import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

def main():
    print('Function Prototypes: ')
          
    print('plotTensor(X, numPlots, title, vmax=300, figsize=(5, 3))')
    print('Tensor must have 5 dimensions, corresponding Week,DoW,Hour,Items,Customers respectively')
    print('Example Usage:')
    print('plotTensor(X, numPlots=5, title=\'Plot of X\', vmax=100)')  
          
    print('\nInstructions')
    print('In order to view the code, type: %load plotTensor.py')
    print('In order to modify the code, to the first line of the cell add: %%writefile plotTensor.py')
    print('Note that after modifying the code, you should run the cell again: %run plotTensor.py')
    print('Also you should type the following code: %matplotlib inline')

if __name__ == "__main__": main()

#def plotTensor(X, numPlots, title, vmax=300, figsize=(5, 3)):          
def plotTensor(X, numPlots, title, figsize=(5, 3)):           
    '''
    Given the tensor X and the maximum number of plots we want to display, 
    this function looks at the dimensions of the tensor and produces the corresponding plots.
    
    Note that this function generates one plot per customer and there is no option for generating subplots. 
    The dimensions of X must be: numWeek, numDay, numHour, numItem, numCustomer.
    '''

                                       # X = 1 x 7 x 16 x 1 x 2500
    dimensions = np.array(X.shape)     # dims = [1,7,16,1,2500]
    
    notCollapsedIndices = np.where(dimensions>1)[0] 
    dimensions[notCollapsedIndices] = 0
    dimensions = dimensions[:-1]       # dims = [1,0,0,1]
    
    #print('Dimensions')
    #print(dimensions)
 
    numCustomers = X.shape[4]
    numPlots = min(numCustomers, numPlots)
    
    # Case 1 - X = numWeek x numDow x 1 x 1 x numCustomers
    if np.array_equal(dimensions,[0,0,1,1]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')

            #plt.imshow(X[:,:,0,0,idx].T, aspect='auto', interpolation='nearest', vmin=0, vmax=vmax)
            plt.imshow(X[:,:,0,0,idx].T, aspect='auto', interpolation='nearest', vmin=0)
            plt.xlabel('Week')
            plt.ylabel('Day of Week')
            plt.yticks(np.arange(7), ['Mo','Tu','We','Th','Fr','Sa','Su'])
            plt.title(title)

            plt.show()
    
    # Case 2 - X = numWeek x 1 x numHours x 1 x numCustomers
    elif np.array_equal(dimensions,[0,1,0,1]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')

            plt.imshow(X[:,0,:,0,idx].T, aspect='auto', interpolation='nearest', vmin=0)
            plt.xlabel('Week')
            plt.ylabel('Hours')
            plt.title(title)

            plt.show()
    
    # Case 3 - X = 1 x numDow x numHours x 1 x numCustomers
    elif np.array_equal(dimensions,[1,0,0,1]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[0,:,:,0,idx].T, aspect='auto', interpolation='nearest', vmin=0)
            plt.ylabel('Hours')
            plt.xlabel('Day of Week')
            plt.xticks(np.arange(7), ['Mo','Tu','We','Th','Fr','Sa','Su'])
            plt.title(title)
            
            plt.show()
    
    # Case 4 - X = numWeek x 1 x 1 x numItems x numCustomers   
    elif np.array_equal(dimensions,[0,1,1,0]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[:,0,0,:,idx].T, aspect='auto', interpolation='nearest', vmin=0)
            plt.ylabel('Items')
            plt.xlabel('Week')
            plt.title(title)
            
            plt.show()
    
    # Case 5 - X = 1 x numDow x 1 x numItems x numCustomers   
    elif np.array_equal(dimensions,[1,0,1,0]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[0,:,0,:,idx].T, aspect='auto', interpolation='nearest', vmin=0)
            plt.ylabel('Items')
            plt.xlabel('Day of Week')
            plt.xticks(np.arange(7), ['Mo','Tu','We','Th','Fr','Sa','Su'])
            plt.title(title)
            
            plt.show()
            
    # Case 6 - X = 1 x 1 x numHours x numItems x numCustomers   
    elif np.array_equal(dimensions,[1,1,0,0]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[0,0,:,:,idx].T, aspect='auto', interpolation='nearest', vmin=0)
            plt.ylabel('Items')
            plt.xlabel('Hours')
            plt.title(title)
            
            plt.show()
            
    else:
        print('Invalid dimensions')
        
#def plotTensorTr(X, numPlots, title, vmax=300, figsize=(5, 3)):      
def plotTensorTr(X, numPlots, title, figsize=(5, 3)):           
    '''
    Given the tensor X and the maximum number of plots we want to display, 
    this function looks at the dimensions of the tensor and produces the corresponding plots.
    
    Note that this function generates one plot per customer and there is no option for generating subplots. 
    The dimensions of X must be: numWeek, numDay, numHour, numItem, numCustomer.
    '''

                                       # X = 1 x 7 x 16 x 1 x 2500
    dimensions = np.array(X.shape)     # dims = [1,7,16,1,2500]
    
    notCollapsedIndices = np.where(dimensions>1)[0] 
    dimensions[notCollapsedIndices] = 0
    dimensions = dimensions[:-1]       # dims = [1,0,0,1]
    
    #print('Dimensions')
    #print(dimensions)
 
    numCustomers = X.shape[4]
    numPlots = min(numCustomers, numPlots)
    
    # Case 1 - X = numWeek x numDow x 1 x 1 x numCustomers
    if np.array_equal(dimensions,[0,0,1,1]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')

            plt.imshow(X[:,:,0,0,idx], aspect='auto', interpolation='nearest', vmin=0)
            plt.ylabel('Week')
            plt.xlabel('Day of Week')
            plt.xticks(np.arange(7), ['Mo','Tu','We','Th','Fr','Sa','Su'])
            plt.title(title)

            plt.show()
    
    # Case 2 - X = numWeek x 1 x numHours x 1 x numCustomers
    elif np.array_equal(dimensions,[0,1,0,1]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')

            plt.imshow(X[:,0,:,0,idx], aspect='auto', interpolation='nearest', vmin=0)
            plt.ylabel('Week')
            plt.xlabel('Hours')
            plt.title(title)

            plt.show()
    
    # Case 3 - X = 1 x numDow x numHours x 1 x numCustomers
    elif np.array_equal(dimensions,[1,0,0,1]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[0,:,:,0,idx], aspect='auto', interpolation='nearest', vmin=0)
            plt.xlabel('Hours')
            plt.ylabel('Day of Week')
            plt.yticks(np.arange(7), ['Mo','Tu','We','Th','Fr','Sa','Su'])
            plt.title(title)
            
            plt.show()
    
    # Case 4 - X = numWeek x 1 x 1 x numItems x numCustomers   
    elif np.array_equal(dimensions,[0,1,1,0]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[:,0,0,:,idx], aspect='auto', interpolation='nearest', vmin=0)
            plt.xlabel('Items')
            plt.ylabel('Week')
            plt.title(title)
            
            plt.show()
    
    # Case 5 - X = 1 x numDow x 1 x numItems x numCustomers   
    elif np.array_equal(dimensions,[1,0,1,0]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[0,:,0,:,idx], aspect='auto', interpolation='nearest', vmin=0)
            plt.xlabel('Items')
            plt.ylabel('Day of Week')
            plt.yticks(np.arange(7), ['Mo','Tu','We','Th','Fr','Sa','Su'])
            plt.title(title)
            
            plt.show()
            
    # Case 6 - X = 1 x 1 x numHours x numItems x numCustomers   
    elif np.array_equal(dimensions,[1,1,0,0]):
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
            
            plt.imshow(X[0,0,:,:,idx], aspect='auto', interpolation='nearest', vmin=0)
            plt.xlabel('Items')
            plt.ylabel('Hours')
            plt.title(title)
            
            plt.show()
            
    else:
        print('Invalid dimensions')
        
def plotBarChart(X, numPlots, title, figsize=(5, 3)):    
    dimensions = np.array(X.shape)     
    
    notCollapsedIndices = np.where(dimensions>1)[0] 
    dimensions[notCollapsedIndices] = 0
    dimensions = dimensions[:-1]      
 
    numCustomers = X.shape[4]
    numPlots = min(numCustomers, numPlots)
    
    # Case 1 - X = numWeek x 1 x 1 x 1 x numCustomers
    if np.array_equal(dimensions,[0,1,1,1]):
        numWeek = X.shape[0]
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
         
            plt.bar(np.arange(numWeek), X[:,0,0,0,idx])
            plt.xlabel('Week')
            plt.title(title)
            plt.show()

    # Case 2 - X = 1 x numDow x 1 x 1 x numCustomers
    elif np.array_equal(dimensions,[1,0,1,1]):
        numDow = X.shape[1]
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
         
            plt.bar(np.arange(numDow), X[0,:,0,0,idx])
            plt.xlabel('Day of Week')
            plt.xticks(np.arange(7), ['Mo','Tu','We','Th','Fr','Sa','Su'])
            plt.title(title)
            plt.show()

    # Case 3 - X = 1 x 1 x numHour x 1 x numCustomers
    elif np.array_equal(dimensions,[1,1,0,1]):
        numHour = X.shape[2]
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
         
            plt.bar(np.arange(numHour), X[0,0,:,0,idx])
            plt.xlabel('Hours')
            plt.title(title)
            plt.show()
    
    # Case 4 - X = 1 x 1 x 1 x numItem x numCustomers
    elif np.array_equal(dimensions,[1,1,1,0]):
        numItem = X.shape[3]
        
        for idx in range(numPlots): 
            fig = plt.figure(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
         
            plt.bar(np.arange(numItem), X[0,0,0,:,idx])
            plt.xlabel('Items')
            plt.title(title)
            plt.show()
    
    else:
        print('Invalid dimensions')