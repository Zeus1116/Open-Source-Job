from bs4 import BeautifulSoup
import re  
import urllib.request, urllib.error  
import lxml
import pandas as pd

findLink = re.compile(r'<a href="(.*?)">') 
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    for data in datalist:
        print(data)
        print("\n")
    saveData(datalist)    



# 爬取网页
def getData(baseurl):
    datalist = []  
    for i in range(0, 10): 
        url = baseurl + str(i * 25)
        html = askURL(url)  
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"): 
            data = []  # 保存一部电影所有信息
            item = str(item)
            link = re.findall(findLink, item)[0]  
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if (len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "") 
                data.append(otitle)
            else:
                data.append(titles[0])
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
            bd = re.sub('/', "", bd)
            data.append(bd.strip())
            datalist.append(data)

    return datalist

def askURL(url):
    head = {  
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def saveData(datalist):
    data_frame = pd.DataFrame(datalist,columns=['影片链接','图像链接','中文名','外文名','评分','评价数','神评','相关信息'])
    data_frame.to_csv('douban250.csv',header=False,mode='a',encoding='utf_8_sig')
    print(data_frame)

if __name__ == "__main__":  
    main()
    print("!!!!!!!")

