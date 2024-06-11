import pandas as pd
from sklearn import cluster

dfNaN = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedDataNaN.csv')
df0 = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData0.csv')
df95 = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData95.csv')
df200 = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData200.csv')
dfMean = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedDataMean.csv')

value0 = df0.drop(labels=["Position", "Version","Area"], axis=1).values
value95 = df95.drop(labels=["Position", "Version","Area"], axis=1).values
value200 = df200.drop(labels=["Position", "Version","Area"], axis=1).values
valueMean = dfMean.drop(labels=["Position", "Version","Area"], axis=1).values

kmeans0 = cluster.KMeans(n_clusters=13)
kmeans95 = cluster.KMeans(n_clusters=13)
kmeans200 = cluster.KMeans(n_clusters=13)
kmeansMean = cluster.KMeans(n_clusters=13)

kmeans0.fit(value0)
kmeans95.fit(value95)
kmeans200.fit(value200)
kmeansMean.fit(valueMean)

cm0 = pd.crosstab(dfNaN.Area,kmeans0.labels_)
cm95 = pd.crosstab(dfNaN.Area,kmeans95.labels_)
cm200 = pd.crosstab(dfNaN.Area,kmeans200.labels_)
cmMean = pd.crosstab(dfNaN.Area,kmeansMean.labels_)

cm0.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaKMEAN0.csv')
cm95.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaKMEAN95.csv')
cm200.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaKMEAN200.csv')
cmMean.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaKMEANMean.csv')
