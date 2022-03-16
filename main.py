import csv
import gspread
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

class findaTOF:
    def __init__(self,tablo):
        self.tablo=tablo

        sheet_id='1B2Tm7H9Te8pbxRSDsHUdpDf8YIwREjXs75K6fnce90s'
        gc=gspread.service_account('tubitak-121z085.json')
        sh=gc.open_by_key(sheet_id)

 
        worksheet=sh.sheet1
        res=worksheet.get(self.tablo)
        
        df=pd.DataFrame(res, columns=['min','cm','mL (H2+CO2)','mL (H2)','TOF h-1'])
        self.tablo=df.loc[3:,:] #baslangictaki katalizor ismi cismi vs vilgiler drop edildir

        Volume_of_Gas=self.tablo['mL (H2)'].astype(float) #row secmede hangi column'a gore yapilacagi ayarlandi
        Desired_Volume_of_Gas_row=self.tablo[Volume_of_Gas>5].index[0] #istenilan gaz degeri loc edildi
        
        Desired_Volume_of_Gas=self.tablo.loc[[Desired_Volume_of_Gas_row-1,Desired_Volume_of_Gas_row,Desired_Volume_of_Gas_row+1]]# daha iyi sonuclu regresyon icin 3 row alindi
     
        create_df_gas=Desired_Volume_of_Gas['mL (H2)']
        create_df_min=Desired_Volume_of_Gas['min']
        #========MATRISE GEC=====
        
        create_matris_gas_unshaped=Desired_Volume_of_Gas['mL (H2)'].to_numpy()
        create_matris_min_unshaped=Desired_Volume_of_Gas['min'].to_numpy()
        matris_gas=np.reshape(create_matris_gas_unshaped,(1,3)).astype(float)
        matris_min=np.reshape(create_matris_min_unshaped,(1,3)).astype(float)


        print(create_df_min,'\n',create_df_gas)           

        #========MATRISE GEC=====



    


        # #========GRAPHIC=========
        # Desired_Volume_of_Gas.plot(kind='scatter',x='min',y='mL (H2)')
        # plt.show()
        # #========GRAPHIC=========


with open('g-CN(U).txt') as f:

    lines=f.readlines()
    

    for row in lines:
        a=row.rstrip('\n')

        findaTOF(a)
    f.close()
