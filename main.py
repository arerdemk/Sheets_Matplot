from dataclasses import replace
from unicodedata import name
import gspread
from gspread import worksheet
from gspread.worksheet import Worksheet
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split



class findaTOF:
    def __init__(self,tablo):
        self.tablo=tablo

        sheet_id='1Bz9u_6UoFJg6AoXuF0D1XmkiEwnASg6ouqIk_oQqp6Q'
        gc=gspread.service_account('credentials.json')
        sh=gc.open_by_key(sheet_id)

        worksheet=sh.sheet1
        res=worksheet.get(self.tablo)
        
        df=pd.DataFrame(res, columns=['min','cm','mL (H2+CO2)','mL (H2)','TOF h-1'])
        self.tablo=df.loc[3:,:]

        
    

    def draw_plot(self):
        x=self.tablo['min'].astype(float)
        y=self.tablo['mL (H2)'].astype(float)

        x_constant=sm.add_constant(x)
        lineermodel=sm.OLS(y,x_constant).fit()
        print(lineermodel.summary())

        # x=x.le(28).astype(float)
        # print(x)

        #====TREND LINE======
        coeff=np.polyfit(x,y,1)
        m=coeff[0].round(2)
        b=coeff[1].round(2)


        lineq=('Lineer Equation: {}x {}'.format(m,b)) #y = mx + b
        desired_gas=28
        realesed_time=(28*m) + b
        TOF_value= ((1*((desired_gas/1000))/(0.082*298))/((0.0000188*(realesed_time/2/60))))
        #formulde 60 (1 saat>dk) yerine 120 yazdim cunku h2 lazim bana o da h2+c02'nin yarisi
        TOFdegeri=('TOF:', TOF_value)
        rsquare=(r2_score(x,y))
        
        dataname=self.tablo.iloc[7]

        self.tablo.plot(kind='scatter', x='min', y='mL (H2+CO2)')

        #plt.gca().invert_yaxis() #super kod y eksenini 0'dan baslatti

        #plt.title('{} {}'.format(dataname,TOFdegeri)) BUNABAKKK
        plt.text(0,2, lineq)
        plt.text(0,1.5,rsquare)
        plt.xticks(rotation='vertical')
        plt.show()

    # def ML(self):
    #     x=self.tablo['mL (H2+CO2)'].astype(float)
    #     y=self.tablo['TOF h-1'].astype(float)
        
    #     x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=2)
    #     reg=LinearRegression()
    #     reg.fit(x_train,y_train)

    #     a=reg.score(x_train,y_train)
    #     b=reg.score(x_test,y_test)
    #     print(a,b)

    #     yeniveri=np.array([28])
    #     c=reg.predict(yeniveri)
    #     print(c)


    # ne buuuuuuu

        

#a=input('gir: ') inputlu olabilir!!      
oe1=findaTOF('oeuc')
oe1.draw_plot()






