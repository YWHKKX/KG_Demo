# -*- coding: utf-8 -*-#

from py2neo import Graph,Node,Relationship
import os

classification = ['游戏名称','游戏标签']

class KG:
    name = open('data/name.txt', 'r', encoding='utf8')
    time = open('data/time.txt', 'r', encoding='utf8')
    size = open('data/size.txt', 'r', encoding='utf8')
    language = open('data/language.txt', 'r', encoding='utf8')
    content = open('data/content.txt', 'r', encoding='utf8')

    def createEntity(self,graph):
        cql = 'CREATE (n:游戏数据库{id:\'0\', name:\'游戏数据库\'}) RETURN n'
        graph.run(cql)

        for i, c in enumerate(classification):
            cql = '''
                MERGE (a:游戏数据库{id:\'%d\', name:\'%s\'})
                MERGE (b {name: '游戏数据库'}) 
                MERGE (b)-[:划分]->(a)
                ''' % (i+1, c)
            graph.run(cql)

        name_list = self.name.readlines()
        time_list = self.time.readlines()
        size_list = self.size.readlines()
        language_list = self.language.readlines()

        for i in range(len(name_list)):
            cql = """
                MERGE (:游戏名称{id:'%d', 名称:'%s', 语言:'%s', 大小:'%s', 发售时间:'%s'})
                """ % (i, name_list[i].replace('\n',''),language_list[i].replace('\n',''),
                       size_list[i].replace('\n',''),time_list[i].replace('\n',''))
            graph.run(cql)

        print("step 1 down")

        tmp_list = []

        for i in range(len(name_list)):
            content_list = self.content.readline().split(' ')
            for j in range(len(content_list)):
                if content_list[j] not in tmp_list:
                    tmp_list.append(content_list[j])
                    cql = 'MERGE (:游戏标签{标签:\'%s\'})' % (content_list[j].replace('\n',''))
                    graph.run(cql)

        print("step 2 down")

    def createreRationship(self,graph):
        self.name.seek(0)
        self.time.seek(0)
        self.size.seek(0)
        self.language.seek(0)
        self.content.seek(0)
        name_list = self.name.readlines()
        time_list = self.time.readlines()
        size_list = self.size.readlines()
        language_list = self.language.readlines()

        for i in range(len(name_list)):
            content_list = self.content.readline().split(' ')
            for j in range(len(content_list)):
                cql = """
                    MATCH (a:游戏名称{id:'%d', 名称:'%s', 语言:'%s', 大小:'%s', 发售时间:'%s'}),
                          (b:游戏标签{标签:'%s'})
                    MERGE (a)-[:分类]->(b)
                """ % (i,name_list[i].replace('\n',''),language_list[i].replace('\n',''),
                       size_list[i].replace('\n',''),time_list[i].replace('\n',''),
                       content_list[j].replace('\n',''))
                graph.run(cql)

        print("step 3 down")

        self.content.seek(0)
        for i in range(2):
            content_list = self.content.readline().split(' ')
            for j in range(len(content_list)):
                cql = """
                     MATCH (:游戏名称{id:'%d'})-[r:分类]->(:游戏标签{标签:'%s'})  
                     WITH count(r) as num,collect(r) as rel
                     WHERE num > 1
                     UNWIND tail(rel) as rels
                     DELETE rels
                 """ % (i,content_list[j])
                graph.run(cql)

        print("step 4 down")

if __name__ == '__main__':
    test_graph = Graph("http://127.0.0.1:7474/browser/", auth=("neo4j", "123456789"))
    test_graph.run('match(n) detach delete n')
    kg = KG()
    kg.createEntity(test_graph)
    kg.createreRationship(test_graph)
