import pandas as pd


#dataQsec=pd.read_csv("1_Q.csv")
#dataUpzToNode=pd.read_csv("input/UPZtoNodes.csv")
#dataWd=pd.read_csv("1_WaterDepth.csv")
#dataTimeStep=pd.read_csv("input/TimestepCalculation.csv")
data=pd.read_csv("FisheriesModuleOutput.csv")

fishList=pd.read_csv("fishList.csv")

data['TotalProduction']=data['Production_Rui']+data['Production_Catla']+data['Production_Mrigal']+data['Production_Kalibaus']+data['Production_Bata']+data['Production_Gonia']+data['Production_Pangas']+data['Production_Boal_Air']+data['Production_Shol_Gazar_Taki']+data['Production_Koi']+data['Production_Shingi_Magur']+data['Production_Sarpunti']+data['Production_OtherInlandFish']+data['Production_Hilsa_Ilish']+data['Production_Galda']+data['Production_Bagda']+data['Production_Harina']+data['Production_Chaka']+data['Production_OtherSmallShrimp_Prawn']

data=data[['date','Year', 'THACODE','TotalProduction']]

data=data.groupby(['Year','THACODE']).sum().reset_index()


#d2 = grouper['TotalProduction'].sum().to_frame(name = 'sum').reset_index()

data['run_code']=1




data.to_csv('data.csv')

print(data.head())

#print(data[['date','Year', 'THACODE','TotalProduction']].head())
# print(data[['date', 'THACODE','Production_Rui','Production_Catla','Production_Mrigal','Production_Kalibaus',
#         'Production_Bata','Production_Gonia','Production_Pangas','Production_Boal_Air','Production_Shol_Gazar_Taki',
#         'Production_Koi', 'Production_Shingi_Magur', 'Production_Sarpunti',
#         'Production_OtherInlandFish', 'Production_Hilsa_Ilish',
#         'Production_Galda', 'Production_Bagda', 'Production_Harina',
#         'Production_Chaka', 'Production_OtherSmallShrimp_Prawn']].head())




       
