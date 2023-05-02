from django.shortcuts import render,HttpResponse

# Create your views here.

'''def show(response):
    return HttpResponse("Hello super World")'''


import numpy as np
from PIL import Image
from rest_framework.decorators import api_view
from rest_framework.response import Response


import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from itertools import product as prod
#import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

config = {
    "apiKey": "AIzaSyD3-PWr4q4au-UV62mpgH5eLaklss52tJc",
    "authDomain": "pythonconnect-46c79.firebaseapp.com",
    "projectId": "pythonconnect-46c79",
    "storageBucket": "pythonconnect-46c79.appspot.com",
    "messagingSenderId": "594544396292",
    "appId": "1:594544396292:web:6afd1b0cc5bc62e0b54d51",
    "measurementId": "G-H1299SM7WD",
    "serviceAccount": "service_account_key.json",
    "databaseURL": "https://pythonconnect-46c79-default-rtdb.firebaseio.com/"
    }

 #getdata from firebase
cred = credentials.Certificate("service_account_key.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://pythonconnect-46c79-default-rtdb.firebaseio.com/'
}
)

@api_view(['GET'])
def temperature_map(request):
    

    

   

    def patchcreator(xspatch,xepatch,yspatch,yepatch):
        xline=[]
        yline=[]
        scalex=100               
        scaley=100
        #FOR THE LIST XLINE                                                                         
        for i in range(int(scalex*xspatch), int(scalex*xepatch), int(scalex*0.01)) :
            el=(i)/scalex
            xline.append(el)
        #FOR THE LIST YLINE
        for i in range(int(scaley*yspatch), int(scaley*yepatch), int(scaley*0.01)) :
            el=(i)/scaley
            yline.append(el)

        patchcord=list(prod(xline,yline))
        #DEFINING COORDINATES INSIDE PATCH
        xval=[]
        yval=[]
        for el in patchcord:
            xval.append(el[0])
            yval.append(el[1])
        return xval,yval

    def patchcolordecide(pval):
        #OVER A SINGLE PATCH, THE PRESSURE READINGS MAY BE CONSTANT
        if pval in range(0,75):
            pclr='blue'
        elif pval in range(76,120):
            pclr='greenyellow'
        elif pval in range(121,160):
            pclr='red'
        else:
            pclr='black'
        return pclr


    pval=[]
    ref = db.reference('fsrForce1/data')
    print(ref.get())
    pval.append(ref.get())
    ref = db.reference('fsrForce2/data')
    print(ref.get())
    pval.append(ref.get())
    ref = db.reference('fsrForce3/data')
    print(ref.get())
    pval.append(ref.get())
    ref = db.reference('fsrForce4/data')
    print(ref.get())
    pval.append(ref.get())
    ref = db.reference('fsrForce5/data')
    print(ref.get())
    pval.append(ref.get())
    print(pval)

    for i in range(0,len(pval)):
        force=(pval[i]/10)*150
        pval[i]=force
    print(pval)

    plt.rcParams["figure.figsize"]=[7.00,3.50]
    plt.rcParams["figure.autolayout"]= True
    im=plt.imread("left_foot.jpeg")
    fig,ax=plt.subplots(2,1,figsize=(10,10), gridspec_kw={'height_ratios': [7, 1]})
    im=ax[0].imshow(im,extent=[0,10,0,10])
    xl1,yl1=patchcreator(2.26,6.00,1.15,2.69)    #BOTTOM SQUARE
    xl2,yl2=patchcreator(4.36,6.90,4.58,6.16)   #MIDDLE SQUARE
    patch1=plt.Circle((8.25,8.88),0.65,facecolor=patchcolordecide(pval[0]),label='1')
    patch2=plt.Circle((5.52,9.02),0.55,facecolor=patchcolordecide(pval[1]),label='2')
    patch3=plt.Circle((2.73,8.25),0.55,facecolor=patchcolordecide(pval[2]),label='3')
    patch4=patches.Rectangle((4.36,4.58),2.7,2,color=patchcolordecide(pval[3]),label='4')
    patch5=patches.Rectangle((2.26,1.15),3.5,2,color=patchcolordecide(pval[4]),label='5')
    ax[0].add_patch(patch1)
    ax[0].add_patch(patch2)
    ax[0].add_patch(patch3)
    ax[0].add_patch(patch4)
    ax[0].add_patch(patch5)
    ##plt.legend(handles=[patch1,patch2,patch3,patch4,patch5])


    ax[0].text(8.23,8.78,'1',fontsize = 16)
    ax[0].text(5.44,9.00,'2',fontsize = 16)
    ax[0].text(2.64,8.22,'3',fontsize = 16)
    ax[0].text(5.56,5.50,'4',fontsize = 20)
    ax[0].text(3.92,2.00,'5',fontsize = 20)
    norm=mpl.colors.Normalize(vmin=0,vmax=150)
    presscbr=mpl.colorbar.ColorbarBase(ax[1],cmap='jet',norm=norm,orientation='horizontal')
    presscbr.set_label("Force (in Newtons)")

    #plt.show()

    plt.savefig("response.png")
    r = Image.open('response.png')
    response = HttpResponse(content_type="image/png")
    r.save(response,'png')
  
    return response
