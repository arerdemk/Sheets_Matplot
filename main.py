from dataclasses import replace
from unicodedata import name
import gspread
from gspread import worksheet
from gspread.worksheet import Worksheet
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np




class findaTOF:
    def __init__(self,tablo):
        self.tablo=tablo

        sheet_id='1Bz9u_6UoFJg6AoXuF0D1XmkiEwnASg6ouqIk_oQqp6Q'
        gc=gspread.service_account('credentials.json')
        sh=gc.open_by_key(sheet_id)

        worksheet=sh.sheet1
        res=worksheet.get(self.tablo)
        
        df=pd.DataFrame(res, columns=['min','cm','mL (H2+CO2)','mL (H2)','TOF h-1'])
        self.tablo=df.loc[3:,:] #baslangictaki katalizor ismi cismi vs vilgiler drop edildir

        Volume_of_Gas=self.tablo['mL (H2)'].astype(float) #row secmede hangi column'a gore yapilacagi ayarlandi
        Desired_Volume_of_Gas_row=self.tablo[Volume_of_Gas>5].index[0] #istenilan gaz degeri loc edildi
        
        Desired_Volume_of_Gas=self.tablo.loc[[Desired_Volume_of_Gas_row-1,Desired_Volume_of_Gas_row,Desired_Volume_of_Gas_row+1]]# duzgun regresyon icin 3 row alindi
        
        # print(Desired_Volume_of_Gas)

        #========MATRISE GEC=====
        create_matris_gas_unshaped=Desired_Volume_of_Gas['mL (H2)'].to_numpy()
        create_matris_min_unshaped=Desired_Volume_of_Gas['min'].to_numpy()
        matris_gas=np.reshape(create_matris_gas_unshaped,(1,3)).astype(float)
        matris_min=np.reshape(create_matris_min_unshaped,(3,1)).astype(float)
        #========MATRISE GEC=====

        print(matris_gas)
        print(matris_min)
        print(matris_gas*matris_min)
        




        # #========GRAPHIC=========
        # Desired_Volume_of_Gas.plot(kind='scatter',x='min',y='mL (H2)')
        # plt.show()
        # #========GRAPHIC=========
      

        

#a=input('gir: ') inputlu olabilir!!      
oe1=findaTOF('oeuc')
