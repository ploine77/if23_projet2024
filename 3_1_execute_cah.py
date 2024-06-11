from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn import cluster
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

dfNaN = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedDataNaN.csv')
df0 = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData0.csv')
df95 = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData95.csv')
df200 = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData200.csv')
dfMean = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedDataMean.csv')

value0 = df0.drop(labels=["Position", "Version","Area"], axis=1).values
Z0 = linkage(value0,method='ward',metric='euclidean')

value95 = df95.drop(labels=["Position", "Version","Area"], axis=1).values
Z95 = linkage(value95,method='ward',metric='euclidean')

value200 = df200.drop(labels=["Position", "Version","Area"], axis=1).values
Z200 = linkage(value200,method='ward',metric='euclidean')

valueMean = dfMean.drop(labels=["Position", "Version","Area"], axis=1).values
ZMean = linkage(valueMean,method='ward',metric='euclidean')

num_clusters = 13

clusters0 = fcluster(Z0, t=num_clusters, criterion='maxclust')
clusters95 = fcluster(Z95, t=num_clusters, criterion='maxclust')
clusters200 = fcluster(Z200, t=num_clusters, criterion='maxclust')
clustersMean = fcluster(ZMean, t=num_clusters, criterion='maxclust')

distanceCut0 = Z0[-(num_clusters-1), 2]
distanceCut95 = Z95[-(num_clusters-1), 2]
distanceCut200 = Z200[-(num_clusters-1), 2]
distanceCutMean = ZMean[-(num_clusters-1), 2]

plt.title("CAH Data with 0")
dendrogram(Z0,labels=df95.index, color_threshold = distanceCut0)
#plt.savefig()

plt.title("CAH Data with -95")
dendrogram(Z95,labels=df95.index, color_threshold = distanceCut95)
#plt.show()

plt.title("CAH Data with -200")
dendrogram(Z200,labels=df95.index, color_threshold = distanceCut200)
#plt.show()

plt.title("CAH Data with Mean")
dendrogram(ZMean,labels=dfMean.index, color_threshold = distanceCutMean)
#plt.show()

cm0 = pd.crosstab(dfNaN.Area,clusters0)
cm95 = pd.crosstab(dfNaN.Area,clusters95)
cm200 = pd.crosstab(dfNaN.Area,clusters200)
cmMean = pd.crosstab(dfNaN.Area,clusters200)

cm0.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaCAH0.csv')
cm95.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaCAH95.csv')
cm200.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaCAH200.csv')
cmMean.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\areaCAHMean.csv')

