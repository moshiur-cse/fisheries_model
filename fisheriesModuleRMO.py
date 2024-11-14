import numpy as np
import pandas as pd
#import random
import os
from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import LogisticRegression

#path=os.path

class FishProductionModuleClass():
    def __init__(self,datarootfolder):
        print("Location:",datarootfolder)

    def initializeModuleforRun(self):
        allDf = pd.read_csv('baseDataTest.csv')
        UpazilaNodeWiseProduction=pd.read_csv("UpazilaWiseProduction.csv")

        selectedUpzList=pd.read_csv('selectedUpzList.csv')

        finalData=pd.DataFrame();

       

        for singleUpazilaData in selectedUpzList.itertuples():
            df=allDf[allDf['THACODE']==singleUpazilaData.THACODE]            
            #print(singleUpazilaData.THACODE)

            #Observed Condition
            df['MAF_Qsec']=df['Qsec'].mean()
            df['MAXF_Qsec']=df['Qsec'].max()
            df['MINF_Qsec']=df['Qsec'].min()

            df['MAX_WD']=df['WD'].max()
            df['MIN_WD']=df['WD'].min()

            df['MAX_MAXTemp']=df['Wtemp_MAX'].max()
            df['MIN_MAXTemp']=df['Wtemp_MAX'].min()
            df['MAX_MINTemp']=df['Wtemp_MIN'].max()
            df['MIN_MINTemp']=df['Wtemp_MIN'].min()

            df['Q_200%MAF']=df['MAF_Qsec']*2
            df['Q_100%MAF']=df['MAF_Qsec']*1
            df['Q_60%MAF']=df['MAF_Qsec']*0.60
            df['Q_50%MAF']=df['MAF_Qsec']*0.50
            df['Q_40%MAF']=df['MAF_Qsec']*0.40
            df['Q_30%MAF']=df['MAF_Qsec']*0.30
            df['Q_25%MAF']=df['MAF_Qsec']*0.25
            df['Q_10%MAF']=df['MAF_Qsec']*0.10
            df['Critical_WD_m']=((0.98*2.2)/3.14)*1.5

            #Occurance of Condtion : (df['Qsec']>=df['Q_200%MAF'],1,0)

            df['Q_200%MAF_OC']=np.where(df['Qsec']>=df['Q_200%MAF'], 1, 0)

            df['Q_100%MAF_OC']=np.where(df['Qsec']>=df['Q_100%MAF'], 1, 0)
            df['Q_60%MAF_OC']=np.where(df['Qsec']>=df['Q_60%MAF'], 1, 0)
            df['Q_50%MAF_OC']=np.where(df['Qsec']>=df['Q_50%MAF'], 1, 0)
            df['Q_40%MAF_OC']=np.where(df['Qsec']>=df['Q_40%MAF'], 1, 0)
            df['Q_30%MAF_OC']=np.where(df['Qsec']>=df['Q_30%MAF'], 1, 0)
            df['Q_25%MAF_OC']=np.where(df['Qsec']>=df['Q_25%MAF'], 1, 0)
            df['Q_10%MAF_OC']=np.where(df['Qsec']>=df['Q_10%MAF'], 1, 0)   

            df['WD>10m_OC']=np.where(df['WD']>=10, 1, 0)
            df['WD>5m_OC']=np.where(df['WD']>=5, 1, 0)
            df['WD>1m_OC']=np.where(df['WD']>=1, 1, 0)
            df['WD>0.5m_OC']=np.where(df['WD']>=0.5, 1, 0)
            df['WD>0.25m_OC']=np.where(df['WD']>=0.25, 1, 0)

            df['Critical_WD_m_OC']=np.where(df['WD']>=df['Critical_WD_m'], 1, 0)

            df['Wtemp_MAX<30C_OC']=np.where(df['Wtemp_MAX']<30, 1, 0)
            df['Wtemp_MIN>5C_OC']=np.where(df['Wtemp_MIN']>5, 1, 0)
            
            #Condtional Probability (Suitable Condition/Day): Suitable Condition Occurred/Total Suitable Condition Occurred	
                                                                    
            #=(Q_200%MAF_OC/Occurrence no of Q_200%MAF_OC)/(Occurrence no of Q_200%MAF_OC/Sum of Occurrence= 1)
            sumOfOccurance=( len(df[df['Q_200%MAF_OC']>0])+len(df[df['Q_100%MAF_OC']>0])+len(df[df['Q_60%MAF_OC']>0])+len(df[df['Q_50%MAF_OC']>0])+len(df[df['Q_40%MAF_OC']>0])+len(df[df['Q_30%MAF_OC']>0])+len(df[df['Q_25%MAF_OC']>0])+len(df[df['Q_10%MAF_OC']>0])+len(df[df['WD>10m_OC']>0])+len(df[df['WD>5m_OC']>0]) +len(df[df['WD>1m_OC']>0])+len(df[df['WD>0.5m_OC']>0])+len(df[df['WD>0.25m_OC']>0])+len(df[df['Critical_WD_m_OC']>0])+len(df[df['Wtemp_MAX<30C_OC']>0])+len(df[df['Wtemp_MIN>5C_OC']>0]))
            
            df['Q_200%MAF_CP']=(df['Q_200%MAF_OC']/len(df[df['Q_200%MAF_OC']>0]))/(len(df[df['Q_200%MAF_OC']>0])/sumOfOccurance)
            df['Q_100%MAF_CP']=(df['Q_100%MAF_OC']/len(df[df['Q_100%MAF_OC']>0]))/(len(df[df['Q_100%MAF_OC']>0])/ sumOfOccurance)
            df['Q_60%MAF_CP']=(df['Q_60%MAF_OC']/len(df[df['Q_60%MAF_OC']>0]))/(len(df[df['Q_60%MAF_OC']>0])/ sumOfOccurance)
            df['Q_50%MAF_CP']=(df['Q_50%MAF_OC']/len(df[df['Q_50%MAF_OC']>0]))/(len(df[df['Q_50%MAF_OC']>0])/ sumOfOccurance)
            df['Q_40%MAF_CP']=(df['Q_40%MAF_OC']/len(df[df['Q_40%MAF_OC']>0]))/(len(df[df['Q_40%MAF_OC']>0])/ sumOfOccurance)
            df['Q_30%MAF_CP']=(df['Q_30%MAF_OC']/len(df[df['Q_30%MAF_OC']>0]))/(len(df[df['Q_30%MAF_OC']>0])/ sumOfOccurance)
            df['Q_25%MAF_CP']=(df['Q_25%MAF_OC']/len(df[df['Q_25%MAF_OC']>0]))/(len(df[df['Q_25%MAF_OC']>0])/ sumOfOccurance)
            df['Q_10%MAF_CP']=(df['Q_10%MAF_OC']/len(df[df['Q_10%MAF_OC']>0]))/(len(df[df['Q_10%MAF_OC']>0])/ sumOfOccurance)

            df['WD>10m_CP']=(df['WD>10m_OC']/len(df[df['WD>10m_OC']>0]))/(len(df[df['WD>10m_OC']>0])/ sumOfOccurance)
            df['WD>5m_CP']=(df['WD>5m_OC']/len(df[df['WD>5m_OC']>0]))/(len(df[df['WD>5m_OC']>0])/ sumOfOccurance)
            df['WD>1m_CP']=(df['WD>1m_OC']/len(df[df['WD>1m_OC']>0]))/(len(df[df['WD>1m_OC']>0])/ sumOfOccurance)
            df['WD>0.5m_CP']=(df['WD>0.5m_OC']/len(df[df['WD>0.5m_OC']>0]))/(len(df[df['WD>0.5m_OC']>0])/ sumOfOccurance)
            df['WD>0.25m_CP']=(df['WD>0.25m_OC']/len(df[df['WD>0.25m_OC']>0]))/(len(df[df['WD>0.25m_OC']>0])/ sumOfOccurance)
        
            df['Critical_WD_m_CP']=(df['Critical_WD_m_OC']/len(df[df['Critical_WD_m_OC']>0]))/(len(df[df['Critical_WD_m_OC']>0])/ sumOfOccurance)
            
            df['Wtemp_MAX<30C_CP']=(df['Wtemp_MAX<30C_OC']/len(df[df['Wtemp_MAX<30C_OC']>0]))/(len(df[df['Wtemp_MAX<30C_OC']>0])/ sumOfOccurance)       
            df['Wtemp_MIN>5C_CP']=(df['Wtemp_MIN>5C_OC']/len(df[df['Wtemp_MIN>5C_OC']>0]))/(len(df[df['Wtemp_MIN>5C_OC']>0])/ sumOfOccurance)
            
            #print(len(df[df['Q_10%MAF_OC']>0]))
            #print( sumOfOccurance)
            
            #Probability of the Suitable Day (Day/Suitable Condition): [P(D) * P(Condition/Day)]/P(Suitable Condition)	
            # 
            # 1/total no of element 	len(df[df['Wtemp_MIN>5C_OC']>0])	
            sumOfTotalOccurance=(len(df['Q_200%MAF_OC'])*16)

            df['PD']=1/len(df['Qsec'])
            
            df['Q_200%MAF_PSD']=(df['Q_200%MAF_CP']*df['PD'])/(len(df[df['Q_200%MAF_OC']>0])/sumOfTotalOccurance)
            df['Q_100%MAF_PSD']=(df['Q_100%MAF_CP']*df['PD'])/(len(df[df['Q_100%MAF_OC']>0])/sumOfTotalOccurance)
            df['Q_60%MAF_PSD']=(df['Q_60%MAF_CP']*df['PD'])/(len(df[df['Q_60%MAF_OC']>0])/sumOfTotalOccurance)
            df['Q_50%MAF_PSD']=(df['Q_50%MAF_CP']*df['PD'])/(len(df[df['Q_50%MAF_OC']>0])/sumOfTotalOccurance)
            df['Q_40%MAF_PSD']=(df['Q_40%MAF_CP']*df['PD'])/(len(df[df['Q_40%MAF_OC']>0])/sumOfTotalOccurance)
            df['Q_30%MAF_PSD']=(df['Q_30%MAF_CP']*df['PD'])/(len(df[df['Q_30%MAF_OC']>0])/sumOfTotalOccurance)
            df['Q_25%MAF_PSD']=(df['Q_25%MAF_CP']*df['PD'])/(len(df[df['Q_25%MAF_OC']>0])/sumOfTotalOccurance)
            df['Q_10%MAF_PSD']=(df['Q_10%MAF_CP']*df['PD'])/(len(df[df['Q_10%MAF_OC']>0])/sumOfTotalOccurance)

            df['WD>10m_PSD']=(df['WD>10m_CP']*df['PD'])/(len(df[df['WD>10m_OC']>0])/sumOfTotalOccurance)
            df['WD>5m_PSD']=(df['WD>5m_CP']*df['PD'])/(len(df[df['WD>5m_OC']>0])/sumOfTotalOccurance)
            df['WD>1m_PSD']=(df['WD>1m_CP']*df['PD'])/(len(df[df['WD>1m_OC']>0])/sumOfTotalOccurance)      
            df['WD>0.5_PSD']=(df['WD>0.5m_CP']*df['PD'])/(len(df[df['WD>0.5m_OC']>0])/sumOfTotalOccurance)
            df['WD>0.25_PSD']=(df['WD>0.25m_CP']*df['PD'])/(len(df[df['WD>0.25m_OC']>0])/sumOfTotalOccurance)
        
            df['Critical_WD_m__PSD']=(df['Critical_WD_m_CP']*df['PD'])/(len(df[df['Critical_WD_m_OC']>0])/sumOfTotalOccurance)
        
            df['Wtemp_MAX<30C_PSD']=(df['Wtemp_MAX<30C_CP']*df['PD'])/(len(df[df['Wtemp_MAX<30C_OC']>0])/sumOfTotalOccurance)
            df['Wtemp_MIN>5C_PSD']=(df['Wtemp_MIN>5C_CP']*df['PD'])/(len(df[df['Wtemp_MIN>5C_OC']>0])/sumOfTotalOccurance)
                
            #Normalization==(Qsec-df['MINF_Qsec'])/(df['MAXF_Qsec']-df['MINF_Qsec'])
            df['Conditional_Sum']=(df['Q_200%MAF_PSD']+df['Q_100%MAF_PSD']+df['Q_60%MAF_PSD']+df['Q_50%MAF_PSD']+df['Q_40%MAF_PSD']+df['Q_30%MAF_PSD']+df['Q_25%MAF_PSD']+df['Q_10%MAF_PSD']+df['WD>10m_PSD']+df['WD>5m_PSD']+df['WD>1m_PSD']+df['WD>0.5_PSD']+df['WD>0.25_PSD']+df['Critical_WD_m__PSD']+df['Wtemp_MAX<30C_PSD']+df['Wtemp_MIN>5C_PSD'])       
            df['Q_Normalization']=(df['Qsec']-df['MINF_Qsec'])/(df['MAXF_Qsec']-df['MINF_Qsec'])
            df['WD_Normalization']=(df['WD']-df['MIN_WD'])/(df['MAX_WD']-df['MIN_WD'])
            df['MAXWTemp_Normalization']=(df['Wtemp_MAX']- df['MIN_MAXTemp'])/(df['MAX_MAXTemp']- df['MIN_MAXTemp'])
            df['MINWTemp_Normalization']=(df['Wtemp_MIN']-df['MIN_MINTemp'])/(df['MAX_MINTemp']-df['MIN_MINTemp'])
            df['Habitat_Normalization']=df[['Q_Normalization','WD_Normalization','MAXWTemp_Normalization','MINWTemp_Normalization']].mean(axis=1)
            df['P_Suitability']=df['Habitat_Normalization']*df['Conditional_Sum']
            
            
            
            
            #print(len(df[df['Q_25%MAF_OC']>0]))
            #print(( sumOfOccurance))
            #print(df.head())		
            # 
            #Survivality due to Hydrological Condition

            df['S_Rui']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)
            df['S_Catla']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)
            df['S_Mrigal']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)
            df['S_Kalibaus']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)
            df['S_Bata']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)
            df['S_Gonia']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)
            df['S_Pangas']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)
            df['S_Boal_Air']=df.apply(lambda x: fishSurvivalCondition("S_Rui", x), axis=1)

            df['S_Shol_Gazar_Taki']=df.apply(lambda x: fishSurvivalCondition("S_Shol_Gazar_Taki", x), axis=1)
            df['S_Koi']=df.apply(lambda x: fishSurvivalCondition("S_Koi", x), axis=1)
            df['S_Shingi_Magur']=df.apply(lambda x: fishSurvivalCondition("S_Shingi_Magur", x), axis=1)
            df['S_Sarpunti']=df.apply(lambda x: fishSurvivalCondition("S_Sarpunti", x), axis=1)
            df['S_OtherInlandFish']=df.apply(lambda x: fishSurvivalCondition("S_OtherInlandFish", x), axis=1)
            df['S_Hilsa_Ilish']=df.apply(lambda x: fishSurvivalCondition("S_Hilsa_Ilish", x), axis=1)
            df['S_Galda']=df.apply(lambda x: fishSurvivalCondition("S_OtherInlandFish", x), axis=1)
            df['S_Bagda']=df.apply(lambda x: fishSurvivalCondition("S_OtherInlandFish", x), axis=1)
            df['S_Harina']=df.apply(lambda x: fishSurvivalCondition("S_OtherInlandFish", x), axis=1)
            df['S_Chaka']=df.apply(lambda x: fishSurvivalCondition("S_OtherInlandFish", x), axis=1)
            df['S_OtherSmallShrimp_Prawn']=df.apply(lambda x: fishSurvivalCondition("S_OtherInlandFish", x), axis=1)

            #THACODE Wise Fish _coef and _intercept value
            nodeWiseFish_coef_intercept=getNodeWiseFish_coef_intercept(df)
            #print(nodeWiseFish_coef_intercept.head())

            #Score 
            df['Score_Rui']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Rui'), axis=1)
            df['Score_Catla']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Catla'), axis=1)
            df['Score_Mrigal']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Mrigal'), axis=1)
            df['Score_Kalibaus']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Kalibaus'), axis=1)
            df['Score_Bata']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Bata'), axis=1)
            df['Score_Gonia']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Gonia'), axis=1)
            df['Score_Pangas']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Pangas'), axis=1)
            df['Score_Boal_Air']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Boal_Air'), axis=1)    
            df['Score_Shol_Gazar_Taki']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Shol_Gazar_Taki'), axis=1)
            df['Score_Koi']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Koi'), axis=1)
            
            df['Score_Shingi_Magur']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Shingi_Magur'), axis=1)
            
            df['Score_Sarpunti']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Sarpunti'), axis=1)
            df['Score_OtherInlandFish']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'OtherInlandFish'), axis=1)
            
            df['Score_Hilsa_Ilish']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Hilsa_Ilish'), axis=1)
            df['Score_Galda']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Galda'), axis=1)
            df['Score_Bagda']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Bagda'), axis=1)
            df['Score_Harina']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Harina'), axis=1)
            df['Score_Chaka']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'Chaka'), axis=1)
            df['Score_OtherSmallShrimp_Prawn']=df.apply(lambda x: scoreCondition(nodeWiseFish_coef_intercept, x,'OtherSmallShrimp_Prawn'), axis=1)
            
            #Probability of Fish	 =(EXP(Z24)/(1+EXP(Z24)))-0.5
            df['P_Rui']=((np.exp(df['Score_Rui'])/(1+np.exp(df['Score_Rui'])))-0.5)	
            df['P_Catla']=((np.exp(df['Score_Catla'])/(1+np.exp(df['Score_Catla'])))-0.5)	
            df['P_Mrigal']=((np.exp(df['Score_Mrigal'])/(1+np.exp(df['Score_Mrigal'])))-0.5)	
            df['P_Kalibaus']=((np.exp(df['Score_Kalibaus'])/(1+np.exp(df['Score_Kalibaus'])))-0.5)	
            df['P_Bata']=((np.exp(df['Score_Bata'])/(1+np.exp(df['Score_Bata'])))-0.5)	
            df['P_Gonia']=((np.exp(df['Score_Gonia'])/(1+np.exp(df['Score_Gonia'])))-0.5)	
            df['P_Pangas']=((np.exp(df['Score_Pangas'])/(1+np.exp(df['Score_Pangas'])))-0.5)	

            df['P_Boal_Air']=((np.exp(df['Score_Boal_Air'])/(1+np.exp(df['Score_Boal_Air'])))-0.5)	
            df['P_Shol_Gazar_Taki']=((np.exp(df['Score_Shol_Gazar_Taki'])/(1+np.exp(df['Score_Shol_Gazar_Taki'])))-0.5)															
            df['P_Koi']=((np.exp(df['Score_Koi'])/(1+np.exp(df['Score_Koi'])))-0.5)	
            df['P_Shingi_Magur']=((np.exp(df['Score_Shingi_Magur'])/(1+np.exp(df['Score_Shingi_Magur'])))-0.5)	
            df['P_Sarpunti']=((np.exp(df['Score_Sarpunti'])/(1+np.exp(df['Score_Sarpunti'])))-0.5)	
            df['P_OtherInlandFish']=((np.exp(df['Score_OtherInlandFish'])/(1+np.exp(df['Score_OtherInlandFish'])))-0.5)	
            
            df['P_Hilsa_Ilish']=((np.exp(df['Score_Hilsa_Ilish'])/(1+np.exp(df['Score_Hilsa_Ilish'])))-0.5)	
            df['P_Galda']=((np.exp(df['Score_Galda'])/(1+np.exp(df['Score_Galda'])))-0.5)	
            df['P_Bagda']=((np.exp(df['Score_Bagda'])/(1+np.exp(df['Score_Bagda'])))-0.5)	
            df['P_Harina']=((np.exp(df['Score_Harina'])/(1+np.exp(df['Score_Harina'])))-0.5)	
            df['P_Chaka']=((np.exp(df['Score_Chaka'])/(1+np.exp(df['Score_Chaka'])))-0.5)
            df['P_OtherSmallShrimp_Prawn']=((np.exp(df['Score_OtherSmallShrimp_Prawn'])/(1+np.exp(df['Score_OtherSmallShrimp_Prawn'])))-0.5)

            #Ratio Calculate from Yearly data to Decade data
            df['Ratio_Rui']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Rui'), axis=1)
            df['Ratio_Catla']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Catla'), axis=1)
            df['Ratio_Mrigal']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Mrigal'), axis=1)
            df['Ratio_Kalibaus']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Kalibaus'), axis=1)
            df['Ratio_Bata']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Bata'), axis=1)
            df['Ratio_Gonia']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Gonia'), axis=1)
            df['Ratio_Pangas']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Pangas'), axis=1)

            df['Ratio_Boal_Air']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Boal_Air'), axis=1)
            df['Ratio_Shol_Gazar_Taki']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Shol_Gazar_Taki'), axis=1)
            df['Ratio_Koi']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Koi'), axis=1)
            df['Ratio_Shingi_Magur']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Shingi_Magur'), axis=1)
            df['Ratio_Sarpunti']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Sarpunti'), axis=1)
            df['Ratio_OtherInlandFish']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'OtherInlandFish'), axis=1)
            
            df['Ratio_Hilsa_Ilish']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Hilsa_Ilish'), axis=1)
            df['Ratio_Galda']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Galda'), axis=1)
            df['Ratio_Bagda']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Bagda'), axis=1)
            df['Ratio_Harina']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Harina'), axis=1)
            df['Ratio_Chaka']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'Chaka'), axis=1)
            df['Ratio_OtherSmallShrimp_Prawn']=df.apply(lambda x: fishRatio(UpazilaNodeWiseProduction, x,'OtherSmallShrimp_Prawn'), axis=1)
            
            #UpazilaNodeWiseProduction['Rui_MT']/UpazilaNodeWiseProduction['TotalProduction_MT']
            #UpazilaNodeWiseProduction
            #Maximum Likelihood, P(Day/Species): [P(Day)*P(Species/Day)]/[P(Species)]	
            ##df['Ratio_Rui']==0 then 0 otherwise  ((df['P_Suitability']*df['P_Rui'])/df['Ratio_Rui'])
            # ML=Maximum Likelihood 
            df['Day_Rui_ML']=np.where(df['Ratio_Rui']==0, 0, ((df['P_Suitability']*df['P_Rui'])/df['Ratio_Rui']))
            df['Day_Catla_ML']=np.where(df['Ratio_Catla']==0, 0, ((df['P_Suitability']*df['P_Catla'])/df['Ratio_Catla']))
            df['Day_Mrigal_ML']=np.where(df['Ratio_Mrigal']==0, 0, ((df['P_Suitability']*df['P_Mrigal'])/df['Ratio_Mrigal']))      
            df['Day_Kalibaus_ML']=np.where(df['Ratio_Kalibaus']==0, 0, ((df['P_Suitability']*df['P_Kalibaus'])/df['Ratio_Kalibaus']))
            df['Day_Bata_ML']=np.where(df['Ratio_Bata']==0, 0, ((df['P_Suitability']*df['P_Bata'])/df['Ratio_Bata']))																	  
            df['Day_Gonia_ML']=np.where(df['Ratio_Gonia']==0, 0, ((df['P_Suitability']*df['P_Gonia'])/df['Ratio_Gonia']))
            df['Day_Pangas_ML']=np.where(df['Ratio_Pangas']==0, 0, ((df['P_Suitability']*df['P_Pangas'])/df['Ratio_Pangas']))
            

            df['Day_Boal_Air_ML']=np.where(df['Ratio_Boal_Air']==0, 0, ((df['P_Suitability']*df['P_Boal_Air'])/df['Ratio_Boal_Air']))
            df['Day_Shol_Gazar_Taki_ML']=np.where(df['Ratio_Shol_Gazar_Taki']==0, 0, ((df['P_Suitability']*df['P_Shol_Gazar_Taki'])/df['Ratio_Shol_Gazar_Taki']))
            df['Day_Koi_ML']=np.where(df['Ratio_Koi']==0, 0, ((df['P_Suitability']*df['P_Koi'])/df['Ratio_Koi']))
            df['Day_Shingi_Magur_ML']=np.where(df['Ratio_Shingi_Magur']==0, 0, ((df['P_Suitability']*df['P_Shingi_Magur'])/df['Ratio_Shingi_Magur']))
            df['Day_Sarpunti_ML']=np.where(df['Ratio_Sarpunti']==0, 0, ((df['P_Suitability']*df['P_Sarpunti'])/df['Ratio_Sarpunti']))
            df['Day_OtherInlandFish_ML']=np.where(df['Ratio_OtherInlandFish']==0, 0, ((df['P_Suitability']*df['P_OtherInlandFish'])/df['Ratio_OtherInlandFish']))
            
            df['Day_Hilsa_Ilish_ML']=np.where(df['Ratio_Hilsa_Ilish']==0, 0, ((df['P_Suitability']*df['P_Hilsa_Ilish'])/df['Ratio_Hilsa_Ilish']))
            df['Day_Galda_ML']=np.where(df['Ratio_Galda']==0, 0, ((df['P_Suitability']*df['P_Galda'])/df['Ratio_Galda']))
            df['Day_Bagda_ML']=np.where(df['Ratio_Bagda']==0, 0, ((df['P_Suitability']*df['P_Bagda'])/df['Ratio_Bagda']))        
            df['Day_Harina_ML']=np.where(df['Ratio_Harina']==0, 0, ((df['P_Suitability']*df['P_Harina'])/df['Ratio_Harina']))
            df['Day_Chaka_ML']=np.where(df['Ratio_Chaka']==0, 0, ((df['P_Suitability']*df['P_Chaka'])/df['Ratio_Chaka']))
            df['Day_OtherSmallShrimp_Prawn_ML']=np.where(df['Ratio_OtherSmallShrimp_Prawn']==0, 0, ((df['P_Suitability']*df['P_OtherSmallShrimp_Prawn'])/df['Ratio_OtherSmallShrimp_Prawn']))
            
        
            #Production Ratio
            df['P_Ratio_Rui']=df.apply(lambda x: productionRatio(df,x,'Rui'), axis=1)
            df['P_Ratio_Catla']=df.apply(lambda x: productionRatio(df,x,'Catla'), axis=1)
            df['P_Ratio_Mrigal']=df.apply(lambda x: productionRatio(df,x,'Mrigal'), axis=1)
            df['P_Ratio_Kalibaus']=df.apply(lambda x: productionRatio(df,x,'Kalibaus'), axis=1)
            df['P_Ratio_Bata']=df.apply(lambda x: productionRatio(df,x,'Bata'), axis=1)
            df['P_Ratio_Gonia']=df.apply(lambda x: productionRatio(df,x,'Gonia'), axis=1)
            df['P_Ratio_Pangas']=df.apply(lambda x: productionRatio(df,x,'Pangas'), axis=1)

            df['P_Ratio_Boal_Air']=df.apply(lambda x: productionRatio(df,x,'Boal_Air'), axis=1)
            df['P_Ratio_Shol_Gazar_Taki']=df.apply(lambda x: productionRatio(df,x,'Shol_Gazar_Taki'), axis=1)

            df['P_Ratio_Koi']=df.apply(lambda x: productionRatio(df,x,'Koi'), axis=1)
            df['P_Ratio_Shingi_Magur']=df.apply(lambda x: productionRatio(df,x,'Shingi_Magur'), axis=1)

            df['P_Ratio_Sarpunti']=df.apply(lambda x: productionRatio(df,x,'Sarpunti'), axis=1)
            df['P_Ratio_OtherInlandFish']=df.apply(lambda x: productionRatio(df,x,'OtherInlandFish'), axis=1)
            df['P_Ratio_Hilsa_Ilish']=df.apply(lambda x: productionRatio(df,x,'Hilsa_Ilish'), axis=1)

            df['P_Ratio_Galda']=df.apply(lambda x: productionRatio(df,x,'Galda'), axis=1)
            df['P_Ratio_Bagda']=df.apply(lambda x: productionRatio(df,x,'Bagda'), axis=1)
            df['P_Ratio_Harina']=df.apply(lambda x: productionRatio(df,x,'Harina'), axis=1)
            df['P_Ratio_Chaka']=df.apply(lambda x: productionRatio(df,x,'Chaka'), axis=1)
            df['P_Ratio_OtherSmallShrimp_Prawn']=df.apply(lambda x: productionRatio(df,x,'OtherSmallShrimp_Prawn'), axis=1)

            #Production (MT)	
            # Rui Catla Mrigal Kalibaus Bata Gonia Pangas Boal_Air Shol_Gazar_Taki Koi Shingi_Magur 
            # Sarpunti OtherInlandFish Hilsa_Ilish Galda Bagda Harina Chaka OtherSmallShrimp_Prawn
            
            df['Production_Rui']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Rui'), axis=1)
            df['Production_Catla']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Catla'), axis=1)
            df['Production_Mrigal']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Mrigal'), axis=1)
            df['Production_Kalibaus']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Kalibaus'), axis=1)
            df['Production_Bata']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Bata'), axis=1)
            df['Production_Gonia']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Gonia'), axis=1)
            df['Production_Pangas']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Pangas'), axis=1)
            
            df['Production_Boal_Air']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Boal_Air'), axis=1)
            df['Production_Shol_Gazar_Taki']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Shol_Gazar_Taki'), axis=1)
            df['Production_Koi']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Koi'), axis=1)
            df['Production_Shingi_Magur']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Shingi_Magur'), axis=1)
            df['Production_Sarpunti']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Sarpunti'), axis=1)
            df['Production_OtherInlandFish']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'OtherInlandFish'), axis=1)
            df['Production_Hilsa_Ilish']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Hilsa_Ilish'), axis=1)
            df['Production_Galda']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Galda'), axis=1)
            df['Production_Bagda']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Bagda'), axis=1)
            df['Production_Harina']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Harina'), axis=1)
            df['Production_Chaka']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'Chaka'), axis=1)
            df['Production_OtherSmallShrimp_Prawn']=df.apply(lambda x: fishProduction(UpazilaNodeWiseProduction, x,'OtherSmallShrimp_Prawn'), axis=1)               																																				
            finalData=finalData.append(df)
            #print(df.head())
            #df.to_csv(str(singleUpazilaData.THACODE)+'Output.csv',index=False)


        # print(data[['date', 'THACODE','Production_Rui','Production_Catla','Production_Mrigal','Production_Kalibaus',
#         'Production_Bata','Production_Gonia','Production_Pangas','Production_Boal_Air','Production_Shol_Gazar_Taki',
#         'Production_Koi', 'Production_Shingi_Magur', 'Production_Sarpunti',
#         'Production_OtherInlandFish', 'Production_Hilsa_Ilish',
#         'Production_Galda', 'Production_Bagda', 'Production_Harina',
#         'Production_Chaka', 'Production_OtherSmallShrimp_Prawn']].head())


        finalData['TotalProduction']=finalData['Production_Rui']+finalData['Production_Catla']+finalData['Production_Mrigal']+finalData['Production_Kalibaus']+finalData['Production_Bata']+finalData['Production_Gonia']+finalData['Production_Pangas']+finalData['Production_Boal_Air']+finalData['Production_Shol_Gazar_Taki']+finalData['Production_Koi']+finalData['Production_Shingi_Magur']+finalData['Production_Sarpunti']+finalData['Production_OtherInlandFish']+finalData['Production_Hilsa_Ilish']+finalData['Production_Galda']+finalData['Production_Bagda']+finalData['Production_Harina']+finalData['Production_Chaka']+finalData['Production_OtherSmallShrimp_Prawn']

        #id	upz_code	crop_type_id	loss_type_id	indicator_code	indicator_value	run_code	collected_date	run_code_ged


        finalData=finalData[['date','Year', 'THACODE','TotalProduction']]
        finalData = finalData.rename(columns={'Year': 'collected_date' ,'THACODE': 'upz_code', 'TotalProduction': 'indicator_value'})

        finalData=finalData.groupby(['collected_date','upz_code']).sum().reset_index()
        finalData['run_code']=1
        finalData['loss_type_id']=1
        finalData['crop_type_id']=1
        finalData['indicator_code']='I-30'

        


        #finalData=finalData

        finalData.to_csv('riverFishProduction.csv',index=False)
        #nodeWiseFish_coef_intercept.to_csv('nodeWiseFish_coef_intercept.csv',index=False)
        return finalData.head()

def fishProduction(condition,x_df,fishName):
    condition=condition[(condition['Year']==x_df['Year']) & (condition['THACODE']==x_df['THACODE'])]
    return (condition.iloc[0][fishName+'_MT']*x_df['P_Ratio_'+fishName])

def productionRatio(all_df,x_df,fishName):

    if x_df['Day_'+fishName+'_ML']==0:
        return 0
    else:       
        condition=all_df[(all_df['Year']==x_df['Year']) & (all_df['THACODE']==x_df['THACODE'])]
        return (x_df['Day_'+fishName+'_ML']/condition['Day_'+fishName+'_ML'].sum())


def fishRatio(condition,x_df,fishName):

    condition=condition[(condition['Year']==x_df['Year']) & (condition['THACODE']==x_df['THACODE'])]
    #print(condition)
    return (condition.iloc[0][fishName+'_MT']/condition.iloc[0]['TotalProduction_MT'])

def scoreCondition(condition,x_df,fishName):    
    if x_df['S_'+fishName]>0: 
        nodeWiseFish=condition[(condition['FishName']==fishName) & (condition['THACODE']==x_df['THACODE'])] 
        #print(nodeWiseFish.iloc[0].Intercept)      
        #if len(nodeWiseFish_coef_intercept)>0:
            #print(nodeWiseFish_coef_intercept)
        return (nodeWiseFish.iloc[0].Intercept+(x_df['Qsec']*nodeWiseFish.iloc[0].Qsec+x_df['WD']*nodeWiseFish.iloc[0].WD))
    else:
        return 0
    
def getNodeWiseFish_coef_intercept(x_df):

    #data=pd.read_csv("FisheriesModuleOutput.csv")
    nodeList=pd.read_csv("upzList.csv")
    #nodeList=x_df.THACODE.unique()
    #print(x_df.THACODE.unique())


    fishList=pd.read_csv("fishList.csv")

    nodeWiseFish_coef_intercept=pd.DataFrame(columns=['THACODE','FishName','Qsec','WD','Intercept'])
    columnList=columns=['THACODE','FishName','Qsec','WD','Intercept']
    ListOfData=[]

    #print(nodeWiseFish_coef_intercept)

    for item in nodeList.itertuples():
        NodeData=x_df[x_df['THACODE']==item.THACODE]
    
        if len(NodeData)!=0:               
            for fish in fishList.itertuples():            
            
                if ("S_"+fish.FishName) in NodeData.columns:
                
                    X=NodeData[['Qsec','WD']]
                    y=NodeData["S_"+fish.FishName]
                    reg = LinearRegression().fit(X, y)
                
                    if reg.coef_[0]<0:
                        reg.coef_[0]=0
                    
                    if reg.coef_[1]<0:
                        reg.coef_[1]=0
                    
                    #if reg.intercept_<0:             
                        #reg.intercept_=0                    
                    
                    ListOfData.append([item.THACODE,fish.FishName,reg.coef_[0],reg.coef_[1],reg.intercept_])
                
    nodeWiseFish_coef_intercept= pd.DataFrame(ListOfData,columns=columnList)           
    #nodeWiseFish_coef_intercept.to_csv('nodeWiseFish_coef_intercept.csv',index=False)
    #print(nodeWiseFish_coef_intercept)   
    return nodeWiseFish_coef_intercept

def fishSurvivalCondition(fishName,x_df):
    if fishName=="S_Rui":
        #Dishcharge
        if (x_df['Q_200%MAF_OC']>0 or x_df['Q_100%MAF_OC']>0 or x_df['Q_50%MAF_OC']>0 or x_df['Q_40%MAF_OC']>0 or x_df['Q_30%MAF_OC']>0):
            #Water Depth
            if (x_df['WD>10m_OC']>0 or x_df['WD>5m_OC']>0):
                #Water Temparature
                if x_df['Wtemp_MAX<30C_OC']>0 or x_df['Wtemp_MIN>5C_OC']:
                    return 1
                return 0    
            else:
                return 0        
        else:
            return 0

    if fishName=="S_Shol_Gazar_Taki":
        if (x_df['Q_10%MAF_OC']>0):
            if (x_df['WD>1m_OC']>0):
                if x_df['Wtemp_MAX<30C_OC']>0 or x_df['Wtemp_MIN>5C_OC']:
                    return 1
                return 0    
            else:
                return 0        
        else:
            return 0
    if fishName=="S_Koi":
        if (x_df['Q_10%MAF_OC']>0):
            if (x_df['WD>1m_OC']>0 or x_df['WD>0.5m_OC']>0 or x_df['WD>0.25m_OC']>0 or x_df['Critical_WD_m_OC']>0):
                if x_df['Wtemp_MAX<30C_OC']>0 or x_df['Wtemp_MIN>5C_OC']:
                    return 1
                return 0    
            else:
                return 0        
        else:
            return 0   
    if fishName=="S_Shingi_Magur":
        if (x_df['Q_30%MAF_OC']>0 or x_df['Q_25%MAF_OC']>0 or x_df['Q_10%MAF_OC']>0):
            if (x_df['WD>1m_OC']>0 or x_df['WD>0.5m_OC']>0 or x_df['WD>0.25m_OC']>0 or x_df['Critical_WD_m_OC']>0):
                if x_df['Wtemp_MAX<30C_OC']>0 or x_df['Wtemp_MIN>5C_OC']:
                    return 1
                return 0    
            else:
                return 0        
        else:
            return 0   
    if fishName=="S_Sarpunti":
        if (x_df['Q_200%MAF_OC']>0 or x_df['Q_100%MAF_OC']>0 or x_df['Q_50%MAF_OC']>0 or x_df['Q_40%MAF_OC']>0 or x_df['Q_30%MAF_OC']>0):
            if (x_df['WD>10m_OC']>0 or x_df['WD>5m_OC']>0 or x_df['WD>1m_OC']>0):
                if x_df['Wtemp_MAX<30C_OC']>0 or x_df['Wtemp_MIN>5C_OC']:
                    return 1
                return 0    
            else:
                return 0        
        else:
            return 0             
    if fishName=="S_OtherInlandFish":
        if (x_df['Q_200%MAF_OC']>0 or x_df['Q_100%MAF_OC']>0 or x_df['Q_50%MAF_OC']>0 or x_df['Q_40%MAF_OC']>0 or x_df['Q_30%MAF_OC']>0 or x_df['Q_25%MAF_OC']>0 or x_df['Q_10%MAF_OC']>0):
            if (x_df['WD>10m_OC']>0 or  x_df['Critical_WD_m_OC']>0):
                if x_df['Wtemp_MAX<30C_OC']>0 or x_df['Wtemp_MIN>5C_OC']:
                    return 1
                return 0    
            else:
                return 0        
        else:
            return 0            
 
    if fishName=="S_Hilsa_Ilish":
        if (x_df['Q_200%MAF_OC']>0 or x_df['Q_100%MAF_OC']>0 or x_df['Q_50%MAF_OC']>0 or x_df['Q_40%MAF_OC']>0):
            if (x_df['WD>10m_OC']>0):
                if x_df['Wtemp_MAX<30C_OC']>0 or x_df['Wtemp_MIN>5C_OC']:
                    return 1
                return 0    
            else:
                return 0        
        else:
            return 0    


def main():
    dataroot = os.getcwd()
    fishProduction = FishProductionModuleClass(dataroot).initializeModuleforRun()
    print(fishProduction)

if __name__ == "__main__":
    main()      
