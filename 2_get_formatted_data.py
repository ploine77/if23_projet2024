import os
import json
import pandas as pd

docPath = 'data'

keysList = []
count = 2

# We treat all data to set NaN if at a position we have an unknown wifi sources
for area in os.listdir(docPath):
    areaPath = r"data\{}".format(area)
    for position in os.listdir(areaPath):
        positionPath = r"data\{}\{}".format(area,position)
        for value in os.listdir(positionPath):
            valuePath = r"data\{}\{}\{}".format(area,position,value)
            with open(valuePath, "r") as fichier_json:
                valueDatas = json.load(fichier_json)
            keys = valueDatas.keys()
            for key in keys:
                if key not in keysList:
                    keysList.append(key)

filesPath = 'files'

if (not os.path.exists(filesPath)):
    os.mkdir(filesPath)

keysPath = r"files\keys.json"
with open(keysPath, "w") as fichier_json:
    json.dump(keysList, fichier_json, indent=5)

datas = {}
dfDatas = []

for area in os.listdir(docPath):
    areaPath = r"data\{}".format(area)
    datas[area]={}
    for position in os.listdir(areaPath):
        positionPath = "data\{}\{}".format(area,position)
        datas[area][position] = {}
        count = 0
        dfData = []
        for value in os.listdir(positionPath):
            valuePath = r"data\{}\{}\{}".format(area,position,value)
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

df = pd.DataFrame(dfDatas)

untreatedDataPath = r'files\untreatedData'

if (not os.path.exists(untreatedDataPath)):
    os.mkdir(untreatedDataPath)

# Save file as csv with NaN
df.to_csv(r'files\untreatedData\untreatedData.csv')

# Save file as json
dataPath = r"files\untreatedData\untreatedData.json"
with open(dataPath, "w") as fichier_json:
    json.dump(datas, fichier_json, indent=5)