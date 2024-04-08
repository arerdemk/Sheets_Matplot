import gspread
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sheet_id='1B2Tm7H9Te8pbxRSDsHUdpDf8YIwREjXs75K6fnce90s'
gc=gspread.service_account('tubitak-121z085.json')
sh=gc.open_by_key(sheet_id)
worksheet=sh.sheet1

with open('GCN.txt') as f:
    lines=f.readlines()
    f.close()

class findaTOF:
    def __init__(self,tablo):
        self.tablo=tablo

        res=worksheet.get(self.tablo)     
        
        df=pd.DataFrame(res, columns=['min','cm','mL (H2+CO2)','mL (H2)','TOF h-1'])
        
        self.tablo=df.loc[3:,:] #baslangictaki katalizor ismi cismi vs vilgiler drop edildir
        Volume_of_Gas=self.tablo['mL (H2)'].astype(float) #row secmede hangi column'a gore yapilacagi ayarlandi


        Desired_Volume_of_Gas_row=self.tablo[Volume_of_Gas>5].index[0] #istenilan gaz degeri loc edildi       
        Desired_Volume_of_Gas=self.tablo.loc[[Desired_Volume_of_Gas_row-1,Desired_Volume_of_Gas_row,Desired_Volume_of_Gas_row+1]]# daha iyi sonuclu regresyon icin 3 row alindi
        
        triple_combine=pd.DataFrame(data=Desired_Volume_of_Gas,columns=['min','mL (H2)'])      
        print(triple_combine)     
            #==== to CSV======
        out_to_csv=triple_combine.to_csv(header=None,index=None,sep=',')
            #==== to CSV======
        create_csv=open('GCN.csv','a')
        create_csv.write(out_to_csv)

class sort_cat:
    def __init__(self,tablo):
        self.tablo=tablo
        res=worksheet.get(self.tablo)     
        
        df=pd.DataFrame(res, columns=['min','cm','mL (H2+CO2)','mL (H2)','TOF h-1'])
        self.tablo=df.loc[3:,:] #baslangictaki katalizor ismi cismi vs vilgiler drop edildir
        Volume_of_Gas=self.tablo['mL (H2)'].tail(1).astype(float).to_csv(header=None,index=None,) #son row secildi
                

        create_csv=open('GCN_SORT.csv','a')
        create_csv.write(Volume_of_Gas)

def call_data():
          
    for row in lines:
        read_row=row.rstrip('\n')
        sort_cat(read_row)
                

def sort_catal():
    a=pd.read_csv('GCN.txt')

    b=pd.read_csv("GCN_SORT.csv").astype(float)

    c=pd.concat([a,b],axis=1)   #buraya oyle birsey buldu NaN'dan kurtul

    new=pd.DataFrame(data=c,columns=['catal','gas'])


    print(c.head(22))

def merge_plot():
    print('sa')
    

findaTOF('GCN_Urea_AgPd_Hidrazin')
