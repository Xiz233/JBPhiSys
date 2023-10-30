import httpx
import os

cachePath = ".\\cache"


def dataInit():
    if not os.path.exists(cachePath):
        os.makedirs(cachePath)
    cacheFile = open(f"{cachePath}\\songCache.cache", mode="w")
    cacheFile.close()


def getSongData():
    Web = "https://mzh.moegirl.org.cn/index.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/89.0.4389.128 Safari/537.36"
    }
    params = {"title": "Phigros/谱面信息"}
    try:
        req = httpx.get(Web, headers=headers, params=params, timeout=2)
        s = req.text
        # print(s)
        return s
    except Exception as e:
        print(e)
        return None
