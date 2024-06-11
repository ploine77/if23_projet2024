import pywifi as pw
import json
import time
import os


text = ""
while (text != "q"):

    # Save current position on file "doc.json"
    docPath = r'C:\Users\nono\Documents\GitHub\if23_projet2024\doc.json'
    print(os.path.abspath(os.path.curdir))
    if (not os.path.exists(docPath)):
        oldArea = 0
        oldPoint = 0
        oldVersion = 0
        with open(r"C:\Users\nono\Documents\GitHub\if23_projet2024\doc.json","w") as fichier:
            info = {
                "currentArea": oldArea,
                "currentPoint": oldPoint,
                "currentVersion": oldVersion
            }
            json.dump(info, fichier)
    else :
        # If the file "doc.json" exist, we use it to add new value
        with open(r"doc.json","r") as fichier:
            data = json.loads(fichier.read())
            oldArea = data['currentArea']
            oldPoint = data['currentPoint']
            oldVersion = data['currentVersion']


    # Create document if they don't exist
    dataPath = r'C:\Users\nono\Documents\GitHub\if23_projet2024\data'
    areaPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\area_{}".format(oldArea)
    pointPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\area_{}\position_{}".format(oldArea,oldPoint)

    if (not os.path.exists(dataPath)):
        os.mkdir(dataPath)
        os.mkdir(areaPath)
        os.mkdir(pointPath)
    elif (not os.path.exists(areaPath)):
        os.mkdir(areaPath)
        os.mkdir(pointPath)
    elif (not os.path.exists(pointPath)):
        os.mkdir(pointPath)

    print("Current area : " + str(oldArea))
    print("Current position : " + str(oldPoint))
    print("Current version : " + str(oldVersion))
    text = str(input("Do you want to change position (y/n), change area (c) or quit (q) ? "))
    if (text == "c"):
        currentArea = oldArea + 1
        currentPoint = 0
        currentVersion = 1
        areaPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\area_{}".format(currentArea)
        pointPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\area_{}\position_{}".format(currentArea,currentPoint)
        os.mkdir(areaPath)
        os.mkdir(pointPath)
        count = 5
    elif (text == "y"):
        currentArea = oldArea
        currentPoint = oldPoint + 1
        currentVersion = 1
        pointPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\area_{}\position_{}".format(currentArea,currentPoint)
        os.mkdir(pointPath)
        count = 5
    elif(text == "n"):
        currentArea = oldArea
        currentPoint = oldPoint
        currentVersion = oldVersion + 1
        count = 5
    if (text == "n" or text == "y" or text == "c"):
        while (count != 0):
            time.sleep(3)
            # Start scanning wifi
            profile = pw.PyWiFi()
            iface = profile.interfaces()[0]
            iface.scan()
            results = iface.scan_results()
            iface.disconnect()
            with open(r"doc.json","w") as fichier:
                    info = {
                        "currentArea": currentArea,
                        "currentPoint": currentPoint,
                        "currentVersion": currentVersion
                    }
                    json.dump(info, fichier)

            versionPath = r"C:\Users\nono\Documents\GitHub\if23_projet2024\data\area_{}\position_{}\version_{}.json".format(currentArea,currentPoint,currentVersion)
            datas = {}
            for data in results:
                bssid = data.bssid
                signal = data.signal
                datas[bssid] = signal

            print(versionPath)
            with open(versionPath, "w") as fichier:
                json.dump(datas, fichier)
            currentVersion += 1
            count += -1

