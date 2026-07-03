---
title: html video blob视频下载
id: 1355
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 现在视频链接一般为m3u8,找到m3u8地址就可以下载了打开ChromeDeveloper工具，然后点击“网络”标签。导航到包含视频的页面，然后开始播放。将文件列表过滤为“m3u8”。找到master.m3u8或index.m3u8并单击它。将文件保存到磁盘并在其中查看。如果文件包含一个m3u8主U
permalink: /archives/html-video-blob-shi-pin-xia-zai/
categories:
- python基础教程
tags:
- 爬虫
---

现在视频链接一般为m3u8,找到m3u8地址就可以下载了
1. 打开Chrome Developer工具，然后点击“网络”标签。
2. 导航到包含视频的页面，然后开始播放。
3. 将文件列表过滤为“ m3u8”。
4. 找到master.m3u8或index.m3u8并单击它。
5. 将文件保存到磁盘并在其中查看。
6. 如果文件包含一个m3u8主URL，则复制该URL。
7. 使用ffmpeg 工具下载m3u8视频
```
ffmpeg -i "https://secure.brightcove.com/services/mobile/streaming/index/rendition.m3u8?assetId=6138283938001&secure=true&videoId=6138277786001" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 6138277786001.mp4
```
Python下载代码
```python
#!/usr/bin/env python3
import requests,urllib
from bs4 import BeautifulSoup
import os
import subprocess

pwd = os.path.split(os.path.realpath(__file__))[0]

url = "https://www.topgear.com/videos"

headers = {
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cookie': "has_js=1; minVersion={\"experiment\":1570672462,\"minFlavor\":\"new_vermi-1.13.7.11.js100\"}; minUniq=%7B%22minUID%22%3A%22bb80328a30-e8cdeb4d55-9a314411d2-aff4bb11a6-4aa23e3779%22%7D; minDaily=%7B%22testMode%22%3Atrue%2C%22dailyUser%22%3Atrue%7D; __gads=ID=b6eee23a8df86f72:T=1588041695:S=ALNI_MYCQR1Bf2fq53bqISIZBy8kIgI9oA; minBuffer=%7B%22minAnalytics%22%3A%22%7B%5C%22clicks%5C%22%3A%5B%5D%2C%5C%22clicksDelay%5C%22%3A%5B%5D%7D%22%2C%22_minEE1%22%3A%22%5B%5D%22%7D; minSession=%7B%22minSID%22%3A%227f32fd50ab-88cc4cf6f3-68d284cdee-1faeb65c08-c5966d76ac%22%2C%22minSessionSent%22%3Atrue%2C%22hadImp%22%3Atrue%2C%22sessionUniqs%22%3A%22%7Btime%3A1588053248571%2Clist%3A%5B11206251nt0%5D%7D%22%7D; OptanonConsent=landingPath=NotLandingPage&datestamp=Tue+Apr+28+2020+13%3A55%3A33+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=3.6.24&AwaitingReconsent=false&groups=1%3A1%2C101%3A0%2C2%3A0%2C0_132429%3A0%2C3%3A0%2C4%3A0%2C0_132431%3A0%2C104%3A0%2C106%3A0%2C111%3A0%2C114%3A0%2C120%3A0%2C124%3A0%2C126%3A0%2C130%3A0%2C133%3A0%2C134%3A0%2C144%3A0%2C145%3A0%2C146%3A0%2C147%3A0%2C150%3A0%2C151%3A0%2C157%3A0%2C162%3A0%2C173%3A0%2C0_126679%3A0%2C0_137695%3A0%2C0_132361%3A0%2C0_132391%3A0; GED_PLAYLIST_ACTIVITY=W3sidSI6Ijh5clQiLCJ0c2wiOjE1ODgwNTMzNDksIm52IjowLCJ1cHQiOjE1ODgwNTMzMzMsImx0IjoxNTg4MDUzMzM3fV0.",
    'cache-control': "no-cache"}

if __name__ == '__main__':
    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    videoId = soup.find_all('video', class_="video-js")[0]['data-video-id'] ##获取视频Id
    title = soup.find_all('h1', class_="video-player__title")[0].contents[0] ##获取视频标题
    url = "https://secure.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId={}&secure=true".format(videoId)  ##生成视频下载Url
    filename = '{}.mp4'.format(title).replace(" ","-")
    cmd_str = 'ffmpeg -i \"' + url + '\" ' + '-acodec copy -vcodec copy -absf aac_adtstoasc ' + pwd + "/" +filename  ##下载视频
    print(cmd_str)
    subprocess.call(cmd_str,shell=True)
```

更多Python相关教程
1. [Python基础教程](https://www.tushu.info/archives/Python-ji-chu-jiao-cheng)
2. [在SublimeEditor中配置Python环境](https://www.tushu.info/archives/zai-Sublime-Editor-zhong-pei-zhi-Python)
3. [Python代码中添加注释](https://www.tushu.info/archives/Python-dai-ma-zhong-tian-jia-zhu-shi)
4. [Python中的变量的使用](https://www.tushu.info/archives/Python-zhong-de-bian-liang-de-shi-yong)
5. [Python中的数据类型](https://www.tushu.info/archives/Python-zhong-de-shu-ju-lei-xing)
6. [Python中的关键字](https://www.tushu.info/archives/Python-zhong-de-guan-jian-zi)
7. [Python字符串操作](https://www.tushu.info/archives/Python-zi-fu-chuan-cao-zuo)
8. [Python中的list操作](https://www.tushu.info/archives/Python-zhong-de-list-cao-zuo)
9. [Python中的Tuple操作](https://www.tushu.info/archives/Python-zhong-de-Tuple-cao-zuo)
10. [Pythonmax（）和min（）–在列表或数组中查找最大值和最小值](https://www.tushu.info/archives/Python-max-he-min-zai-lie-biao-huo-shu)
11. [Python找到最大的N个（前N个）或最小的N个项目](https://www.tushu.info/archives/Python-zhao-dao-zui-da-de-N-ge-qian-N)
12. [Python读写CSV文件](https://www.tushu.info/archives/Python-du-xie-CSV-wen-jian)
13. [Python中使用httplib2–HTTPGET和POST示例](https://www.tushu.info/archives/Python-zhong-shi-yong-httplib2-HTTP-GET)
14. [Python将tuple开箱为变量或参数](https://www.tushu.info/archives/Python-jiang-tuple-kai-xiang-wei-bian)
15. [Python开箱Tuple–太多值无法解压](https://www.tushu.info/archives/Python-kai-xiang-Tuple-tai-duo-zhi-wu)
16. [Pythonmultidict示例–将单个键映射到字典中的多个值](https://www.tushu.info/archives/Python-multidict-shi-li-jiang-dan-ge)
17. [PythonOrderedDict–有序字典](https://www.tushu.info/archives/Python-OrderedDict-you-xu-zi-dian)
18. [Python字典交集–比较两个字典](https://www.tushu.info/archives/Python-zi-dian-jiao-ji-bi-jiao-liang-ge)
19. [Python优先级队列示例](https://www.tushu.info/archives/Python-you-xian-ji-dui-lie-shi-li)
20. [python中如何格式化日期](https://www.tushu.info/archives/Python-zhong-ru-he-ge-shi-hua-ri-qi)
21. [30 分钟 Python 爬虫教程](https://www.tushu.info/archives/30-fen-zhong-Python-pa-chong-jiao-cheng)
22. [爬虫下载网页视频(video blob)](https://www.tushu.info/archives/html-video-blob-shi-pin-xia-zai)