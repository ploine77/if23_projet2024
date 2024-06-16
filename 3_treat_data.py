import json
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

keysPath = r"files\keys.json"
docPath = r'data'

with open(keysPath, "r") as fichier_json:
    keys = json.load(fichier_json)

untreatedDataPath = r"files\untreatedData"

if (not os.path.exists(untreatedDataPath)):
    print("Error : Run 2_get_formatted_data before")
    exit()

print("Choose a value to test")
dataValue = int(input())

df = pd.read_csv(r"files\untreatedData\untreatedData.csv")

df.replace("NaN", np.nan, inplace=True)
dfMean = df.copy()

researchDataPath = r'files\data_{}'.format(dataValue)

if (not os.path.exists(researchDataPath)):
    os.mkdir(researchDataPath)

    count = 0
    for column in df.columns[3:]:
        count+=1
        for area in df['Area'].unique():
            for position in df['Position'].unique():
                columnsPos = (df['Area'] == area) & (df['Position'] == position)
                df.loc[columnsPos, column] = df.loc[columnsPos, column].fillna(-dataValue)
            columnArea = (df['Area'] == area)
            df.loc[columnArea, column] = df.loc[columnArea, column].fillna(-dataValue)

    df.to_csv(r'files\data_{}\treated_data_{}.csv'.format(dataValue,dataValue))

    count = 0
    for column in dfMean.columns[4:]:
        count+=1
        for area in dfMean['Area'].unique():
            for position in dfMean['Position'].unique():
                columnsPos = (dfMean['Area'] == area) & (dfMean['Position'] == position)
                meanPos = dfMean.loc[columnsPos, column].mean()
                dfMean.loc[columnsPos, column] = dfMean.loc[columnsPos, column].fillna(meanPos)
            columnArea = (dfMean['Area'] == area)
            meanArea = dfMean.loc[columnArea, column].mean()
            if np.isnan(meanArea):
                meanArea = -dataValue
            dfMean.loc[columnArea, column] = dfMean.loc[columnArea, column].fillna(meanArea)

    dfMean.to_csv(r'files\data_{}\treated_data_mean_{}.csv'.format(dataValue,dataValue))
else : 
    df = pd.read_csv(r'files\data_{}\treated_data_{}.csv'.format(dataValue,dataValue))
    dfMean = pd.read_csv(r'files\data_{}\treated_data_mean_{}.csv'.format(dataValue,dataValue))


value = df.drop(labels=["Position", "Version","Area"], axis=1).values[:,2:]
valueMean = dfMean.drop(labels=["Position", "Version","Area"], axis=1).values[:,2:]
Z = linkage(value,method='ward',metric='euclidean')
ZMean = linkage(valueMean,method='ward',metric='euclidean')

num_clusters = 13

clusters = fcluster(Z, t=num_clusters, criterion='maxclust')
clustersMean = fcluster(ZMean, t=num_clusters, criterion='maxclust')

distanceCut = Z[-(num_clusters-1), 2]
distanceCutMean = ZMean[-(num_clusters-1), 2]

plt.title("CAH")
dendrogram(Z,labels=df.index, color_threshold = distanceCut)
plt.savefig(r'files\data_{}\cah_{}.png'.format(dataValue,dataValue))
plt.clf()

plt.title("CAH Mean")
dendrogram(ZMean,labels=df.index, color_threshold = distanceCutMean)
plt.savefig(r'files\data_{}\cah_mean_{}.png'.format(dataValue,dataValue))
plt.clf()

cm = pd.crosstab(df.Area,clusters)
cmMean = pd.crosstab(df.Area,clustersMean)

cm.to_csv(r'files\data_{}\confusion_matrix_cah_{}.csv'.format(dataValue,dataValue))
cmMean.to_csv(r'files\data_{}\confusion_matrix_cah_mean_{}.csv'.format(dataValue,dataValue))


kmeans = KMeans(n_clusters=13)
kmeansMean = KMeans(n_clusters=13)

kmeans.fit(value)
kmeansMean.fit(valueMean)

cm = pd.crosstab(df.Area,kmeans.labels_)
cmMean = pd.crosstab(df.Area,kmeansMean.labels_)

cm.to_csv(r'files\data_{}\confusion_matrix_kmean_{}.csv'.format(dataValue,dataValue))
cmMean.to_csv(r'files\data_{}\confusion_matrix_kmean_mean_{}.csv'.format(dataValue,dataValue))

# Random Forest Classifier

X_train, X_test, y_train, y_test = train_test_split(value, df.Area, test_size=0.2, random_state=42)
X_train_mean, X_test_mean, y_train_mean, y_test_mean = train_test_split(valueMean, df.Area, test_size=0.2, random_state=42)

model_RCF = RandomForestClassifier(n_estimators=13, random_state=42)
model_RCF.fit(X_train, y_train)
y_pred_RCF = model_RCF.predict(X_test)
accuracy_RCF = accuracy_score(y_test, y_pred_RCF)

model_mean_RCF = RandomForestClassifier(n_estimators=13, random_state=42)
model_mean_RCF.fit(X_train_mean, y_train_mean)
y_pred_mean_RCF = model_mean_RCF.predict(X_test_mean)
accuracy_mean_RCF = accuracy_score(y_test_mean, y_pred_mean_RCF)

model_knn = KNeighborsClassifier(n_neighbors=13)
model_knn.fit(X_train, y_train)
y_pred_knn = model_knn.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)

model_mean_knn = KNeighborsClassifier(n_neighbors=13)
model_mean_knn.fit(X_train_mean, y_train_mean)
y_pred_mean_knn = model_mean_knn.predict(X_test_mean)
accuracy_mean_knn = accuracy_score(y_test_mean, y_pred_mean_knn)

model_svm = SVC(kernel='linear', random_state=42)
model_svm.fit(X_train, y_train)
y_pred_svm = model_svm.predict(X_test)
accuracy_svm = accuracy_score(y_test, y_pred_svm)

model_mean_svm = SVC(kernel='linear', random_state=42)
model_mean_svm.fit(X_train_mean, y_train_mean)
y_pred_mean_svm = model_mean_svm.predict(X_test_mean)
accuracy_mean_svm = accuracy_score(y_test_mean, y_pred_mean_svm)

accuracy = r'files\data_{}\accurary_{}.txt'.format(dataValue,dataValue)

with open(accuracy, 'w') as accuracy:
    accuracy.write(f'RFC : {accuracy_RCF} \n')
    accuracy.write(f'RFC with mean : {accuracy_mean_RCF} \n')
    accuracy.write(f'KNN : {accuracy_knn} \n')
    accuracy.write(f'KNN with mean : {accuracy_mean_knn} \n')
    accuracy.write(f'SVM : {accuracy_svm} \n')
    accuracy.write(f'SVM with mean : {accuracy_mean_svm} \n')







