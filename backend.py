import os
import sqlite3
import json
import get
from lxml import etree

configPath = ".\\config.json"
cachePath = ".\\cache\\"
DBPath = ".\\PhiData.db"

difList = ["EZ", "HD", "IN", "AT"]


def Text2HTML(rawStr):
    HTML = etree.HTML(rawStr, None)
    Str = HTML.xpath('//*[@id="mw-content-text"]/div/table/tbody//text()')
    return Str


def cacheStg(cacheData):
    cacheFile = open(cachePath + "songCache.cache", mode="w", encoding="utf-8")
    cacheFile.write(cacheData)
    cacheFile.close()


def cacheRead():
    cacheFile = open(cachePath + "songCache.cache", mode="r", encoding="utf-8")
    cacheData = cacheFile.read()
    cacheFile.close()
    return cacheData


def configInit():
    if not os.path.exists(configPath):
        os.makedirs(configPath)
        DBPath = input("首次使用，请输入输出数据库路径：")
        config = {"DBPath": DBPath}
        configFile = open(configPath, "w")
        configFile.write(json.dumps(config))
        configFile.close()


def DBStg(data):
    log = open("JB.log", mode="w", encoding="utf-8")
    connect = sqlite3.connect(DBPath)
    cur = connect.cursor()
    curName = "_"
    songDic = {}
    for i in range(len(data)):
        data[i] = data[i].replace("\n", "").replace("\r", "")
    while "" in data:
        data.remove("")
    for i in range(100):
        try:
            while f"[{i}]" in data:
                data.remove(f"[{i}]")
        except Exception as e:
            break
    for i in range(len(data)):
        text = data[i]
        if text == "查":
            break
        # print(text)
        log.write(text + "\n")
        if text == "所属章节":
            if data[i - 1] == "x160px":
                pre = data[i - 2]
            else:
                pre = data[i - 1]
            songDic[pre] = [("name", pre)]
            curName = pre
            # print(curName)
            # log.write(curName)
            # if len(songDic[pre]) == 3:
            #     break
            continue
        if text in difList:
            difDic = {}
            difDic["Dif"] = text
            difDic["level"] = data[i + 2]
            difDic["note"] = data[i + 3]
            difDic["Charter"] = data[i + 4]
            songDic[curName].append(difDic)
        elif i > 0:
            if (data[i - 1] == "所属章节") & (data[i + 1] == "BPM"):
                songDic[curName].append(("Chapter", data[i]))
            if (data[i - 1] == "BPM") & (data[i + 1] == "曲师"):
                songDic[curName].append(("BPM", data[i]))
            if (data[i - 1] == "曲师") & (data[i + 1] == "长度"):
                songDic[curName].append(("曲师", data[i]))
            elif (data[i - 1] == "曲师") & (data[i + 2] == "长度"):
                songDic[curName].append(("曲师", data[i] + data[i + 1]))
            if (data[i - 1] == "长度") & (data[i + 1] == "画师"):
                songDic[curName].append(("长度", data[i]))
            if (data[i - 1] == "画师") & (data[i + 1] == "难度"):
                songDic[curName].append(("画师", data[i]))
            elif (data[i - 1] == "画师") & (data[i + 2] == "难度"):
                songDic[curName].append(("画师", data[i] + data[i + 1]))
    log.close()
    for p in songDic.values():
        if len(p) == 1:
            break
        # print(p)
        St=6
        try:
            songDic = {'BPM':'UK','长度':'UK'}
            songDic[p[0][0]] = p[0][1]
            songDic[p[1][0]] = p[1][1]
            songDic[p[2][0]] = p[2][1]
            songDic[p[3][0]] = p[3][1]
            try:
                songDic[p[4][0]] = p[4][1]
                try:
                    songDic[p[5][0]] = p[5][1]
                except:
                    St-=1
                    pass
            except:
                St-=1
                pass
            difArg = ""
            noteArg = ""
            charterArg = ""
            for i in range(6, len(p)):
                Dif = f"{p[i]['Dif']}"
                difArg += f",{p[i]['level']}{Dif}"
                noteArg += f",{p[i]['note']}{Dif}"
                charterArg += f",{p[i]['Charter']}{Dif}"
            difArg = difArg[1:]
            noteArg = noteArg[1:]
            charterArg = charterArg[1:]
            cur.execute(
                """INSERT INTO PhigrosData (name,
                    cover,
                    chatper,
                    BPM,
                    length,
                    composer,
                    artist,
                    dif,
                    charter,
                    note
                    ) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (
                    songDic["name"],
                    "gugugu",
                    songDic["Chapter"],
                    songDic["BPM"],
                    songDic["长度"],
                    songDic["曲师"],
                    songDic["画师"],
                    difArg,
                    charterArg,
                    noteArg,
                ),
            )
        except Exception as e:
            print(p)
            raise (e)
    cur.close()
    connect.commit()
    connect.close()


def GetData():
    if not os.path.exists(cachePath + "songCache.cache"):
        rawData = get.getSongData()
        cacheStg(rawData)
    data = Text2HTML(cacheRead())
    DBStg(data)
