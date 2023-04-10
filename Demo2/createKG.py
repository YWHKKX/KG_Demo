# -*- coding: utf-8 -*-#

from py2neo import Graph,Node,Relationship
import os

classification = ['游戏名称','游戏标签','游戏类型','游戏作者']

class KG:
    name_file = open('data/name.txt', 'r', encoding='utf8')
    size_file = open('data/size.txt', 'r', encoding='utf8')
    author_file = open('data/author.txt', 'r', encoding='utf8')
    time_file = open('data/time.txt', 'r', encoding='utf8')
    language_file = open('data/language.txt', 'r', encoding='utf8')
    content_file = open('data/content.txt', 'r', encoding='utf8')
    url_file = open('data/url.txt', 'r', encoding='utf8')
    classify_file = open('data/classify.txt', 'r', encoding='utf8')

    def createEntity(self,graph):
        cql = '''CREATE (n:游戏数据库{id:'0', name:'游戏数据库'}) RETURN n'''
        graph.run(cql)

        for i, c in enumerate(classification):
            cql = '''
                MERGE (a:游戏数据库{id:'%d', name:'%s'})
                MERGE (b {name: '游戏数据库'}) 
                MERGE (b)-[:划分]->(a)
                ''' % (i+1, c)
            graph.run(cql)

        name_list = self.name_file.readlines()
        time_list = self.time_file.readlines()
        language_list = self.language_file.readlines()
        author_list = self.author_file.readlines()
        content_list = self.content_file.readlines()

        for i in range(len(name_list)):
            cql = """
                MERGE (:游戏名称{id:'%d',名称:"%s",语言:'%s',内容简述:'%s',发售时间:'%s'})
                """ % (i, name_list[i].replace('\n',''),
                       language_list[i].replace('\n',''),
                       content_list[i].replace('\n',''),
                       time_list[i].replace('\n',''))
            graph.run(cql)

        print("step 1 down")

        author_tmp_list = []
        for i in range(len(author_list)):
            if author_list[i] not in author_tmp_list:
                author_tmp_list.append(author_list[i])
                cql = """
                    MERGE (:游戏作者{id:'%d', 名称:"%s"})
                    """ % (i, author_list[i].replace('\n',''))
                graph.run(cql)

        print("step 2 down")

        classify_tmp_list = []
        classify_tmp_list2 = []
        for i in range(len(name_list)):
            classify_list = self.classify_file.readline().split(' ')
            for j in range(len(classify_list)-1):
                if classify_list[j+1] not in classify_tmp_list:
                    classify_tmp_list.append(classify_list[j+1])
                    cql = """
                        MERGE (:游戏标签{标签:'%s'})
                        """ % (classify_list[j+1].replace('\n',''))
                    graph.run(cql)
                if classify_list[0] not in classify_tmp_list2:
                    classify_tmp_list2.append(classify_list[0])
                    cql = """
                        MERGE (:游戏类型{类型:'%s'})
                        """ % (classify_list[0].replace('\n',''))
                    graph.run(cql)

        print("step 3 down")

    def createreRationship(self,graph):
        self.name_file.seek(0)
        self.time_file.seek(0)
        self.language_file.seek(0)
        self.content_file.seek(0)
        self.author_file.seek(0)
        self.classify_file.seek(0)
        name_list = self.name_file.readlines()
        author_list = self.author_file.readlines()

        for i in range(len(name_list)):
            classify_file = self.classify_file.readline().split(' ')
            for j in range(len(classify_file)-1):
                cql = """
                    MATCH (a:游戏名称{id:'%d', 名称:"%s"}),
                          (b:游戏标签{标签:'%s'})
                    MERGE (b)-[:标签]->(a)
                """ % (i,name_list[i].replace('\n',''),
                       classify_file[j+1].replace('\n',''))
                graph.run(cql)

            cql = """
                MATCH (a:游戏名称{id:'%d', 名称:"%s"}),
                      (b:游戏类型{类型:'%s'})
                MERGE (b)-[:类型]->(a)
            """ % (i,name_list[i].replace('\n',''),
                    classify_file[0].replace('\n',''))
            graph.run(cql)

            cql = """
                MATCH (a:游戏名称{id:'%d', 名称:"%s"}),
                      (b:游戏作者{id:'%d', 名称:"%s"})
                MERGE (b)-[:制作]->(a)
            """ % (i,name_list[i].replace('\n',''),
                   i,author_list[i].replace('\n',''))
            graph.run(cql)

        print("step 4 down")

if __name__ == '__main__':
    test_graph = Graph("http://127.0.0.1:7474/browser/", auth=("neo4j", "123456789"))
    test_graph.run('match(n) detach delete n')
    kg = KG()
    kg.createEntity(test_graph)
    kg.createreRationship(test_graph)
