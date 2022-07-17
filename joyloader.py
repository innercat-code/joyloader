
import os
from pyquery import PyQuery as pq
import requests
from urllib.parse import unquote
import time
from PIL import Image
from io import BytesIO

fp = open('log.txt', 'w')
fp.write("Начало записи\n")
fp.close()

def log(s):
    fp = open('log.txt', 'a')
    fp.write(s +"\n")
    fp.close()

md = ['"', '\'', '`', ':', '*', '/', '\\', '?', '<', '>', '|', '+']

print('''
  ╔═════════════════════╤════════════╗
  ║                     │            ║
  ║  J O Y L O A D E R  │  ver. 1.5  ║
  ║                     │            ║
  ╚═════════════════════╧════════════╝
  
Парсер сайта joyreactor.cc
- Собирает картинки, качает их в папку, перелистывает по страницам, пока те не кончатся
- В файл log.txt записываются адреса сканов на случай ошибки
- 1.4 (15.07.22) сайт перешел на https, скрипт исправлен под это
- 1.5 (16.07.22) запилено скачивание полноразмерных картинок
''')

loadDir = input("Папка: ")
if loadDir == "": loadDir = "load"
if not os.path.exists(loadDir): os.mkdir(loadDir)

start = input("Ссылка: ")
if start == "": start = "https://anime.reactor.cc/tag/Anime+%D0%93%D0%B8%D1%84%D0%BA%D0%B8"
site = start.split("/")[2]
print(site)

def parseImg(url):
    print("--- PARSE URL: "+ str(url))
    log(str(url))
    d = pq(url=url)

    pretty = d(".image .prettyPhotoLink")
    for a in pretty.items():
        nm = unquote(a.attr("href").split("/")[-1])
        for c in md: nm = nm.replace(c, "")
        print("pretty: "+ nm)
        url2 = "https:"+ a.attr("href")
        img_data = requests.get(url2, headers={"Referer": url2}).content
        with open(loadDir +'/'+ nm, 'wb') as handler: handler.write(img_data)

    imgs = d(".image img")
    for img in imgs.items():
        nm = unquote(img.attr("src").split("/")[-1])
        for c in md: nm = nm.replace(c, "")
        if not os.path.exists(loadDir +'/'+ nm):
            print("img: "+ nm)
            url2 = "https:"+ img.attr("src")
            img_data = requests.get(url2, headers={"Referer": url2}).content
            with open(loadDir +'/'+ nm, 'wb') as handler: handler.write(img_data)

    gifs = d(".image span a.video_gif_source")   
    for gif in gifs.items(): 
        nm = unquote(gif.attr("href").split("/")[-1])
        for c in md: nm = nm.replace(c, "")
        print("gif: "+ nm)
        np = os.path.splitext(str(nm))[0]
        if os.path.exists(loadDir +'/'+ np +'.jpeg'): os.remove(loadDir +'/'+ np +'.jpeg')
        url2 = "https:"+ gif.attr("href")
        gif_data = requests.get(url2, headers={"Referer": url2}).content
        with open(loadDir +'/'+ nm, 'wb') as handler: handler.write(gif_data)
    
    print("Ждем")
    time.sleep(5) # не меняй, ато палучиш пожопе
    next = d("a.next")
    href = next.attr("href")
    if next.attr("href") != None: parseImg("https://"+ site + next.attr("href"))
    else: print("THE END")
    

parseImg(start)

input("ok")

fp.close()


# auto-py-to-exe