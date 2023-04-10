from py2neo import Graph, Node, Relationship, cypher, Path
import neo4j

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")

	def connectDB(self):
		self.graph = Graph("http://localhost:7474",auth=("neo4j", "123456789"))

	def name2game(self,value):
		sql = "MATCH (n:游戏名称{名称:'"+str(value)+"'}) return n;"
		answer = self.graph.run(sql).data()
		return answer

	def game2author(self,value):
		sql = "MATCH(a)-[r:制作]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def game2classify(self,value):
		sql = "MATCH(a)-[r:类型]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def game2label(self,value):
		sql = "MATCH(a)-[r:标签]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer