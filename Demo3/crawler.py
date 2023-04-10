# -*- coding: utf-8 -*-#

import os
from time import sleep
from lxml import etree
import requests, re
from urllib.parse import urljoin, urlencode
from bs4 import BeautifulSoup

headers = {
    'Accept': '',
    'Cookie': '',
    'User-Agent': ''
}

class Crawler:
    target_url = 'https://www.bnacg.com/dm/list_1_'
    base_url = ''
    name_file = 0
    platform_file = 0
    seiyuu_file = 0
    classify_file = 0
    role_name_file = 0
    role_img_file = 0
    author_file = 0

    def get_base_html(self,url):
        res = requests.get(url,headers)
        text = res.text.encode('ISO-8859-1').decode('utf-8')
        return text

    def create_list(self):
        base_html = self.get_base_html(self.base_url)
        soup = BeautifulSoup(base_html, 'html.parser')
        html = soup.findAll("ul", {"class": "result-list"})

        url_list = re.findall('<a class="img-wrap" href="(.*?)" rel="nofollow"', str(html))

        name_list = []
        author_list = []
        role_img_list = []
        role_name_list = []
        classify_list = []
        seiyuu_list =[]
        platform_list = []

        for url in url_list:
            url_html = self.get_base_html(url)
            soup = BeautifulSoup(url_html, 'html.parser')
            name = re.findall('<div class="ts18 bold"> (.*?) /', str(url_html))
            classify = re.findall('<div class="rw_ju"> <span class="bold">类型：</span>(.*?)</div>',url_html)
            role_name = re.findall('title="(.*?)" alt="',url_html)
            role_img = re.findall('<img src="(.*?)" title="',url_html)
            seiyuu = re.findall('<div class="rw_ju"> <span class="bold">人物配音：</span>(.*?)</div>',url_html)
            author = re.findall('<dd class="canshu value">(.*?)</dd>',url_html)

            for i in range(len(role_name)):
                role_name[i] = str(role_name[i]).replace(" ","")

            name_list.append(name[0])
            role_img_list.append(role_img[1:])
            role_name_list.append(role_name)
            author_list.append(author[2])
            platform_list.append(author[3])
            seiyuu_list.append(seiyuu)

            if(len(classify) != 0):
                classify_list.append(classify[0].split(','))

        #for i in list(zip(name_list,author_list,platform_list,classify_list,seiyuu_list,role_name_list,role_img_list)):
            #print(i)

        for i in range(25):
            if(len(role_img_list[i])!=len(role_img_list[i])):
                print(role_img_list[i])
                print(role_name_list[i])

        for i in range(len(name_list)):
            self.name_file.write(str(name_list[i].replace('《', '').replace('》', '')) + "\n")
            self.author_file.write(str(author_list[i].replace(' ','')) + "\n")
            self.platform_file.write(str(platform_list[i].replace(' ','')) + "\n")
            self.classify_file.write(str(classify_list[i])[1:-1].replace('\'','').replace(',','') + "\n")
            self.seiyuu_file.write(str(seiyuu_list[i])[1:-1].replace('\'', '').replace(',', '') + "\n")
            self.role_name_file.write(str(role_name_list[i])[1:-1].replace('\'', '').replace(',', '') + "\n")
            self.role_img_file.write(str(role_img_list[i])[1:-1].replace('\'', '').replace(',', '') + "\n")

    def run(self):
        self.name_file = open('data/name.txt', 'w', encoding='utf8')
        self.author_file = open('data/author.txt', 'w', encoding='utf8')
        self.role_name_file = open('data/role_name.txt', 'w', encoding='utf8')
        self.role_img_file = open('data/role_img.txt', 'w', encoding='utf8')
        self.platform_file = open('data/platform.txt', 'w', encoding='utf8')
        self.seiyuu_file = open('data/seiyuu.txt', 'w', encoding='utf8')
        self.classify_file = open('data/classify.txt', 'w', encoding='utf8')

        for i in range(30):
            self.base_url = self.target_url + str(i+1) + ".html"
            print("Now is: " + self.base_url)
            self.create_list()

    def test(self):
        res = requests.get(self.target_url, headers)
        print(res.encoding)

if __name__ == '__main__':
    cra = Crawler()
    cra.run()


