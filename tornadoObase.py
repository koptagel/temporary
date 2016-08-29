# %load tornadoObase.py
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
from sklearn.decomposition import NMF

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import methods from other .py files
from loadFundamentalTensor import clearIrrelevantKeys
from loadFundamentalTensor import loadFundamentalTensor
from loadFundamentalTensor import loadFundamentalTensorCustomer
from loadFundamentalTensor import loadViewCustomer
from collapseTensor import collapseTensor
from collapseTensor import collapseSlotTensor
from plotTensor import plotTensor
from plotTensor import plotTensorTr
from plotTensor import plotBarChart
from plotTensor import plotTimeSlot
from plotTensor import plotTimeSlotBarChart
from NMF import nmfFixBasis
from NMF import nmf
from distance import distance
from weblog import webBrowseMatrix
from weblog import webBrowseGraph
from weblog import loadWeblogCustomer
from weblog import plotWeblogMatrix
from TxtFileFuncs import loadMatrixFromTxt
from TxtFileFuncs import loadRecommendationMatrixFromTxt
from TxtFileFuncs import loadItemIdAndDsFromTxt
from TxtFileFuncs import loadCustomerIdFromTxt
from TxtFileFuncs import loadRecommendationOfCustomerMatrixFromTxt
from TxtFileFuncs import loadRecommendationOfCustomerMatrixFromTxt2
from TxtFileFuncs import loadRecommendationOfCustomerProfilesFromTxt

# Setting host name, port number, directory name and the static path. 
HOST = 'localhost'
PORT = 8086

CUSTOMERCOUNT = 3193

MAX_INT = 2147483647

DIRNAME = os.path.dirname(os.path.realpath('__file__'))
STATIC_PATH = os.path.join(DIRNAME, '.')

# Creating global variables. 
global EtailerSelectedCustomerIndex2Id
EtailerSelectedCustomerIndex2Id = np.loadtxt('files/Etailer_customersIndex2Id_%d.txt'%CUSTOMERCOUNT, dtype='int')

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
EtailerMatrix = np.load("files/Etailer_Customers_Items_%d.npy"%CUSTOMERCOUNT)

global EtailerMatrixEst
#EtailerMatrixEst, _, _, _, _, _ = nmf(EtailerMatrix, 100, 20)
model = NMF(n_components=20, init='nndsvd', random_state=2)
W = model.fit_transform(EtailerMatrix) 
H = model.components_
EtailerMatrixEst = np.dot(W,H)


### RECOMMENDATION SYSTEM
print("** Start Recommendation System **")

filename = "files/1_1_1_7269_3392_Tensor_binary.txt"
global PurchaseMatrix
PurchaseMatrix = loadMatrixFromTxt(filename)

#filename = "files/1_1_1_7269_3392_TensorEst.txt"
#global PurchaseMatrixEst
#PurchaseMatrixEst = loadRecommendationMatrixFromTxt(filename)

name = "files/81_7_24_7269_3392"
global itemids
global itemdss
global customeridss
itemids,itemdss = loadItemIdAndDsFromTxt(name)
customeridss = loadCustomerIdFromTxt(name)

#model = NMF(n_components=20, init='nndsvd', random_state=2)
#W = model.fit_transform(PurchaseMatrix) 
#H = model.components_
#PurchaseMatrixEst = np.dot(W,H)

print("** End Recommendation System **")
### RECOMMENDATION SYSTEM


global profileList
profileList = ["Keyifciler", "Tazeciler", "Bebekliler"]

global productList 
productList = ["Cips", "Fistik", "Kola"]

global tempIndices
tempIndices = np.zeros((CUSTOMERCOUNT))

global tempRes
tempRes = np.zeros((CUSTOMERCOUNT))

global tempPerc
tempPerc = np.zeros((CUSTOMERCOUNT))

global Dist
Dist = np.zeros((CUSTOMERCOUNT))

############ HTML CLASSES ##############

# Code segment that will bu used in the landing page. Gives examples of how-to-use the functionalities. 
class MainPage(tornado.web.RequestHandler):

    def get(self):
        self.post()
        
    def post(self):
        self.write('<html><head><h1> Obase Tornado Server </h1></head>'
                   '<body> Son Guncelleme: 21.08.2016 20:00 <br><br>'
                   '* customerSalesMap fonksiyonunda artik her iki eksene de saat araligi verilebiliyor. <br>'
                   '* similarCustomers fonksiyonu su anda her iki eksene de saat araligi verilecek sekilde calismiyor. Onumuzdeki gunlerde metod guncellenecek. <br><br>'
                   '* recommendProducts2 fonksiyonundaki problem giderildi. <br>'
                   '* similarCustomers fonksiyonu musteri profilleri icin urun dondurecek sekilde guncellendi. Fonksiyona yeni parametreler eklendi. <br>'
                   '* similarCustomers fonksiyonu artik distance, minimum ve maksimum distance ve toplam musteri sayisi degerlerini de donduruyor. <br>'
                   '* similarCustomers fonksiyonundaki benzerlik yuzdesinin hesaplanisi, fonksiyonun aciklama kismina eklendi. <br>'
                   '* similarCustomers fonksiyonu, saat araliklari alacak sekilde guncellendi. Su anda bir eksen saat araligi iken, diger eksen hafta, haftanin gunu veya urun olacak sekilde calisiyor.<br>'
                   '* customerSalesMap fonksiyonu, saat araliklari alacak sekilde guncellendi. Su anda bir eksen saat araligi iken, diger eksen hafta, haftanin gunu veya urun olacak sekilde calisiyor.<br><br>'
                   '<h2> Dataset Bilgileri </h2>'
                   'Ilk Alisveris Tarihi: 05.01.2015 00:00 <br>'
                   'Son Alisveris Tarihi: 16.05.2016 15:00 <br>'
                   'Toplam Satis Miktari: 432.636 <br>'
                   'Musteri Sayisi: 3.193 <br>'
                   'Gecerli Urun Sayisi: 6.087 <br>'
                   'Gecerli Urun Grup3 Sayisi: 180 <br><br>'
                   'recommendProducts2 fonksiyonu daha farkli bir dataset kullaniyor. <br>'
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
                   'ProfileId ve ProfileDs inputları profilin id numarasını ve ismini ifade etmek için gerekiyor. Bu id ve isim daha sonra similarCustomers fonksiyonunda kullanılacak. <br>'
                   'Musteriler, profile uygunluklarina gore siralanmistir (yuksek yuzdeden dusuk yuzdeye gore). <br><br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>customersOfProfile</b>?jsonData=<b>{"Count":5, "MinPercentage":60, "ProfileId": 11, "ProfileDs": "Bebek", "Products": [{"id": 9556}, {"id": 34398}, {"id": 5974}]}</b> <br>'
                   '<b> Output: </b> {"Customers": [{"percentage":98, "id": 90361}, {"percentage":80, "id": 90412}, {"percentage":77, "id": 1073258}]} <br>'
                   'Bu ornekte, verilen urunlere uyan, profil uygunlugu %60in uzerinde olan maksimum 5 musteri listeleniyor. <br>'
                   'Profile uyan müsterilerin bilgileri, daha sonra kullanılmak için arka planda kaydediliyor. <br><br>'
                   '<h3> customerSalesMap </h3>'
                   'Verilen musteri idsine ve istenilen grafik kriterlerine gore, musteri haritasinin url bilgisi dondurulur. <br><br>'
                   'Grafik kriterlerinin alabilecegi degerler ve ifade ettikleri durumlar asagidaki tablolarda gosterilmistir. <br>'
                   'X ve Y Duzlemleri:'
                   '<table border="1" width=600>'
                   '<tr><td> 0 </td><td> 1 </td><td> 2 </td><td> 3 </td><td> 4 </td><td> 5 </td><td> 6 </td></tr><br>'
                   '<tr><td> Hafta </td><td> Haftanin Gunu </td><td> Saat </td><td> Urun </td><td> Weblog Matrix </td><td> Weblog Graph </td><td> Saat Araligi </td></tr><br>'
                   '</table><br>'
                   'Type:'
                   '<table border="1" width=500>'
                   '<tr><td> 1 </td><td> 2 </td></tr><br>'
                   '<tr><td> Toplam Satis Tutari </td><td> Satis yapilip yapilmadigi (0 veya 1 seklinde) </td></tr><br>'
                   '</table> <br>'
                   'Musterilerin satis grafiklerinin bar chartlarini gorebilmek icin xAxis ve yAxis degerlerinin ayni sayi olmasi gerekli. <br>'
                   'Musterilerin web aktivitelerinin grafiklerinin de xAxis ve yAxis degerlerinin ayni sayi olmasi gerekiyor. <br>'
                   'Saat araliklarina bakilabilmesi icin input olarak slots parametresi de verilmesi gerekiyor. <br>'
                   'Saat araligi belirlerken istenilen sayida aralik boyutu belirlenebiliyor. <br><br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>customerSalesMap</b>?jsonData=<b>{"id": 90412, "xAxis":0, "yAxis": 6, "type": 1, "slots": [{"x":0,"y":8},{"x":10,"y":20},{"x":20,"y":24}]} </b><br>'
                   '<b> Output: </b> {"image_url": "45.55.237.86:8880/files/90412_0_6_1.png"} <br>'
                   'Bu ornekte 90412 numarali musterinin haftalara ve saat araliklarina ([0,8),[10,20),[20,24)) gore yaptigi toplam harcama gosterilmektedir. <br><br>'
                   'Ornek olarak kullanilabilecek musteri idleri: 1073258, 999538, 1155093. <br><br>'
                   '<h3> similarCustomers </h3>'
                   'Verilen musteri idsine, grafik kriterlerine, kisi sayisi, uzaklik tipine ve uygunluk sinirina gore, musteriye benzer olan diger musterilerin listesi, benzerlik oranlari ve diger musterilere onerilebilecek urun listesi dondurulur. <br>'
                   'Su anda onerilen urun listesi random bicimde uretiliyor (gercek urun idleri ile). Ilerleyen gunlerde bu kisim degistirilecek. <br><br>'
                   'Grafik kriterlerinin alabilecegi degerler ve ifade ettikleri durumlar customerSalesMap fonksiyonundaki gibidir. <br>'
                   'Count ve MinPercentage parametrelerinin islevleri customersOfProfile fonksiyonundaki islevleriyle aynidir. <br><br>'
                   'distanceType parametresinin alabilecegi degerler ve ifade ettigi uzakliklar asagidaki gibidir.'
                   '<table border="1" width=1150>'
                   '<tr><td> 0 </td><td> 1 </td><td> 2 </td><td> 3 </td></tr><br>'
                   '<tr><td> Kullback-Leibler (KL) Divergence </td><td> Itakura-Saito (IS) Distance </td><td> Hellinger Distance </td><td> Euclidean Distance </td></tr><br>'
                   '<tr><td> KL(P,Q) = P * log(P/Q) - P + Q </td><td> IS(P,Q) = (P/Q) * log(P/Q) - 1 </td><td> H(P,Q) = (1/sqrt(2)) * sqrt((sqrt(P) - sqrt(Q))*(sqrt(P) - sqrt(Q))) </td><td> EUC(P,Q) = (1/2) * (P-Q) * (P-Q) </td></tr><br>'
                   '</table><br>'
                   'searchType parametresinin alabilecegi degerler ve anlamları asagidaki gibidir.'
                   '<table border="1" width=500>'
                   '<tr><td> 0 </td><td> 1 </td><br>'
                   '<tr><td> Bütün müşterilerde ara </td><td> Sadece o profildeki müşterilerde ara </td></tr><br>'
                   '</table><br>'
                   'searchType parametresi 1 değerini aldığında, input olarak ayrıca profilin id numarasının ve isminin verilmesi gerekiyor (customersOfProfile fonksiyonunda kullanılan). <br><br>'
                   'baseCount parametresi, benzer urunlerin kac musteri temel alinarak hesaplanacagini belirtiyor. Parametre 0 degerini aldiginda, o profildeki/listedeki butun musteriler icin calisiyor. <br><br> '
                   'productCount parametresi, musterilere onerilen ilk kac urunu goz onunde bulunduracagimizi belirtiyor. <br><br>'
                   'baseCount ve productCount parametrelerine verilen degerlere gore fonksiyonun calisma suresinde farkliliklar oluyor. <br><br>'
                   'Musterilerin benzerlik yuzdesi bu formulle hesaplaniyor; percentage = 100 - (100 * distance / maxDistance) <br><br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>similarCustomers</b>?jsonData=<b>{"id": 1279930, "xAxis":0, "yAxis": 6, "type": 2, "distanceType": 0, "Count":5, "MinPercentage":60, "productCount": 10, "baseCount": 50, "searchType": 1, "ProfileId": 11, "ProfileDs": "Bebek", "slots": [{"x":0,"y":8},{"x":10,"y":20},{"x":20,"y":24}]} </b><br>' 
                   '<b> Output: </b> {"Customers": [{"distances": 0, "percentage": 100, "id": 1279930}, {"distances": 35, "percentage": 72, "id": 1406410}, {"distances": 42, "percentage": 66, "id": 1058305}, {"distances": 42, "percentage": 66, "id": 1366933}, {"distances": 44, "percentage": 65, "id": 91248}], "Products": [{"id": 12680, "percentage": 62}, {"id": 12667, "percentage": 48}, {"id": 20083, "percentage": 48}, {"id": 12700, "percentage": 46}, {"id": 12677, "percentage": 46}, {"id": 12719, "percentage": 44}, {"id": 12678, "percentage": 38}, {"id": 10981, "percentage": 36}, {"id": 12689, "percentage": 32}, {"id": 12668, "percentage": 27}], "MinDistance": 0, "MaxDistance": 128} <br>'
                   'Bu ornekte 1279930 numarali musterinin alim aliskanligina (haftalara ve saat araliklarina gore, alisveris yapip yapmadigi) en cok benzerlik gosteren, profil uygunlugu %60in uzerinde olan maksimum 5 musteri listeleniyor.'
                   'Bu müşteriler, 11 numaralı Bebek profilindeki müşterilerden seçiliyor. <br><br>'
                   'Bu ornekte benzerlik yuzdeleri su sekilde hesaplaniyor (maxDistance=128): <br>'
                   'Musterinin kendisine olan uzakligi distance(1279930,1279930) = 0. percentage = 100 <br>'
                   '1406410 id numarali musteriye olan uzakligi distance(1279930,1406410) = 35. percentage = 100 - (100 * 35 / 128) = 72 <br>'
                   'Musterinin kendisine en benzemeyen kisiyle olan uzakligi distance = maxDistance. percentage = 100 - (100 * 128 / 128) = 0 <br><br>'
                   'Bu ornekte onerilen urunleri inceledigimizde; <br>'
                   '12680 id numarali urun, 50 kisiden (baseCount) 31 kisiye onerilmis. O yuzden onerilme yuzdesi 62 olarak hesaplaniyor. <br> '
                   '12667 id numarali urun, 50 kisiden 24 kisiye onerilmis. O yuzden onerilme yuzdesi 48 olarak hesaplaniyor. <br><br> '
                   'Ornek olarak kullanilabilecek musteri idleri: 1073258, 999538, 1155093. <br><br>'
                   '<h3> customerWeblog </h3>'
                   'Verilen musteri idsine gore, webdeki hareket grafiklerinin url bilgisi dondurulur. <br><br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>customerWeblog</b>?jsonData=<b>{"id": 90412} </b><br>'
                   '<b> Output: </b> {"image_url": "45.55.237.86:8880/files/90412_webmatrix.png","image_url_graph": "45.55.237.86:8880/files/90412_webgraph.png"} <br>'
                   'Ornek olarak kullanilabilecek musteri idleri: 1073258, 999538. <br><br>'
                   '<h3> recommendProducts </h3>'
                   'Verilen musteri idsi, tavsiye tipi ve sayiya gore onerilen urunlerin idleri dondurulur. <br>'
                   'Su anda onerilen urunlerin IdUrunGrup3 degerleri donduruluyor. Ilerleyen asamalarda IdUrun degerleri dondurulecek. <br><br> '
                   'type parametresi oneri listesinin nasil duzenlenecegini belirtiyor. Parametrenin alabilecegi degerler ve anlamlari asagidaki gibidir. '
                   '<table border="1" width=800>'
                   '<tr><td> mix </td><td> Hem simdiye kadar alinan hem de henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'
                   '<tr><td> discover </td><td> Yalnizca henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'
                   '<tr><td> habit </td><td> Yalnizca simdiye kadar alinan urunler listelenir </td></tr><br>'
                   '</table><br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>recommendProducts</b>?jsonData=<b>{"id": 737293, "type": "mix", "Count":5} </b><br>'
                   '<b> Output: </b> {"Products": [{"id": 597}, {"id": 454}, {"id": 457}, {"id": 553}, {"id": 636}]} <br>'
                   'Bu ornekte 737293 numarali musteri icin maksimum 5 tane urun oneriliyor. Urun listesi musterinin hem simdiye kadar aldigi hem de henuz almadigi fakat alma ihtimali yuksek urunlerden olusuyor. <br><br>'
                   '<h3> recommendProducts2 </h3>'
                   'Verilen musteri idsi, tavsiye tipi ve sayiya gore onerilen urunlerin idleri dondurulur. <br><br>'
                   'Bu fonksiyonda kullanilan dataset, serverin geri kalanindan farkli. Butun server bu datasete gore update edilecek. <br>'
                   'Dataset 05.01.2015 00:00 - 18.07.2016 14:00 tarihleri arasinda yapilan satislari kapsiyor. <br>' 
                   '81 Hafta, 7 Gun, 24 Saat, 7.269 Urun, 3.392 Musteri <br><br>'
                   'type parametresi oneri listesinin nasil duzenlenecegini belirtiyor. Parametrenin alabilecegi degerler ve anlamlari asagidaki gibidir. '
                   '<table border="1" width=800>'
                   '<tr><td> mix </td><td> Hem simdiye kadar alinan hem de henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'
                   '<tr><td> discover </td><td> Yalnizca henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'
                   '<tr><td> habit </td><td> Yalnizca simdiye kadar alinan urunler listelenir </td></tr><br>'
                   '</table><br>'
                   '<b> Input: </b> 45.55.237.86:8880/<b>recommendProducts2</b>?jsonData=<b>{"id": 737293, "type": "mix", "Count":5} </b><br>'
                   '<b> Output: </b> {"Products": [{"id": 32823}, {"id": 18110}, {"id": 18109}, {"id": 1808}, {"id": 18107}]} <br>'
                   'Bu ornekte 737293 numarali musteri icin maksimum 5 tane urun oneriliyor. Urun listesi musterinin hem simdiye kadar aldigi hem de henuz almadigi fakat alma ihtimali yuksek urunlerden olusuyor. <br><br>'
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
        

class CustomerSalesMap(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        plot_data = json.loads(temp)
        
        customerId = int(plot_data['id'])
        criteria = plot_data['type']
        ax1 = int(plot_data['xAxis'])
        ax2 = int(plot_data['yAxis'])
        
        if customerId not in EtailerSelectedCustomerIndex2Id:
            self.write("Invalid Customer Id")
        elif criteria not in [1,2]:
            self.write("Invalid Type. Type must be 1 or 2.")
        elif ax1 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")
        elif ax2 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")
        #elif ax1 == ax2:
        #    self.write("Invalid Axis Values. Axis values must be different from each other.")
        else:
        
            customerIndex = np.where(EtailerSelectedCustomerIndex2Id==customerId)[0][0]
            
            if criteria==1:
                plotCriteria = 'sum'
            else:
                plotCriteria = 'binary'
            
            if ax1 in [0,1,2,3] and ax2 in [0,1,2,3]:
                dimensions = np.array([1,1,1,1,0])
                dimensions[ax1] = 0
                dimensions[ax2] = 0


                X = loadFundamentalTensorCustomer('files/Etailer_AllHours_Item_Customer_Tensor_%d.mat'%CUSTOMERCOUNT, customerIndex, 24)
                X = collapseTensor(X, dimensions, plotCriteria)

                plt.figure
                plotTitle = "Sales of Customer %d" % customerId
                if ax1 < ax2:
                    plotTensor(X, numPlots=1, title=plotTitle, figsize=(8, 6))
                elif ax1 == ax2:
                    plotBarChart(X, numPlots=1, title=plotTitle, figsize=(8, 6))
                else: 
                    plotTensorTr(X, numPlots=1, title=plotTitle, figsize=(8, 6))
                plt.savefig('./files/%d_%d_%d_%d.png' % (customerId,ax1,ax2,criteria))

                imageUrl = ("45.55.237.86:%s/files/%d_%d_%d_%d.png" % (PORT,customerId,ax1,ax2,criteria))

                info = json.dumps({"image_url": imageUrl})
                self.write("%s" % info)
            
            elif ax1==6 or ax2==6:
                if ax1 != ax2:
                    slots = plot_data['slots']
                    timePoints = []
                    timePointsY = []
                    for i in range(len(slots)):
                        timePoints.append(int(slots[i]["x"]))
                        timePointsY.append(int(slots[i]["y"]))


                    X = loadFundamentalTensorCustomer('files/Etailer_AllHours_Item_Customer_Tensor_%d.mat'%CUSTOMERCOUNT, customerIndex, 24)
                    newMatrix = collapseSlotTensor(X, ax1, ax2, timePoints, timePointsY, plotCriteria)

                    plt.figure
                    plotTitle = "Sales of Customer %d" % customerId
                    plotTimeSlot(newMatrix.T, plotTitle,ax1,ax2, timePoints, timePointsY, figsize=(8, 6))
                    plt.savefig('./files/%d_%d_%d_%d.png' % (customerId,ax1,ax2,criteria))
                    imageUrl = ("45.55.237.86:%s/files/%d_%d_%d_%d.png" % (PORT,customerId,ax1,ax2,criteria))

                    info = json.dumps({"image_url": imageUrl})
                    self.write("%s" % info)
                else:
                    slots = plot_data['slots']
                    timePoints = []
                    timePointsY = []
                    for i in range(len(slots)):
                        timePoints.append(int(slots[i]["x"]))
                        timePointsY.append(int(slots[i]["y"]))


                    X = loadFundamentalTensorCustomer('files/Etailer_AllHours_Item_Customer_Tensor_%d.mat'%CUSTOMERCOUNT, customerIndex, 24)
                    newMatrix = collapseSlotTensor(X, 1, ax2, timePoints, timePointsY, plotCriteria)
                    newMatrix = np.sum(newMatrix, axis=0, keepdims=False)
                    if plotCriteria == 'binary':
                        newMatrix[np.where(newMatrix>0)]=1
                        
                    plt.figure
                    plotTitle = "Sales of Customer %d" % customerId
                    plotTimeSlotBarChart(newMatrix, plotTitle, timePoints, timePointsY, figsize=(8, 6))
                    plt.savefig('./files/%d_%d_%d_%d.png' % (customerId,ax1,ax2,criteria))
                    imageUrl = ("45.55.237.86:%s/files/%d_%d_%d_%d.png" % (PORT,customerId,ax1,ax2,criteria))

                    info = json.dumps({"image_url": imageUrl})
                    self.write("%s" % info)
                    
                    print("****")
                    print(newMatrix.shape)
                
            else:
            
                #distances = webBrowseMatrix(customerId)
                
                filename = 'files/weblog_%d.mat'%CUSTOMERCOUNT
                distances = loadWeblogCustomer(filename, customerIndex)
                
                if np.sum(distances) == 0:
                    self.write("Invalid Customer Id. This customer does not have weblog data.")
                else:
                    plotWeblogMatrix(customerId,distances)
                    webBrowseGraph(customerId,distances)
                    
                    if ax1 == 4:
                        imageUrl = (HOST+":%s/files/%d_webmatrix.png" % (PORT,customerId))
                    elif ax1 == 5:
                        imageUrl = (HOST+":%s/files/%d_webgraph.png" % (PORT,customerId))

                    info = json.dumps({"image_url": imageUrl})
                    self.write("%s" % info)

                    
                    
class CustomerWeblogPlots(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        plot_data = json.loads(temp)
        
        customerId = int(plot_data['id'])
        
        distances = webBrowseMatrix(customerId)
        
        if np.sum(distances) == 0:
            self.write("Invalid Customer Id. This customer does not have weblog data.")
        else:
            webBrowseGraph(customerId,distances)

            matrixUrl = ("45.55.237.86:%s/files/%d_webmatrix.png" % (PORT,customerId))
            graphUrl = ("45.55.237.86:%s/files/%d_webgraph.png" % (PORT,customerId))

            info = json.dumps({"image_url": matrixUrl, "image_url_graph": graphUrl})
            self.write("%s" % info)

                 
                
class CustomersOfProfile(tornado.web.RequestHandler):
        
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
    
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        profile_data = json.loads(temp)
        
        numCustomers = profile_data['Count']
        minPercentage = profile_data['MinPercentage']
        #criteria = profile_data['type']
        
        profileId = profile_data['ProfileId']
        profileDs = profile_data['ProfileDs']
    
        if numCustomers<1:
            self.write("Invalid count. Count must be more than 0.")
        elif minPercentage>100:
            self.write("Invalid percentage. Minimum percentage must less than or equal to 100.")
        #elif criteria not in [1,2]:
        #    self.write("Invalid Type. Type must be 1 or 2.")
        else:

            productList = profile_data['Products']
            numProducts = len(productList)

            index = []
            invalidItems = []
            for i in range(numProducts):
                pid = productList[i]['id']

                if pid in itemIds:
                    ind = np.where(itemIds==pid)[0][0]
                    pid3 = itemIdsGroup3[ind]
                    index.append(np.where(ItemIndex2IdGroup3==pid3)[0][0])
                else:
                    data2 = {}
                    data2['id'] = int(pid)
                    invalidItems.append(data2)

            global EtailerMatrix
            EtailerMatrix[np.where(EtailerMatrix>0)]=1
            
            #if criteria == 2:
            #    EtailerMatrix[np.where(EtailerMatrix>0)]=1
            
            s1,s2 = EtailerMatrix.shape
            rank = 1

            Z2 = np.zeros((rank,s2))
            Z2[0,index] = 1

            maxIter = 3

            _, _, _, _, indices, percentages = nmfFixBasis(EtailerMatrix, Z2, maxIter, rank)
            customerIds = EtailerSelectedCustomerIndex2Id[indices]

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

            if len(invalidItems) > 0:
                json_data = json.dumps({"Customers": data, "InvalidItems": invalidItems})
            else:    
                json_data = json.dumps({"Customers": data})
                
            self.write(json_data)  
            
            
            data = []
            for i in range(len(customerIds)):
                data2 = {}
                data2['percentage'] = int(percentages[i])
                data2['id'] = int(customerIds[i])
                data.append(data2)
                
            filename = "files/profileFiles/ProfileCustomers_%s_%d.txt" % (profileDs,profileId)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)

            
            filename = "files/profileFiles/ProfileProducts_%s_%d.txt" % (profileDs,profileId)
            with open(filename, 'w') as outfile:
                json.dump(productList, outfile)

            
            
class similarCustomers(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        similar_data = json.loads(temp)
        

        customerId = int(similar_data['id'])
        numCustomers = similar_data['Count']
        minPercentage = similar_data['MinPercentage']
        
        criteria = similar_data['type']
        ax1 = int(similar_data['xAxis'])
        ax2 = int(similar_data['yAxis'])
        
        distanceType = similar_data['distanceType']
        searchType = similar_data['searchType']
        
        numRecItems = similar_data['productCount']
        numRecBase = similar_data['baseCount']
        
        if customerId not in EtailerSelectedCustomerIndex2Id:
            self.write("Invalid Customer Id")
        elif numCustomers<1:
            self.write("Invalid count. Count must be more than 0.")
        elif minPercentage>100:
            self.write("Invalid percentage. Minimum percentage must less than or equal to 100.")
        elif criteria not in [1,2]:
            self.write("Invalid Type. Type must be 1 or 2.")
        elif ax1 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")
        elif ax2 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")
        #elif ax1 == ax2:
        #    self.write("Invalid Axis Values. Axis values must be different from each other.")
        elif distanceType not in [0,1,2,3]:
            self.write("Invalid Distance Type. Distance type must be 0,1,2 or 3.")
        elif searchType not in [0,1]:
            self.write("Invalid Search Type. Search type must be 0 or 1.")
        else:
        
            customerIndex = np.where(EtailerSelectedCustomerIndex2Id==customerId)[0][0]
    
                
            if distanceType==0:
                metric = 'kl'
            elif distanceType==1:
                metric = 'is'
            elif distanceType==2:
                metric = 'hel'
            else:
                metric = 'euc'
                
            if criteria == 2:
                plotCriteria = 'binary'
            else:
                plotCriteria = 'sum'
                
                
            if ax1 in [4,5] or ax2 in [4,5]:
                filename = 'files/weblog_%d.mat'%CUSTOMERCOUNT
                
                X = loadWeblogCustomer(filename, customerIndex)
                
                distances = np.zeros(CUSTOMERCOUNT)
                for i in range(CUSTOMERCOUNT):
                    custDist = loadWeblogCustomer(filename, i)

                    if np.sum(custDist) == 0:
                        distances[i] = MAX_INT
                    else:
                        distances[i] = distance(X, custDist, metric)
                
                global tempRes
                tempRes = distances
            
            elif ax1 == 6 and ax2 == 6:
                print("*** ax1 ax2 6")
                
                slots = similar_data['slots']
                timePoints = []
                timePointsY = []
                for i in range(len(slots)):
                    timePoints.append(int(slots[i]["x"]))
                    timePointsY.append(int(slots[i]["y"]))

                filename = 'files/dhc_%d.mat'%CUSTOMERCOUNT
                X = loadViewCustomer(filename,customerIndex)
                #X = loadFundamentalTensorCustomer('files/Etailer_AllHours_Item_Customer_Tensor_%d.mat'%CUSTOMERCOUNT, customerIndex, 24)
                X = collapseSlotTensor(X, 1, ax2, timePoints, timePointsY, plotCriteria)
                X = np.sum(X, axis=0, keepdims=True)
                if plotCriteria == 'binary':
                    X[np.where(X>0)]=1  
                    
                print("x shape")
                print(X.shape)
                    
                if searchType == 0:
                    profileCustCount = CUSTOMERCOUNT
                    custIndexList = np.arange(CUSTOMERCOUNT)
                    
                else:
                    profileId = similar_data['ProfileId']
                    profileDs = similar_data['ProfileDs']
                    
                    filename2 = "files/profileFiles/ProfileCustomers_%s_%d.txt" % (profileDs, profileId)

                    json_data=open(filename2).read()
                    customersData = json.loads(json_data)

                    profileCustCount = 150
                    profileCustomers = customersData[0:profileCustCount]

                    #customerIdsList = []
                    custIndexList = []
                    for cust in profileCustomers:
                        #customerIdsList.append(cust['id'])
                        custIndexList.append(np.where(EtailerSelectedCustomerIndex2Id==cust['id'])[0][0])
                    custIndexList = np.array(custIndexList)
                 
                distances = np.zeros(len(custIndexList))
                for i in range(len(custIndexList)):
                    filename = 'files/dhc_%d.mat'%CUSTOMERCOUNT
                    cust = loadViewCustomer(filename,custIndexList[i])
                    #cust = loadFundamentalTensorCustomer('files/Etailer_AllHours_Item_Customer_Tensor_%d.mat'%CUSTOMERCOUNT, custIndexList[i], 24)
                    cust = collapseSlotTensor(cust, 1, ax2, timePoints, timePointsY, plotCriteria)
                    cust = np.sum(X, axis=0, keepdims=True)
                    if plotCriteria == 'binary':
                        cust[np.where(cust>0)]=1  

                    distances[i] = distance(X, cust, metric)
                    #cust = loadViewCustomer(filename,custIndexList[i])
                    #cust = collapseSlotTensor(cust, ax1, ax2, timePoints, timePointsY, plotCriteria)
                    
            
            elif ax1 == 6 or ax2 == 6:
                slots = similar_data['slots']
                timePoints = []
                timePointsY = []
                for i in range(len(slots)):
                    timePoints.append(int(slots[i]["x"]))
                    timePointsY.append(int(slots[i]["y"]))
                
                dimensions = np.array([1,1,1,1,0])
                if ax1 == 6:
                    dimensions[2] = 0
                    dimensions[ax2] = 0
                if ax2 == 6:
                    dimensions[ax1] = 0
                    dimensions[2] = 0
                
                if (dimensions==np.array([0,1,0,1,0])).all():
                    filename = 'files/whc_%d.mat'%CUSTOMERCOUNT
                elif (dimensions==np.array([1,0,0,1,0])).all():
                    filename = 'files/dhc_%d.mat'%CUSTOMERCOUNT
                else:
                    filename = 'files/hic_%d.mat'%CUSTOMERCOUNT
               
                X = loadViewCustomer(filename,customerIndex)
                X = collapseSlotTensor(X, ax1, ax2, timePoints, timePointsY, plotCriteria)
    
                if searchType == 0:
                    profileCustCount = CUSTOMERCOUNT
                    custIndexList = np.arange(CUSTOMERCOUNT)
                    
                else:
                    profileId = similar_data['ProfileId']
                    profileDs = similar_data['ProfileDs']
                    
                    filename2 = "files/profileFiles/ProfileCustomers_%s_%d.txt" % (profileDs, profileId)

                    json_data=open(filename2).read()
                    customersData = json.loads(json_data)

                    profileCustCount = 150
                    profileCustomers = customersData[0:profileCustCount]

                    #customerIdsList = []
                    custIndexList = []
                    for cust in profileCustomers:
                        #customerIdsList.append(cust['id'])
                        custIndexList.append(np.where(EtailerSelectedCustomerIndex2Id==cust['id'])[0][0])
                    custIndexList = np.array(custIndexList)
                 
                distances = np.zeros(len(custIndexList))
                for i in range(len(custIndexList)):
                    cust = loadViewCustomer(filename,custIndexList[i])
                    cust = collapseSlotTensor(cust, ax1, ax2, timePoints, timePointsY, plotCriteria)
                    distances[i] = distance(X, cust, metric)
                    
            else:
                
                dimensions = np.array([1,1,1,1,0])
                dimensions[ax1] = 0
                dimensions[ax2] = 0
                
                if (dimensions==np.array([0,0,1,1,0])).all() or (dimensions==np.array([0,1,1,1,0])).all():
                    filename = 'files/wdc_%d.mat'%CUSTOMERCOUNT
                elif (dimensions==np.array([0,1,0,1,0])).all():
                    filename = 'files/whc_%d.mat'%CUSTOMERCOUNT
                elif (dimensions==np.array([0,1,1,0,0])).all():
                    filename = 'files/wic_%d.mat'%CUSTOMERCOUNT
                elif (dimensions==np.array([1,0,0,1,0])).all() or (dimensions==np.array([1,0,1,1,0])).all() or (dimensions==np.array([1,1,0,1,0])).all():
                    filename = 'files/dhc_%d.mat'%CUSTOMERCOUNT
                elif (dimensions==np.array([1,0,1,0,0])).all() or (dimensions==np.array([1,1,1,0,0])).all():
                    filename = 'files/dic_%d.mat'%CUSTOMERCOUNT
                else:
                    filename = 'files/hic_%d.mat'%CUSTOMERCOUNT
                    
                
                X = loadViewCustomer(filename,customerIndex)
                X = collapseTensor(X, dimensions, plotCriteria)

                if searchType == 0:
                    profileCustCount = CUSTOMERCOUNT
                    custIndexList = np.arange(CUSTOMERCOUNT)
                    
                else:
                    profileId = similar_data['ProfileId']
                    profileDs = similar_data['ProfileDs']
                    
                    filename2 = "files/profileFiles/ProfileCustomers_%s_%d.txt" % (profileDs, profileId)

                    json_data=open(filename2).read()
                    customersData = json.loads(json_data)

                    profileCustCount = 150
                    profileCustomers = customersData[0:profileCustCount]

                    #customerIdsList = []
                    custIndexList = []
                    for cust in profileCustomers:
                        #customerIdsList.append(cust['id'])
                        custIndexList.append(np.where(EtailerSelectedCustomerIndex2Id==cust['id'])[0][0])
                    custIndexList = np.array(custIndexList)
   

                distances = np.zeros(len(custIndexList))
                for i in range(len(custIndexList)):
                    cust = loadViewCustomer(filename,custIndexList[i])
                    cust = collapseTensor(cust, dimensions, plotCriteria)

                    distances[i] = distance(X, cust, metric)

                
                global tempRes
                tempRes = distances

                #distances = distances + np.ones((1000))
                #beta = 0.1
                #distances = np.exp(-beta * distances)
            
            
            indices = distances.argsort()
            sortedDistances = np.sort(distances)
            sortedDistances = - sortedDistances
            percentages = (100 * np.ones(len(custIndexList))) - ( sortedDistances * 100 / np.min(sortedDistances) )

            customerIds = []
            for i in range(len(custIndexList)):
                customerIds.append(EtailerSelectedCustomerIndex2Id[custIndexList[indices[i]]])
            customerIds = np.array(customerIds)
            
            #customerIds = EtailerSelectedCustomerIndex2Id[indices]
            
            
            count = 0
            data = []
            for i in range(len(customerIds)):
                if count < numCustomers:
                    if int(percentages[i])>= minPercentage:
                        data2 = {}
                        data2['percentage'] = int(percentages[i])
                        data2['distances'] = - int(sortedDistances[i])
                        data2['id'] = int(customerIds[i])

                        data.append(data2)
                        count = count+1

            ###
            abc = True
            if abc:
                filename = "files/1_1_1_7269_3392_TensorEst.txt"
                
                if numRecBase == 0:
                    numPeople = len(customerIds)
                else:
                    numPeople = min(len(customerIds),numRecBase)
                
                retMatrix = loadRecommendationOfCustomerProfilesFromTxt(filename, customeridss, customerIds[0:numPeople])

                row,col = retMatrix.shape
                asd = np.argsort(retMatrix.toarray())
                asd = asd[:,col-numRecItems:col]
                itemIndices = list(asd.flatten())
                
                visited = set()
                count = {}

                for i in range(len(itemIndices)):
                    itemIndex = itemIndices[i]

                    if itemIndex not in visited:
                        visited.add(itemIndex)
                        count[str(itemIndex)] = 1 / row
                    else:
                        count[str(itemIndex)] = count[str(itemIndex)] + 1 / row

                recIndexList=sorted(count.items(), key=lambda x: x[1])[::-1]

                productIds = []
                productPercentages = []
                for i in range(len(recIndexList)):
                    productIds.append(itemids[int(recIndexList[i][0])])
                    perc = recIndexList[i][1] * 100 
                    productPercentages.append(perc)
                
                
            else:
            ###
                productIndices = np.random.randint(6000, size=numRecItems)
                productIds = itemIds[productIndices]
            
                productPercentages = np.random.randint(50, size=(numRecItems)) + 50
                productPercentages = np.sort(productPercentages,axis=0)[::-1].flatten()
            ###
            
            productsData = []
            for i in range(numRecItems):
                data2 = {}
                data2['id'] = int(productIds[i])
                data2['percentage'] = int(productPercentages[i])
                productsData.append(data2)

            json_data = json.dumps({"Customers": data, "Products": productsData, "MinDistance": -int(np.max(sortedDistances)), "MaxDistance": -int(np.min(sortedDistances))})

            self.write(json_data)  
            
            
            global tempIndices
            tempIndices = indices
            
            global tempPerc
            tempPerc = percentages
            
            global Dist
            Dist = distances
 
# localhost:8880/recommendProducts?jsonData={"id": 737293, "type": "mix", "Count":10}
class RecommendProducts(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        rec_data = json.loads(temp)
        
        customerId = int(rec_data['id'])
        numRecItems = int(rec_data['Count'])
        criteria = rec_data['type']
        
        
        customerIndex = np.where(EtailerSelectedCustomerIndex2Id==customerId)[0][0]
        
        customerSales = EtailerMatrix[customerIndex,:]
        customerSalesEst = EtailerMatrixEst[customerIndex,:]
            
        
        
        if criteria != 'mix':
            realItemIndices = np.where(customerSales>0)
            realItemIndices = realItemIndices[0]

            recItemIndicesOrder = np.argsort(customerSalesEst)[::-1]
            recItemIndices = []

            if criteria == 'discover':
                for i in range(len(recItemIndicesOrder)):
                    if recItemIndicesOrder[i] not in realItemIndices:
                        recItemIndices.append(recItemIndicesOrder[i])
            else:
                for i in range(len(recItemIndicesOrder)):
                    if recItemIndicesOrder[i] in realItemIndices:
                        recItemIndices.append(recItemIndicesOrder[i])

            if(len(recItemIndices)>0):
                recItemIndices = np.array(recItemIndices) 
                recItemIndices = recItemIndices[0:numRecItems]
            
        else:
            recItemIndices = np.argsort(customerSalesEst)[::-1][0:numRecItems]
        
        if(len(recItemIndices)==0):
            self.write("Criteria changed to: Mix")
            recItemIndices = np.argsort(customerSalesEst)[::-1][0:numRecItems]
        

        recProductIds = itemIdsGroup3[recItemIndices]
            
        data = []
        for i in range(len(recProductIds)):
            data2 = {}
            data2['id'] = int(recProductIds[i])
            #data2['index'] = int(recItemIndices[i])
            data.append(data2)

        json_data = json.dumps({"Products": data})

        self.write(json_data)  
        
        #plt.figure(num=None, figsize=(7,4), dpi=80)
        #plt.bar(np.arange(len(customerSales)), customerSales, color='b')
        #plt.xlabel('Items')
        #plt.title('Sales of Customer %d' % customerId)
        #plt.savefig('./files/%d.png' % customerId)
        
        #plt.figure(num=None, figsize=(7,4), dpi=80)
        #plt.bar(np.arange(len(customerSalesEst)), customerSalesEst, color='b')
        #plt.xlabel('Items')
        #plt.title('Sales Estimation of Customer %d' % customerId)
        #plt.savefig('./files/%d_Est.png' % customerId)
        
        
        #self.write('<html>'
        #           '<br><img src=\"/files/%d.png\"><br>' 
        #           '<img src=\"/files/%d_Est.png\"><br></body></html>' % (customerId,customerId))
  
class RecommendProducts2(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        temp = self.get_argument('jsonData')
        rec_data = json.loads(temp)
        
        customerId = int(rec_data['id'])
        numRecItems = int(rec_data['Count'])
        criteria = rec_data['type']
        
        
        customerIndex = np.where(customeridss==customerId)[0][0] 
        customerSales = PurchaseMatrix[customerIndex,:].toarray()
        
        filename = "files/1_1_1_7269_3392_TensorEst.txt"
        customerSalesEst = loadRecommendationOfCustomerMatrixFromTxt2(filename, customerIndex).toarray()

        #customerSalesEst = PurchaseMatrixEst[customerIndex,:]
            
        if criteria != 'mix':
            realItemIndices = np.where(customerSales[0]>0)
            realItemIndices = realItemIndices[0]

            recItemIndicesOrder = np.argsort(customerSalesEst[0])[::-1]
            recItemIndices = []
            
            if criteria == 'discover':
                for i in range(len(recItemIndicesOrder)):
                    if recItemIndicesOrder[i] not in realItemIndices:
                        recItemIndices.append(recItemIndicesOrder[i])
            else:
                for i in range(len(recItemIndicesOrder)):
                    if recItemIndicesOrder[i] in realItemIndices:
                        recItemIndices.append(recItemIndicesOrder[i])

            if(len(recItemIndices)>0):
                #recItemIndices = np.array(recItemIndices) 
                recItemIndices = recItemIndices[0:numRecItems]
            
        else:
            #recItemIndices = np.argsort(customerSalesEst)[::-1][0:numRecItems]
            recItemIndices = np.argsort(customerSalesEst[0])[::-1]
            recItemIndices = recItemIndices[0:numRecItems]
            
        if(len(recItemIndices)==0):
            self.write("Criteria changed to: Mix")
            #recItemIndices = np.argsort(customerSalesEst)[::-1][0:numRecItems]
            recItemIndices = np.argsort(customerSalesEst[0])[::-1]
            recItemIndices = recItemIndices[0:numRecItems]
            

        global itemids
        recProductIds = itemids[recItemIndices]
            
        data = []
        for i in range(len(recProductIds)):
            data2 = {}
            data2['id'] = int(recProductIds[i])
            data.append(data2)

        json_data = json.dumps({"Products": data})

        self.write(json_data)  


# The configuration of routes.
routes_config = [
    (r"/", MainPage), 
    (r"/defineProfile", DefineProfile),
    (r"/defineProducts", DefineProducts),
    (r"/midResults", MidResults),
    (r"/customersOfProfile", CustomersOfProfile),
    (r"/customerSalesMap", CustomerSalesMap),
    (r"/similarCustomers", similarCustomers),
    (r"/customerWeblog", CustomerWeblogPlots),
    (r"/recommendProducts", RecommendProducts),
    (r"/recommendProducts2", RecommendProducts2),
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

    
    
# localhost:8880/similarCustomers?jsonData={"id": 1279930,"xAxis":6,"yAxis": 1,"type": 2,"distanceType":0,"Count":15,"MinPercentage":0, "productCount": 20, "baseCount": 50, "searchType": 1, "ProfileId": 11, "ProfileDs": "Bebek", "slots": [{"x": 0,"y": 8},{"x": 8,"y": 16},{"x": 16,"y": 24}]}
# localhost:8880/customerSalesMap?jsonData={"id": 90412, "xAxis":0, "yAxis": 6, "type": 1, "slots": [{"x": 0,"y": 8},{"x": 8,"y": 16},{"x": 16,"y": 24}]} 