
# Including the required libraries .
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.escape import json_encode

import os
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline


# Setting host name, port number, directory name and the static path. 
HOST = 'localhost'
PORT = 8880

DIRNAME = os.path.dirname(os.path.realpath('__file__'))
STATIC_PATH = os.path.join(DIRNAME, '.')


# Creating global variables. 
global selectedCustomerIndex2Id
selectedCustomerIndex2Id = np.loadtxt('files/customersIndex2Id.txt', dtype='int')

# In later implementation, X will represent the sales tensor of all customers.
# For now, it is randomly generated. 
global X
X = np.random.rand(10,20,30)


# Code segment that will bu used in the landing page. Gives examples of how-to-use the functionalities. 
class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
        self.write('<html><head><h1> Tornado Obase Server </h1></head><br>'
                   '<body><h2> Example Usages </h2><br>'
                   '<b> localhost:8880/customerInfo/110236 </b> <br>'
                   'Displays demographic information of customer with id = 110236 <br>'
                   'Some customer ids to use for customerInfo: 110236, 100240, 110236 <br><br>'
                   '<b> localhost:8880/customerSale/991921217 </b> <br>'
                   'Displays heatmap of the sales of customer with id = 991921217 <br>'
                   'Some customer ids to use for customerSale: 991921217, 991464688, 99888001 <br>'
                   '</body></html>')
       

# Code segment that will return customer demographic information as a JSON object. 
# The customer id is given. 
# From the api provided, the code segment executes query to get information and convert it to JSON format.
class CustomerInfo(tornado.web.RequestHandler):
    def get(self, parameter):
        self.post(parameter)
    
    def post(self, parameter):
        customerId = int(parameter)
        #self.write("Customer Id: %d " % customerId)
        
        r = requests.get('http://212.57.2.68:93/api/database/musteri?$filter=IdMusteri+eq+%d'%customerId)
        info = r.json()

        #self.write("Customer Demographic Information: %s" % info)
        self.write("%s" % info)
   

# Given the customer id, this code segment get the sales matrix of the customer, saves it in .png format and displays the image. 
class CustomerSale(tornado.web.RequestHandler):
    def get(self, parameter):
        self.post(parameter)
    
    def post(self, parameter):
        customerId = int(parameter)
        customerIndex = np.where(selectedCustomerIndex2Id==customerId)[0][0]
        
        #SalesTensor = loadFundamentalTensorCustomer('matfiles/AllHours_Item_Customer_Tensor.mat', customerIndex)
        #SalesTensor = collapseTensor(SalesTensor, [1,0,0,1,0], 'sum')
        #SalesTensor = SalesTensor[0,:,:,0,0]
        
        global X
        SalesTensor = X[:,:,customerIndex]
        
        plt.figure
        plt.imshow(SalesTensor)
        plt.savefig('./images/sale.png')

        self.write('<html>Customer Index: %d <br>'
                   'Sale Matrix of Customer<br>'
                   '<img src=\"/images/sale.png\"></body></html>' % customerIndex)


# The configuration of routes.
routes_config = [
    (r"/", MainPage), 
    (r"/customerInfo/([^/]+)", CustomerInfo),
    (r"/customerSale/([^/]+)", CustomerSale),
    (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": "." }),
]
application = tornado.web.Application(routes_config)


def start():
    print("Tornado Obase Server.\nStarting on port %s" % PORT)
    http_server = HTTPServer(application, xheaders=True)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
    return application


if __name__ == "__main__":
    start()