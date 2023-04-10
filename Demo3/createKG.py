# -*- coding: utf-8 -*-#

from py2neo import Graph,Node,Relationship
import os

classification = ['番剧名称','番剧类型','角色列表','声优列表','播放平台','制作公司']

class KG:
    name_file = open('data/name.txt', 'r', encoding='utf8')
    platform_file = open('data/platform.txt', 'r', encoding='utf8')
    author_file = open('data/author.txt', 'r', encoding='utf8')
    role_img_file = open('data/role_img.txt', 'r', encoding='utf8')
    role_name_file = open('data/role_name.txt', 'r', encoding='utf8')
    seiyuu_file = open('data/seiyuu.txt', 'r', encoding='utf8')
    classify_file = open('data/classify.txt', 'r', encoding='utf8')

    def createEntity(self,graph):
        cql = '''CREATE (n:番剧数据库{id:'0', name:'番剧数据库'}) RETURN n'''
        graph.run(cql)

        for i, c in enumerate(classification):
            cql = '''
                MERGE (a:番剧数据库{id:'%d', name:'%s'})
                MERGE (b {name: '番剧数据库'}) 
                MERGE (b)-[:划分]->(a)
                ''' % (i+1, c)
            graph.run(cql)

        name_list = self.name_file.readlines()
        author_list = self.author_file.readlines()
        platform_list = self.platform_file.readlines()

        for i in range(len(name_list)):
            cql = """
                MERGE (:番剧名称{id:'%d',名称:"%s"})
                """ % (i, name_list[i].replace('\n',''))
            graph.run(cql)

        print("step 1 down")

        author_tmp_list = []
        platform_tmp_list = []
        for i in range(len(name_list)):
            if author_list[i] not in author_tmp_list:
                author_tmp_list.append(author_list[i])
                cql = """
                    MERGE (:制作公司{id:'%d', 名称:"%s"})
                    """ % (i, author_list[i].replace('\n',''))
                graph.run(cql)
            if platform_list[i] not in platform_tmp_list:
                platform_tmp_list.append(platform_list[i])
                cql = """
                    MERGE (:播放平台{id:'%d', 名称:"%s"})
                    """ % (i, platform_list[i].replace('\n', ''))
                graph.run(cql)

        print("step 2 down")

        classify_tmp_list = []
        seiyuu_tmp_list = []
        for i in range(len(name_list)):
            classify_list = self.classify_file.readline().split(' ')
            seiyuu_list = self.seiyuu_file.readline().split(' ')
            role_name_list = self.role_name_file.readline().split(' ')
            role_img_list = self.role_img_file.readline().split(' ')
            for j in range(len(classify_list)):
                if classify_list[j] not in classify_tmp_list:
                    classify_tmp_list.append(classify_list[j])
                    cql = """
                        MERGE (:番剧类型{类型:'%s'})
                        """ % (classify_list[j].replace('\n',''))
                    graph.run(cql)
            for j in range(len(seiyuu_list)):
                if seiyuu_list[j] not in seiyuu_tmp_list:
                    seiyuu_tmp_list.append(seiyuu_list[j])
                    cql = """
                        MERGE (:声优列表{名称:'%s'})
                        """ % (seiyuu_list[j].replace('\n',''))
                    graph.run(cql)
            for j in range(len(role_name_list)):
                if (len(role_name_list)!=len(role_img_list)):
                    print(role_name_list[j])
                    print(role_img_list[j])
                cql = """
                    MERGE (:角色列表{名称:'%s',图片:'%s'})
                    """ % (role_name_list[j].replace('\n',''),role_img_list[j].replace('\n',''))
                graph.run(cql)

        print("step 3 down")

    def createreRationship(self,graph):
        self.name_file.seek(0)
        self.seiyuu_file.seek(0)
        self.platform_file.seek(0)
        self.role_name_file.seek(0)
        self.role_img_file.seek(0)
        self.author_file.seek(0)
        self.classify_file.seek(0)

        name_list = self.name_file.readlines()
        author_list = self.author_file.readlines()
        platform_list = self.platform_file.readlines()

        for i in range(len(name_list)):
            classify_list = self.classify_file.readline().split(' ')
            role_name_list = self.role_name_file.readline().split(' ')
            role_img_list = self.role_img_file.readline().split(' ')
            seiyuu_list = self.seiyuu_file.readline().split(' ')

            for j in range(len(classify_list)-1):
                cql = """
                    MATCH (a:番剧名称{id:'%d', 名称:"%s"}),
                          (b:番剧类型{类型:'%s'})
                    MERGE (b)-[:类型]->(a)
                """ % (i,name_list[i].replace('\n',''),
                       classify_list[j].replace('\n',''))
                graph.run(cql)

            for j in range(len(role_name_list)):
                cql = """
                    MATCH (a:番剧名称{id:'%d', 名称:"%s"}),
                          (b:角色列表{名称:'%s',图片:'%s'})
                    MERGE (b)-[:属于]->(a)
                """ % (i,name_list[i].replace('\n',''),
                       role_name_list[j].replace('\n',''),
                       role_img_list[j].replace('\n',''))
                graph.run(cql)

                cql = """
                    MATCH (a:声优列表{名称:"%s"}),
                          (b:角色列表{名称:'%s',图片:'%s'})
                    MERGE (a)-[:配音]->(b)
                """ % (seiyuu_list[j].replace('\n', ''),
                       role_name_list[j].replace('\n', ''),
                       role_img_list[j].replace('\n', ''))
                graph.run(cql)

            cql = """
                MATCH (a:番剧名称{id:'%d', 名称:"%s"}),
                      (b:制作公司{名称:"%s"})
                MERGE (b)-[:制作]->(a)
            """ % (i,name_list[i].replace('\n',''),
                   author_list[i].replace('\n',''))
            graph.run(cql)

            cql = """
                MATCH (a:番剧名称{id:'%d', 名称:"%s"}),
                      (b:播放平台{名称:"%s"})
                MERGE (b)-[:播放]->(a)
            """ % (i,name_list[i].replace('\n',''),
                   platform_list[i].replace('\n',''))
            graph.run(cql)

        print("step 4 down")

if __name__ == '__main__':
    test_graph = Graph("http://127.0.0.1:7474/browser/", auth=("neo4j", "123456789"))
    test_graph.run('match(n) detach delete n')
    kg = KG()
    kg.createEntity(test_graph)
    kg.createreRationship(test_graph)
