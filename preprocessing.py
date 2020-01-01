
import pandas as pd
from pandas import DataFrame
from datetime import datetime


print(datetime.now())

monetary = pd.read_csv("Monetary_of_a_year.csv", index_col=None)
monetary.columns = ['ID','amount'] 

frequency = pd.read_csv("Frequency_of_a_year.csv", index_col=None)
frequency.columns = ['ID','amount']

length = pd.read_csv("First_And_Last_Transaction_So_Far.csv", index_col=None)
length.columns = ['ID','first','last']  # first and last indicates the date that the first and the last transactions happened. We use them to calculate Recency and Life Time.

# Recency = Today - LastDay 
# LifeTime = LastDay - FirstDay 
# In my data first and last dates are stored as integers in Persian calendar.
# Line 23 to line 51 are calculating Recency and LifeTime, you may use different ways to do so regarding your initial data. 
tmp = length
tmp['d'] = tmp['last']%100
tmp['last'] = tmp['last']/100
tmp['last']  = tmp['last'].astype('int32')
tmp['m'] = tmp['last']%100
tmp['last'] = tmp['last']/100
tmp['last']  = tmp['last'].astype('int32')
tmp['y'] = tmp['last']%10
tmp['dl'] = tmp['d']
tmp['ml'] = tmp['m']
tmp['yl'] = tmp['y']
tmp['d'] = 30-tmp['d'] 
tmp['m'] = 8-tmp['m']
tmp['y'] = 8-tmp['y']
tmp['last'] = tmp['d'] + 30*tmp['m'] + 365*tmp['y']
length['Recency'] = tmp['last']

tmp['df'] = tmp['first']%100
tmp['first'] = tmp['first']/100
tmp['first']  = tmp['first'].astype('int32')
tmp['mf'] = tmp['first']%100
tmp['first'] = tmp['first']/100
tmp['first']  = tmp['first'].astype('int32')
tmp['yf'] = tmp['first']%10
tmp['df'] = tmp['dl']-tmp['df']
tmp['mf'] = tmp['ml']-tmp['mf']
tmp['yf'] = tmp['yl']-tmp['yf']
tmp['first'] = tmp['df'] + 30*tmp['mf'] + 365*tmp['yf']
length['LifeTime'] = tmp['first']

# Drop temporary columns
length = length.drop(['d', 'm','y','df','mf','yf','dl', 'ml','yl','last','first'], axis = 1) 


monetary['amount'] = monetary['amount'].astype('int32')
frequency['amount'] = frequency['amount'].astype('int32')


print(length)

# Now we merge the dataframes to have all the LRFM attributes together
all = length.merge(frequency, on='ID', how = 'left')
all = all.fillna(0)
all = all.merge(monetary, on='ID', how = 'left')
print(all)
all = all.fillna(0)

all.columns = ['ID','Recency','LifeTime','Frequency','Monetary']
print(all)
all.to_csv('data.csv',index=False)

data = all

# base is max (LifeTime,one year). My monetary and frequency come from the last year of the data. 
# But I want monthly purchase as the monetory and monthly count of transactions as the frequency. For this I divided the initial amount by base.
data['base'] = data['LifeTime']
data.loc[data['LifeTime']>335  ,'base'] = 335
data['base'] = data['base']/30
data['base'] = data['base'].astype('int32')
data.loc[data['base']==0  ,'base'] = 1

data['Monetary'] = data['Monetary']/data['base']
data['Frequency'] = data['Frequency']/data['base']
data = data.drop(['base'], axis = 1)


#Monetary Scoring
data.loc[data['Monetary']<=2000 ,'MonetaryS'] = 1
data.loc[data['Monetary'].between(2000, 20000, inclusive = True)  ,'MonetaryS'] = 2
data.loc[data['Monetary'].between(20000,50000 , inclusive = True),'MonetaryS'] = 3
data.loc[data['Monetary'].between(50000,100000 , inclusive = True),'MonetaryS'] = 4
data.loc[data['Monetary'].between(100000,200000 , inclusive = True),'MonetaryS'] = 5
data.loc[data['Monetary'].between(200000,300000 , inclusive = True),'MonetaryS'] = 6
data.loc[data['Monetary'].between(300000,400000 , inclusive = True),'MonetaryS'] = 7
data.loc[data['Monetary'].between(400000,500000 , inclusive = True),'MonetaryS'] = 8
data.loc[data['Monetary'].between(500000,700000 , inclusive = True),'MonetaryS'] = 9
data.loc[data['Monetary'].between(700000,1000000 , inclusive = True),'MonetaryS'] = 10
data.loc[data['Monetary'].between(1000000,1500000 , inclusive = True),'MonetaryS'] = 11
data.loc[data['Monetary'].between(1500000,2000000 , inclusive = True),'MonetaryS'] = 12
data.loc[data['Monetary'].between(2000000,5000000 , inclusive = True),'MonetaryS'] = 13
data.loc[data['Monetary'].between(5000000,10000000 , inclusive = True),'MonetaryS'] = 14
data.loc[data['Monetary'].between(10000000,20000000 , inclusive = True),'MonetaryS'] = 15
data.loc[data['Monetary'].between(20000000,50000000 , inclusive = True),'MonetaryS'] = 16
data.loc[data['Monetary'].between(50000000,100000000 , inclusive = True),'MonetaryS'] = 17
data.loc[data['Monetary'].between(100000000,300000000 , inclusive = True),'MonetaryS'] = 18
data.loc[data['Monetary'].between(300000000,500000000 , inclusive = True),'MonetaryS'] = 19
data.loc[data['Monetary']>500000000 ,'MonetaryS'] = 20

#Frequency Scoring
data.loc[data['Frequency']<=0.2 ,'FrequencyS'] = 1
data.loc[data['Frequency'].between(0.2,0.5 , inclusive = True),'FrequencyS'] = 2
data.loc[data['Frequency'].between(0.5,1 , inclusive = True),'FrequencyS'] = 3
data.loc[data['Frequency'].between(1,2 , inclusive = True),'FrequencyS'] = 4
data.loc[data['Frequency'].between(2,3 , inclusive = True),'FrequencyS'] = 5
data.loc[data['Frequency'].between(3,5 , inclusive = True),'FrequencyS'] = 6
data.loc[data['Frequency'].between(5,7  , inclusive = True),'FrequencyS'] = 7
data.loc[data['Frequency'].between(7,10  , inclusive = True),'FrequencyS'] =8
data.loc[data['Frequency'].between(10,15  , inclusive = True),'FrequencyS'] = 9
data.loc[data['Frequency'].between(15,20  , inclusive = True),'FrequencyS'] = 10
data.loc[data['Frequency'].between(20,30  , inclusive = True),'FrequencyS'] = 11
data.loc[data['Frequency'].between(30,40  , inclusive = True),'FrequencyS'] = 12
data.loc[data['Frequency'].between(40,50  , inclusive = True),'FrequencyS'] = 13
data.loc[data['Frequency'].between(50,70  , inclusive = True),'FrequencyS'] = 14
data.loc[data['Frequency'].between(70,100  , inclusive = True),'FrequencyS'] = 15
data.loc[data['Frequency'].between(100,120  , inclusive = True),'FrequencyS'] = 16
data.loc[data['Frequency'].between(120,150 , inclusive = True),'FrequencyS'] = 17
data.loc[data['Frequency'].between(150,200 , inclusive = True),'FrequencyS'] = 18
data.loc[data['Frequency'].between(200,300 , inclusive = True),'FrequencyS'] = 19
data.loc[data['Frequency'].between(300,400 , inclusive = True),'FrequencyS'] = 20
data.loc[data['Frequency'].between(400,500 , inclusive = True),'FrequencyS'] = 21
data.loc[data['Frequency'].between(500,600 , inclusive = True),'FrequencyS'] = 22
data.loc[data['Frequency'].between(600,700 , inclusive = True),'FrequencyS'] = 23
data.loc[data['Frequency'].between(700,800 , inclusive = True),'FrequencyS'] = 24
data.loc[data['Frequency'].between(800,1000 , inclusive = True),'FrequencyS'] = 25
data.loc[data['Frequency']>1000 ,'FrequencyS'] = 26

#Recency Scoring
data.loc[data['Recency']<=7 ,'RecencyS'] = 1
data.loc[data['Recency'].between(7,15 , inclusive = True),'RecencyS'] = 2
data.loc[data['Recency'].between(15,30 , inclusive = True),'RecencyS'] = 3
data.loc[data['Recency'].between(30,60 , inclusive = True),'RecencyS'] = 4
data.loc[data['Recency'].between(60,120 , inclusive = True),'RecencyS'] = 5
data.loc[data['Recency'].between(120,180 , inclusive = True),'RecencyS'] = 6
data.loc[data['Recency'].between(180,240 , inclusive = True),'RecencyS'] = 7
data.loc[data['Recency'].between(240,300 , inclusive = True),'RecencyS'] = 8
data.loc[data['Recency'].between(300,365 , inclusive = True),'RecencyS'] = 9
data.loc[data['Recency'].between(365,730 , inclusive = True),'RecencyS'] = 10
data.loc[data['Recency'].between(730,1095 , inclusive = True),'RecencyS'] = 11
data.loc[data['Recency'].between(1095,1460 , inclusive = True),'RecencyS'] = 12
data.loc[data['Recency'].between(1460,1825 , inclusive = True),'RecencyS'] = 13
data.loc[data['Recency']>1825,'RecencyS'] = 14

#LifeTime Scoring
data.loc[data['LifeTime']<=7 ,'LifeTimeS'] = 1
data.loc[data['LifeTime'].between(7,15 , inclusive = True),'LifeTimeS'] = 2
data.loc[data['LifeTime'].between(15,30 , inclusive = True),'LifeTimeS'] = 3
data.loc[data['LifeTime'].between(30,60 , inclusive = True),'LifeTimeS'] = 4
data.loc[data['LifeTime'].between(60,120 , inclusive = True),'LifeTimeS'] = 5
data.loc[data['LifeTime'].between(120,180 , inclusive = True),'LifeTimeS'] = 6
data.loc[data['LifeTime'].between(180,240 , inclusive = True),'LifeTimeS'] = 7
data.loc[data['LifeTime'].between(240,300 , inclusive = True),'LifeTimeS'] = 8
data.loc[data['LifeTime'].between(300,365 , inclusive = True),'LifeTimeS'] = 9
data.loc[data['LifeTime'].between(365,730 , inclusive = True),'LifeTimeS'] = 10
data.loc[data['LifeTime'].between(730,1095 , inclusive = True),'LifeTimeS'] = 11
data.loc[data['LifeTime'].between(1095,1460 , inclusive = True),'LifeTimeS'] = 12
data.loc[data['LifeTime'].between(1460,1825 , inclusive = True),'LifeTimeS'] = 13
data.loc[data['LifeTime']>1825,'LifeTimeS'] = 14


data.to_csv('clusteringInput.csv',index=False)

print(datetime.now())
