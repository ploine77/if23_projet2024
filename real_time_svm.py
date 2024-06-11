import pandas as pd
from scipy.cluster.hierarchy import linkage
from sklearn.svm import SVC

df = pd.read_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\treatedData.csv')
Z = linkage(df.drop(labels=["Position", "Version","Area"], axis=1).values,method='ward',metric='euclidean')

svm = SVC(kernel='linear')
svm.fit(Z, Z.Area)
