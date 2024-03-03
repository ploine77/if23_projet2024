import pywifi as pw
import json
import os


text = ""
print("Quit with q")
while (text != "q"):
    ## Save current position on file named "doc.json"
    docPath = r'C:\Users\nono\if23_projet2024\doc.json'
    if (not os.path.exists(docPath)):
        oldPoint = 0
        oldVersion = 0
        with open(r"C:\Users\nono\if23_projet2024\doc.json","w") as fichier:
            info = {
                "currentPoint": oldPoint,
                "currentVersion": oldVersion
            }
            json.dump(info, fichier)
    else :
        with open(r"C:\Users\nono\if23_projet2024\doc.json","r") as fichier:
            data = json.loads(fichier.read())
            oldPoint = data['currentPoint']
            oldVersion = data['currentVersion']


    ## Create document if they don't exist
    dataPath = r'C:\Users\nono\if23_projet2024\data'
    pointPath = r"C:\Users\nono\if23_projet2024\data\position_{}".format(oldPoint)

    if (not os.path.exists(dataPath)):
        os.mkdir(dataPath)
        os.mkdir(pointPath)
    elif (not os.path.exists(pointPath)):
        os.mkdir(pointPath)

    ## Start scanning wifi
    profile = pw.PyWiFi()
    iface = profile.interfaces()[0]
    iface.scan()
    results = iface.scan_results()
    print("Current point : " + str(oldPoint))
    text = str(input("Do you want to change position (y/n) ? "))
    if (text == "y"):
        currentPoint = oldPoint + 1
        currentVersion = 1
        pointPath = r"C:\Users\nono\if23_projet2024\data\position_{}".format(currentPoint)
        os.mkdir(pointPath)
    elif(text == "n"):
        currentPoint = oldPoint
        currentVersion= oldVersion+1
        print(currentVersion)
    if (text == "y" or "n"):
        with open(r"C:\Users\nono\if23_projet2024\doc.json","w") as fichier:
                info = {
                    "currentPoint": currentPoint,
                    "currentVersion": currentVersion
                }
                print(info)
                json.dump(info, fichier)


        versionPath = r"C:\Users\nono\if23_projet2024\data\position_{}\version_{}.json".format(currentPoint,currentVersion)
        datas = {}
        count=0
        for data in results:
            info = {'ssid': data.ssid,'bssid': data.bssid,'signal': data.signal}
            if info not in datas.values():
                datas[count] = info
                count+=1

        with open(versionPath, "w") as fichier:
            json.dump(datas, fichier)

