
import numpy as np
from scipy.sparse import *

def loadMatrixFromTxt(filename):
    row = []
    col = []
    data = []

    for line in open(filename, "r"):
        values = line.split()

        item = int(values[3])
        customer = int(values[4])
        amount = float(values[5])

        row.append(customer)
        col.append(item)
        data.append(amount)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)

    PurchaseMatrix = csr_matrix( (data,(row,col)), shape=(max(row)+1,max(col)+1) )

    return PurchaseMatrix


def loadRecommendationMatrixFromTxt(filename):
    row = []
    col = []
    data = []

    for line in open(filename, "r"):
        values = line.split()

        customer = int(values[0])
        item = int(values[1])
        amount = float(values[2])

        row.append(customer)
        col.append(item)
        data.append(amount)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)

    PurchaseMatrixEst = csr_matrix( (data,(row,col)), shape=(max(row)+1,max(col)+1) )

    return PurchaseMatrixEst

def loadRecommendationOfCustomerMatrixFromTxt(filename, customerIndex):
    row = []
    col = []
    data = []

    for line in open(filename, "r"):
        values = line.split()

        customer = int(values[0])
        if customer == customerIndex:
            item = int(values[1])
            amount = float(values[2])

            row.append(customer)
            col.append(item)
            data.append(amount)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)

    PurchaseMatrixEst = csr_matrix( (data,(row,col)), shape=(max(row)+1,max(col)+1) )

    return PurchaseMatrixEst

def loadItemIdAndDsFromTxt(name):
    filename = "%s_Items.txt" % (name)
    
    itemids = []
    for line in open(filename, "r"):
        values = line.split()

        itemId = int(values[0])
        itemids.append(itemId)    
    itemids = np.array(itemids)


    filename = "%s_ItemsDs.txt" % (name)
    itemdss = []
    for line in open(filename, "r"):
        itemDs = line
        itemdss.append(itemDs) 
    itemdss = np.array(itemdss)

    return itemids, itemdss


def loadCustomerIdFromTxt(name):
    filename = "%s_Customers.txt" % (name)
    
    custids = []
    for line in open(filename, "r"):
        values = line.split()

        custId = int(values[0])
        custids.append(custId)    
    custids = np.array(custids)
    
    return custids