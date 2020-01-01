import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn import preprocessing

print(datetime.now())

data = pd.read_csv('clusteringInput.csv', index_col=None)
data.columns = ['ID','Recency','LifeTime','Frequency','Monetary','MonetaryS','FrequencyS','RecencyS','LifeTimeS'] #Attributes with S are scores
print(data)
# If your data is too big in initial steps you can work on a sample of it and when you're done with setting initializations run the algorithm on the whole data set. 
# data = data.sample(frac=0.1)
data = data.drop(data.loc[data['ID']==0].index)
# Let X be the attributes that we want to cluster by
X = data[['MonetaryS','FrequencyS','RecencyS','LifeTimeS']]

## My data doesn't need normalization because of the scoring
#normalizer = preprocessing.Normalizer().fit(X)
#XP = normalizer.transform(X)
#print(XP)
#X =  pd.DataFrame(data=XP[:,:])

X.columns = ['MonetaryS','FrequencyS','RecencyS','LifeTimeS'] #Attributes with S are scores

# Replace NULL values with 0
X.fillna(0)
# Negative score for recency
X['RecencyS'] = - X['RecencyS']
print(X)
# Dimension reduction by PCA 
pca2 = PCA(n_components=1)
pca2.fit(X)
x_1D = pca2.transform(X)
print(x_1D)

# Cluster by KMeans
kmeans = KMeans(n_clusters=4,random_state=0).fit(x_1D)
# to add the labels to the initial data set
data['label'] = kmeans.labels_


""" # To see the clustering result on diagrams
plt.scatter(data['Monetary'],data['Frequency'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.show()
plt.scatter(data['Monetary'],data['Recency'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.show()
plt.scatter(data['Frequency'],data['Recency'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.show()
"""
    
data.to_csv("clusteredData.csv",index=False)
print(datetime.now())
