# -*- coding: utf-8 -*-#

import os
from time import sleep
from lxml import etree
import requests, re
from urllib.parse import urljoin, urlencode
import pprint

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
}

class Crawler:
    target_url = 'https://down.ali213.net/pcgame/all/0-0-0-0-new-pic-'
    base_url = ''
    name_file = 0
    time_file = 0
    size_file = 0
    language_file = 0
    content_file = 0
    url_file = 0
    classify_file = 0

    def get_base_html(self,url):
        res = requests.get(url,headers)
        text = res.text.encode('iso-8859-1').decode('utf-8')
        return text

    def create_list(self):
        base_html = self.get_base_html(self.base_url)
        url_list = re.findall('<div class="famous-li"><a href="(/pcgame/.*?.html)" target="_blank" class="content-a">', base_html)

        name_list = []
        author_list = []
        language_list = []
        time_list = []
        classify_list = []

        for url in url_list:
            url_html = self.get_base_html("https://down.ali213.net/"+url)
            name_language = re.findall('<h1>(.*?)</h1>', url_html)
            author = re.findall('<li>游戏发行.(.*?)</li>', url_html)
            time = re.findall('<a href="/pcgame/all/0-0-(.*?)-0-new-pic-1.html" target', url_html)
            classify = re.findall('-new-pic-1.html" target="_blank">(.*?)</a>',url_html)
            content = re.findall('<p>\u3000\u3000(.*?)</p>',url_html)

            name_language = str(name_language[0]).rsplit(" ",1)
            name = str(name_language[0])
            language = str(name_language[1])
            author = str(author[0])
            time = str(time[0])
            del classify[1:3]

            name_list.append(name)
            author_list.append(author)
            time_list.append(time)
            language_list.append(language)
            classify_list.append(classify)

            if len(content) == 0:
                self.content_file.write('\n')
            else:
                self.content_file.write(str(content[0])+'\n')

        for i in list(zip(name_list,author_list,time_list,language_list,classify_list)):
            print(i)

        for i in range(len(name_list)):
            self.name_file.write(str(name_list[i]) + "\n")
            self.time_file.write(str(time_list[i]) + "\n")
            self.language_file.write(str(language_list[i]) + "\n")
            self.author_file.write(str(author_list[i]) + "\n")
            self.url_file.write(str(url_list[i]) + "\n")
            self.classify_file.write(str(classify_list[i])[1:-1].replace(',', '').replace('\'', '') + "\n")

    def run(self):
        self.name_file = open('data/name.txt', 'w', encoding='utf8')
        self.size_file = open('data/size.txt', 'w', encoding='utf8')
        self.author_file = open('data/author.txt', 'w', encoding='utf8')
        self.time_file = open('data/time.txt', 'w', encoding='utf8')
        self.language_file = open('data/language.txt', 'w', encoding='utf8')
        self.content_file = open('data/content.txt', 'w', encoding='utf8')
        self.url_file = open('data/url.txt', 'w', encoding='utf8')
        self.classify_file = open('data/classify.txt', 'w', encoding='utf8')
        for i in range(30):
            self.base_url = self.target_url+str(i+1)
            print("now is "+self.base_url)
            self.create_list()

    def test(self):
        res = requests.get(self.target_url, headers)
        print(res.encoding)

if __name__ == '__main__':
    cra = Crawler()
    cra.run()


