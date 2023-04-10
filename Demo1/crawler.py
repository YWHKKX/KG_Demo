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
    name = 0
    time = 0
    size = 0
    language = 0
    content = 0

    def get_base_html(self,get):
        if get:
            res = requests.get(self.base_url,headers)
            text = res.text.encode('iso-8859-1').decode('utf-8')
            return text
        else:
            text = open('base_html.txt', encoding='utf8').read()
            return text

    def create_list(self):
        base_html = self.get_base_html(1)
        name_list = re.findall('<div class="game-name">(.*?)</div>', base_html)
        time_list = re.findall('<div>时间：<span>(.*?)</span>', base_html)
        size_list = re.findall('<div>大小：<span>(.*?)</span>', base_html)
        language_list = re.findall('<span class="game-lang">(.*?)</span>', base_html)
        content_list = []

        for i in re.findall('</div><p>(.*?)</p></div>', base_html):
            content_list.append(re.findall('<span>(.*?)</span>', i))

        for i in list(zip(name_list,time_list,size_list,language_list,content_list)):
            print(i)

        for i in range(len(name_list)):
            self.name.write(str(name_list[i]) + "\n")
            self.time.write(str(time_list[i]) + "\n")
            self.size.write(str(size_list[i]) + "\n")
            self.language.write(str(language_list[i]) + "\n")
            self.content.write(str(content_list[i])[1:-1].replace(',','').replace('\'','') + "\n")

    def run(self):
        self.name = open('data/name.txt', 'w', encoding='utf8')
        self.time = open('data/time.txt', 'w', encoding='utf8')
        self.size = open('data/size.txt', 'w', encoding='utf8')
        self.language = open('data/language.txt', 'w', encoding='utf8')
        self.content = open('data/content.txt', 'w', encoding='utf8')
        for i in range(80):
            self.base_url = self.target_url+str(i+1)
            print("now is "+self.base_url)
            self.create_list()

    def test(self):
        res = requests.get(self.target_url, headers)
        print(res.encoding)

if __name__ == '__main__':
    cra = Crawler()
    cra.run()


