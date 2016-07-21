# %load weblog.py
# %load weblog.py

import matplotlib.pyplot as plt
import requests
import numpy as np
import datetime as dt
import networkx as nx
import scipy.io

def webBrowseMatrix(customerId):
    url =  'http://212.57.2.68:93/api/database/StatisticCart?$select=Carttype,Cartoperationname,Productid,Name,Totalcartitemcount,Statisticdate&$filter=Customerid+eq+%d&$orderby=Statisticdate+asc' % customerId
    r = requests.get(url)
    results = r.json()
    
    cat_url = 'http://212.57.2.68:93/api/database/StatisticCatalog?$select=Catalogtype,Catalogid,Name,Statisticdate&$filter=Customerid+eq+%d&$orderby=Statisticdate+asc' % customerId
    catR = requests.get(cat_url)
    catResults = catR.json()
    
    data = {}
    
    for z in results:
        data2 = {}
        data2['dType'] = "Cart"
        data2['Cartoperationname'] = z['Cartoperationname']
        data2['Productid'] = z['Productid']
        data2['Name'] = z['Name']    
        data2['Totalcartitemcount'] = z['Totalcartitemcount']  
      
        data[z['Statisticdate']] = data2
        
        
    for z in catResults:
        data2 = {}
        data2['dType'] = "Catalog"
        data2['Catalogtype'] = z['Catalogtype']
        data2['Catalogid'] = z['Catalogid']
        data2['Name'] = z['Name'] 
        
        data[z['Statisticdate']] = data2
        
     
    name2ind = {"Login": 0, "Category": 10, "Product": 11, "Logout": 9, "AddItemToCart": 1, "EnterShoppingCartPage": 2, "StartCheckout": 3,"SaveBilling": 4, "SaveShipping": 5, "SaveShippingMethod": 6, "SaveDeliveryTime": 13, "SavePaymentMethod": 7, "ConfirmOrder": 8, "RemoveAllCartItem": 14, "UpdateCartAll": 12}           
    
    distances = np.zeros((15,15))
    
    prevAct = -1
    sortedKeys = sorted(data)
    for key in sortedKeys:
        ts = dt.datetime.strptime(key[0:19], '%Y-%m-%dT%H:%M:%S') #+ dt.timedelta(hours=3)
        dType = data[key]['dType']
            
        if dType == "Cart":
            ind = name2ind[data[key]['Cartoperationname']] 
        else:
            ind = name2ind[data[key]['Catalogtype']] 
            
        if prevAct != -1:
            distances[prevAct,ind] = distances[prevAct,ind] + 1
        
        prevAct = ind
        
    fig = plt.figure(num=None, figsize=(15,8), dpi=80, facecolor='w', edgecolor='k')        
    plt.imshow(distances, aspect='auto', interpolation='nearest', vmin=0)
    
    labelList = sorted(name2ind, key=lambda k: name2ind[k])
    xLabelList = []
    for i in range(len(labelList)):
        xLabelList.append(labelList[i][0:5])
    plt.xticks(np.arange(15), xLabelList)
    plt.yticks(np.arange(15), labelList)
    
    plt.savefig('./files/%d_webmatrix.png' % customerId)
    
    return distances

def webBrowseGraph(customerId,distances):
    name2ind = {"Login": 0, "Category": 10, "Product": 11, "Logout": 9, "AddItemToCart": 1, "EnterShoppingCartPage": 2, "StartCheckout": 3,"SaveBilling": 4, "SaveShipping": 5, "SaveShippingMethod": 6, "SaveDeliveryTime": 13, "SavePaymentMethod": 7, "ConfirmOrder": 8, "RemoveAllCartItem": 14, "UpdateCartAll": 12}           
    
    ind2name = {}
    for i in name2ind.keys():
        ind2name[name2ind[i]] = i[0:5]

    G = nx.DiGraph()

    plt.figure(figsize=(20,10))

    G.add_nodes_from(np.arange(15))
    nodeLabels = ind2name

    for src in range(15):
        for dest  in range(15):
            if src != dest:
                dist = distances[src,dest]
                if dist != 0:
                    G.add_edge(src, dest, weight=dist)

    edgeLabels=dict([((u,v,),d['weight'])
                     for u,v,d in G.edges(data=True)])

    pos=nx.spring_layout(G)

    nx.draw(G, pos, node_size=3000)
    nx.draw_networkx_labels(G, pos, nodeLabels, font_size=15)
    nx.draw_networkx_edge_labels(G, pos, edgeLabels)
    
    plt.savefig('./files/%d_webgraph.png' % customerId)
  
def loadWeblogCustomer(filename, customerIndex):
    tempX = scipy.io.loadmat(filename)
    custView = tempX['data'][:,:,customerIndex]
    
    return custView

def plotWeblogMatrix(customerId,distances):
    name2ind = {"Login": 0, "Category": 10, "Product": 11, "Logout": 9, "AddItemToCart": 1, "EnterShoppingCartPage": 2, "StartCheckout": 3,"SaveBilling": 4, "SaveShipping": 5, "SaveShippingMethod": 6, "SaveDeliveryTime": 13, "SavePaymentMethod": 7, "ConfirmOrder": 8, "RemoveAllCartItem": 14, "UpdateCartAll": 12}           
    
    fig = plt.figure(num=None, figsize=(15,8), dpi=80, facecolor='w', edgecolor='k')        
    plt.imshow(distances, aspect='auto', interpolation='nearest', vmin=0)
    
    labelList = sorted(name2ind, key=lambda k: name2ind[k])
    xLabelList = []
    for i in range(len(labelList)):
        xLabelList.append(labelList[i][0:5])
    plt.xticks(np.arange(15), xLabelList)
    plt.yticks(np.arange(15), labelList)
    
    plt.savefig('./files/%d_webmatrix.png' % customerId)