import json
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import pywifi as pw
import time

keysPath = r"files\keys.json"

print("Choose treatment value")
dataValue = int(input())

researchDataPath = r'files\data_{}'.format(dataValue)

if (not os.path.exists(researchDataPath)):
    print("Unexistant value")
    exit()
else:
    df = pd.read_csv(r'files\data_{}\treated_data_{}.csv'.format(dataValue,dataValue))

value = df.drop(labels=["Position", "Version","Area"], axis=1).values[:,2:]
with open(keysPath, "r") as fichier_json:
    keys = json.load(fichier_json)

model_svm = SVC()
model_svm.fit(value,df.Area)

model_knn = KNeighborsClassifier(n_neighbors=13)
model_knn.fit(value, df.Area)
model_RCF = RandomForestClassifier(n_estimators=13, random_state=42)
model_RCF.fit(value, df.Area)

def determine_area():
    profile = pw.PyWiFi()
    iface = profile.interfaces()[0]
    iface.scan()
    results = iface.scan_results()
    iface.disconnect()

    datas = {}
    for data in results:
        bssid = data.bssid
        signal = data.signal
        datas[bssid] = signal
    new_datas = {}
    for key in keys:
        keyValue = datas.get(key)
        if keyValue is not None:
            new_datas[key] = keyValue
        else:
            new_datas[key] = -dataValue
    dataList = []
    dataList.append(new_datas)
    dfData = pd.DataFrame(dataList)
    dataList = np.array(dfData.values)

    predictions_svm = model_svm.predict(dataList)
    predictions_knn = model_knn.predict(dataList)
    predictions_RCF = model_RCF.predict(dataList)

    if predictions_knn == predictions_RCF and predictions_knn == predictions_svm :
        return predictions_knn[0]
    elif predictions_knn == predictions_RCF : 
        return (predictions_knn[0],predictions_svm[0])
    elif predictions_knn == predictions_svm : 
        return (predictions_knn[0],predictions_RCF[0])
    elif predictions_RCF == predictions_svm : 
        return (predictions_RCF[0],predictions_knn[0])
    else :
        return (predictions_RCF[0],predictions_knn[0],predictions_svm)

test_place = "y"
mode = int(input("Choose Real Time (1) or Data by Data (2) ? "))
if mode == 1 :
    while True:
        print(determine_area())
        time.sleep(3)
elif mode == 2 :
    while test_place == "y":
        test_place = str(input("Test a place ?(y/n)"))
        if test_place == "y" :
            print(determine_area())


    
    



