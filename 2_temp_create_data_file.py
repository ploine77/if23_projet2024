import os
import json
import pandas as pd
import numpy as np

docPath = r'C:\Users\nono\Documents\GitHub\if23_projet2024\data'

keysList = []
count = 2

# We treat all data to set NaN if at a position we have an unknown wifi sources
for area in os.listdir(docPath):
    areaPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\{}".format(area)
    for position in os.listdir(areaPath):
        positionPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\{}\{}".format(area,position)
        for value in os.listdir(positionPath):
            valuePath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\{}\{}\{}".format(area,position,value)
            with open(valuePath, "r") as fichier_json:
                valueDatas = json.load(fichier_json)
            keys = valueDatas.keys()
            for key in keys:
                if key not in keysList:
                    keysList.append(key)

keysPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\files\keys.json"
with open(keysPath, "w") as fichier_json:
    json.dump(keysList, fichier_json, indent=5)

datas = {}
dfDatas = []

for area in os.listdir(docPath):
    areaPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\{}".format(area)
    datas[area]={}
    for position in os.listdir(areaPath):
        positionPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\{}\{}".format(area,position)
        datas[area][position] = {}
        count = 0
        dfData = []
        for value in os.listdir(positionPath):
            valuePath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\{}\{}\{}".format(area,position,value)
            datas[area][position][count]={}
            with open(valuePath, "r") as fichier_json:
                valueDatas = json.load(fichier_json)
            for key in keysList:
                keyValue = valueDatas.get(key)
                if keyValue is not None:
                    datas[area][position][count][key] = keyValue
                else:
                    datas[area][position][count][key] = "NaN"
            count += 1
            data = {"Version":value,"Area": area, "Position": position}
            for key in keysList:
                data[key] = valueDatas.get(key, "NaN")
            dfDatas.append(data)


dfNaN = pd.DataFrame(dfDatas)

# Save file as csv with NaN
dfNaN.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedDataNaN.csv')

# Save file as json
dataPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\files\data_with_pos.json"
with open(dataPath, "w") as fichier_json:
    json.dump(datas, fichier_json, indent=5)

dfNaN.replace("NaN", np.nan, inplace=True)

df95 = dfNaN.copy()
dfMean = dfNaN.copy()
df0 = dfNaN.copy()
df200 = dfNaN.copy()

count = 0
for column in df95.columns[3:]:
    count+=1
    for area in df95['Area'].unique():
        for position in df95['Position'].unique():
            columnsPos = (df95['Area'] == area) & (df95['Position'] == position)
            df95.loc[columnsPos, column] = df95.loc[columnsPos, column].fillna(-95)
        columnArea = (df95['Area'] == area)
        df95.loc[columnArea, column] = df95.loc[columnArea, column].fillna(-95)

df95.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData95.csv')

count = 0
for column in df0.columns[3:]:
    count+=1
    for area in df0['Area'].unique():
        for position in df0['Position'].unique():
            columnsPos = (df0['Area'] == area) & (df0['Position'] == position)
            df0.loc[columnsPos, column] = df0.loc[columnsPos, column].fillna(0)
        columnArea = (df0['Area'] == area)
        df0.loc[columnArea, column] = df0.loc[columnArea, column].fillna(0)

df0.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData0.csv')

count = 0
for column in df200.columns[3:]:
    count+=1
    for area in df200['Area'].unique():
        for position in df200['Position'].unique():
            columnsPos = (df200['Area'] == area) & (df200['Position'] == position)
            df200.loc[columnsPos, column] = df200.loc[columnsPos, column].fillna(-200)
        columnArea = (df200['Area'] == area)
        df200.loc[columnArea, column] = df200.loc[columnArea, column].fillna(-200)

df200.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedData200.csv')


count = 0
for column in dfMean.columns[3:]:
    count+=1
    for area in dfMean['Area'].unique():
        for position in dfMean['Position'].unique():
            columnsPos = (dfMean['Area'] == area) & (dfMean['Position'] == position)
            meanPos = dfMean.loc[columnsPos, column].mean()
            dfMean.loc[columnsPos, column] = dfMean.loc[columnsPos, column].fillna(meanPos)
        columnArea = (dfMean['Area'] == area)
        meanArea = dfMean.loc[columnArea, column].mean()
        if np.isnan(meanArea):
            meanArea = -95
        dfMean.loc[columnArea, column] = dfMean.loc[columnArea, column].fillna(meanArea)

dfMean.to_csv(r'C:\Users\nono\Documents\GitHub\if23_projet2024\files\treatedDataMean.csv')




