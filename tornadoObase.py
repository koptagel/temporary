# %load tornadoObase.py

# Including the required libraries .
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.escape import json_encode

import os
import json
import requests
import numpy as np
import scipy.io as sio

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import methods from other .py files
from loadFundamentalTensor import clearIrrelevantKeys
from loadFundamentalTensor import loadFundamentalTensor
from loadFundamentalTensor import loadFundamentalTensorCustomer
from collapseTensor import collapseTensor
from plotTensor import plotTensor
from plotTensor import plotTensorTr
from NMF import nmf


# Setting host name, port number, directory name and the static path. 
HOST = 'localhost'
PORT = 8880

DIRNAME = os.path.dirname(os.path.realpath('__file__'))
STATIC_PATH = os.path.join(DIRNAME, '.')

# Creating global variables. 
global EtailerSelectedCustomerIndex2Id
EtailerSelectedCustomerIndex2Id = np.loadtxt('files/Etailer_customersIndex2Id_400.txt', dtype='int')

global ItemIndex2IdGroup3
ItemIndex2IdGroup3 = np.loadtxt('files/Etailer_ItemsIndex2IdGroup3.txt', dtype='int')

global itemIds 
itemIds = np.loadtxt('files/Etailer_ItemIds.txt', dtype='int')

global itemIdsGroup3 
itemIdsGroup3 = np.loadtxt('files/Etailer_ItemIdsGroup3.txt', dtype='int')

#global EtailerTensor
#EtailerTensor,_,_,_,_,_ = loadFundamentalTensor('files/Etailer_AllHours_Item_Customer_Tensor.mat', 24)  

#global EtailerMatrix
#EtailerMatrix = collapseTensor(EtailerTensor,[1,1,1,0,0],'sum')
#EtailerMatrix = EtailerMatrix[0,0,0,:,:].T

global EtailerMatrix
EtailerMatrix = np.load("files/Etailer_Customers_Items_400.npy")



global profileList
profileList = ["Keyifciler", "Tazeciler", "Bebekliler"]

global productList 
productList = ["Cips", "Fistik", "Kola"]


############ HTML CLASSES ##############

# Code segment that will bu used in the landing page. Gives examples of how-to-use the functionalities. 
class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
        self.write('<html><head><h1> Obase Tornado Server </h1></head>'
                   '<body> Son Guncelleme: 17.05.2016 17:30 <br><br>'
                   '* customersOfProfile fonksiyonu gercek verilerle uyumlu hale getirildi. Artik gercek urun idleri verildiginde fonksiyon calisiyor. <br>'
                   '* customerSalesMap fonksiyonu gercek verilerle uyumlu hale getirildi. Ornek olarak gosterilen musteri idleri degistirildi. <br><br>'
                   '* customersOfProfile fonksiyonunun parametrelerinde degisiklik yapildi. <br>'
                   '* customerSaleMap fonksiyonunun ismi customerSalesMap olarak degistirildi. <br>'
                   '* Access-Control-Allow-Origin izni icin degisiklikler yapildi. <br><br>'
                   '<h2> Genel Kullanim </h2>'
                   '45.55.237.86:8880/<b>FonksiyonIsmi</b>?jsonData=<b>JsonInputu</b> <br><br>'
                   'Asagida listelenen butun fonksiyonlarda veriler Json formatinda alinip, sonuclar Json formatinda geri dondurulecektir. <br>'
                   '<b>FonksiyonIsmi</b> yazan yere asagida siralanan fonksiyonlardan birinin adinin yazilmasi gerekiyor. <br>'
                   '<b>JsonInputu</b> yazan kisma ise verilerin Json formatinda girilmesi gerekiyor. <br><br>'
                   'Her fonksiyon icin dikkat edilmesi gerekilen noktalar ve ornek kullanimlar ilerleyen kisimlarda gosterilmistir. <br>'
                   'Ornek kullanimlardaki Json inputlari, fonksiyonlarin calisabilmesi icin gerekli olan temel yapiyi gostermektedir. <br>'
                   'Bu temel yapiya ek olarak baska bilgiler de ayni Json inputunun icerisinde gonderilebilir. <br>'
                   '<h2> Fonksiyonlar </h2>'
                   '<h3> customersOfProfile </h3>'
                   'Verilen urun listesine (kullanici profiline) ve kriterlere gore, bu profile uyan musterilerin idleri ve profile olan uygunluklari listelenecektir. <br>'
                   'MinPercentage parametresi, belirli bir profil uygunluguna sahip musterilerin siralanmasini sagliyor. '
                   'Count parametresi ise listelenecek maksimum musteri sayisini belirtiyor. <br>'
                   'Musteriler, profile uygunluklarina gore siralanmistir (yuksek yuzdeden dusuk yuzdeye gore). <br><br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>customersOfProfile</b>?jsonData=<b>{"Count":5, "MinPercentage":60, "Products": [{"id": 32748}, {"id": 32747}, {"id": 32874}, {"id": 32823}]}</b> <br>'
                   '<b> Output: </b> {"Customers": [{"percentage":98, "id": 90361}, {"percentage":80, "id": 90412}, {"percentage":77, "id": 1073258}]} <br>'
                   'Bu ornekte, verilen urunlere uyan, profil uygunlugu %60in uzerinde olan maksimum 5 musteri listeleniyor. <br><br>'
                   '<h3> customerSalesMap </h3>'
                   'Verilen musteri idsine ve istenilen grafik kriterlerine gore, musteri haritasinin url bilgisi dondurulur. <br><br>'
                   'Grafik kriterlerinin alabilecegi degerler ve ifade ettikleri durumlar asagidaki tablolarda gosterilmistir. <br>'
                   'X ve Y Duzlemleri:'
                   '<table border="1" width=300>'
                   '<tr><td> 0 </td><td> 1 </td><td> 2 </td><td> 3 </td></tr><br>'
                   '<tr><td> Hafta </td><td> Haftanin Gunu </td><td> Saat </td><td> Urun </td></tr><br>'
                   '</table><br>'
                   'Type:'
                   '<table border="1" width=500>'
                   '<tr><td> 1 </td><td> 2 </td></tr><br>'
                   '<tr><td> Toplam Satis Tutari </td><td> Satis yapilip yapilmadigi (0 veya 1 seklinde) </td></tr><br>'
                   '</table> <br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>customerSalesMap</b>?jsonData=<b>{"id": 90412, "xAxis":0, "yAxis": 2, "type": 1} </b><br>'
                   '<b> Output: </b> {"image_url": "45.55.237.86:8880/files/90412_0_2_1.png"} <br>'
                   'Bu ornekte 90412 numarali musterinin haftalara ve saatlere gore yaptigi toplam harcama gosterilmektedir. <br><br>'
                   'Ornek olarak kullanilabilecek musteri idleri: 1073258, 999538, 1155093. <br><br>'
                   '</body></html>')
        


class DefineProfile(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><head><h2> Profil Tanimlama Ekrani </h2></head><br>'
                   '<body><form action="/defineProfile" method="post">'
                   '<table border="1" width=100>'
                   '<tr><td> <b> Profil Tanimla </b> </td></tr><br>'
                   '<tr><td> <input type="text" name="profileName"> </td></tr><br>'
                   '</table>'
                   '<input type="submit" value="Ekle">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("En son eklenen profil: " + self.get_argument("profileName"))
    
        global profileList
        profileList.append(self.get_argument("profileName"))

def tag(attr='', **kwargs):
    for tag, txt in kwargs.items():
        return '<{tag}{attr}>{txt}</{tag}>'.format(**locals())

def createProductsTable():
    global productList

    rows = '\n'.join(tag(tr=''.join(tag(td=productList[i])))
                     for i in range(len(productList)))
    
    return(rows)

def createProfilesList():
    global productList

    rows = '\n'.join( ('<option value="%s"> %s </option>' ) % (profileList[i],profileList[i])
                     for i in range(len(profileList)))
 
    return(rows)

class DefineProducts(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><head><h2> Urun Tanimlama Ekrani </h2></head><br>'
                   '<body><form action="/defineProducts" method="post">'
                   'Musteri Profilleri: <select name="profileName" size="1">')
        
        profiles = createProfilesList()
        self.write(profiles)
                   
        self.write('</select><br>'
                   '<table border="1" width=150>'
                   '<tr><td> <b> Urun Tanimla </b> </td></tr><br>')
                   
        products = createProductsTable()
        self.write(products)
        
        self.write('</table><br>'
                   '<input type="text" name="productName"> <input type="submit" value="Ekle"> '
                   '</form></body></html>')

        
    def post(self):
        #self.set_header("Content-Type", "text/plain")
        #self.write("En son eklenen urun: " + self.get_argument("productName")) 
        #self.write("Secilen profil: " + self.get_argument("profileName")) 
        
        global productList
        productList.append(self.get_argument("productName"))
        
        self.get()
          
            
        
class MidResults(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><head><h2> Ara Sonuc Ekrani </h2></head><br>'
                   '<body><form action="/midResults" method="post">'
                   'Musteri Profilleri: <select name="profileName" size="1">')
        
        profiles = createProfilesList()
        self.write(profiles)
        
        self.write('</select><br>'
                   '<table border="1" width=250>'
                   '<tr><td> <b> Musteri </b> </td> <td> <b> Profil Uygunlugu </b> </td> </tr><br>'
                   '<tr><td> Musteri X </td> <td> %100 </td> </tr><br>'
                   '<tr><td> Musteri Y </td> <td> %99 </td> </tr><br>'
                   '<tr><td> Musteri Z </td> <td> %98 </td> </tr><br>'
                   '<tr><td> Musteri T </td> <td> %97 </td> </tr><br>'
                   '</table><br>'
                   'Kriter: <select name="criteriaName" size="1">'
                   '<option value="cName"> Haftanin Gunleri </option>'
                   '<option value="cName"> Haftalik Harcama </option>'
                   '<option value="cName"> Haftalik Urunler </option></select><br>'
                   '<img src=\"/files/99888001.png\" height="300", width="400"><br>'
                   '<input type="button" value="Benzerlerini Bul"></form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("En son secilen customer: " + self.get_argument("customerName"))     

        
############ OBASE FUNCTIONS ##############

# localhost:8880/customersOfProfile?jsonData={"Products": [{"id": 3}, {"id": 7}, {"id": 1}, {"id": 20}, {"id": 19}, {"id": 35}]} 
class CustomersOfProfile(tornado.web.RequestHandler):
        
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
    
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        profile_data = json.loads(temp)
        
        productList = profile_data['Products']
        numProducts = len(productList)
        
        #index = []
        #for i in range(numProducts):
        #    index.append(productList[i]['id'])
        
        index = []
        for i in range(numProducts):
            pid = productList[i]['id']
            
            if pid in itemIds:
                ind = np.where(itemIds==pid)[0][0]
                pid3 = itemIdsGroup3[ind]
                index.append(np.where(ItemIndex2IdGroup3==pid3)[0][0])
        
        global EtailerMatrix
        s1,s2 = EtailerMatrix.shape
        rank = 1
        
        #index = [3,7,1,19,20,30,35,40]
        Z2 = np.zeros((rank,s2))
        Z2[0,index] = 1
        
        maxIter = 3
        
        _, _, _, _, indices, percentages = nmf(EtailerMatrix, Z2, maxIter, rank)
        customerIds = EtailerSelectedCustomerIndex2Id[indices]
        
        #self.write("Percentages and Customer Ids")
        #for i in range(len(percentages)):
        #    self.write(" %f, %d. " %(percentages[i], customerIds[i]))
        
        numCustomers = profile_data['Count']
        minPercentage = profile_data['MinPercentage']
        
        count = 0
        data = []
        for i in range(len(customerIds)):
            if count < numCustomers:
                if int(percentages[i])>= minPercentage:
                    data2 = {}
                    data2['percentage'] = int(percentages[i])
                    data2['id'] = int(customerIds[i])

                    data.append(data2)
                    count = count+1
            
        json_data = json.dumps({"Customers": data})
        self.write(json_data)  


class CustomerSalesMap(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        plot_data = json.loads(temp)
        
        customerId = int(plot_data['id'])
        ax1 = int(plot_data['xAxis'])
        ax2 = int(plot_data['yAxis'])
        criteria = plot_data['type']
        
        #customerIndex = np.where(selectedCustomerIndex2Id==customerId)[0][0]
        customerIndex = np.where(EtailerSelectedCustomerIndex2Id==customerId)[0][0]
        
        
        dimensions = np.array([1,1,1,1,0])
        dimensions[ax1] = 0
        dimensions[ax2] = 0

        if criteria==1:
            plotCriteria = 'sum'
        else:
            plotCriteria = 'binary'
        
        X = loadFundamentalTensorCustomer('files/Etailer_AllHours_Item_Customer_Tensor_400.mat', customerIndex, 24)
        X = collapseTensor(X, dimensions, plotCriteria)
        
        plt.figure
        plotTitle = "Sales of Customer %d" % customerId
        if ax1 < ax2:
            plotTensor(X, numPlots=1, title=plotTitle, figsize=(8, 6))
        else: 
            plotTensorTr(X, numPlots=1, title=plotTitle, figsize=(8, 6))
        plt.savefig('./files/%d_%d_%d_%d.png' % (customerId,ax1,ax2,criteria))

        imageUrl = ("45.55.237.86:%s/files/%d_%d_%d_%d.png" % (PORT,customerId,ax1,ax2,criteria))
        
        info = json.dumps({"image_url": imageUrl})
        self.write("%s" % info)
        

# The configuration of routes.
routes_config = [
    (r"/", MainPage), 
    (r"/defineProfile", DefineProfile),
    (r"/defineProducts", DefineProducts),
    (r"/midResults", MidResults),
    (r"/customersOfProfile", CustomersOfProfile),
    (r"/customerSalesMap", CustomerSalesMap),
    (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": "." }),
]
application = tornado.web.Application(routes_config)

def start():
    print("Obase Tornado Server.\nStarting on host %s, port %s" % (HOST,PORT))
    http_server = HTTPServer(application, xheaders=True)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
    return application


if __name__ == "__main__":
    start()