from py2neo import Graph, Node, Relationship, cypher, Path
import neo4j

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")

	def connectDB(self):
		self.graph = Graph("http://localhost:7474",auth=("neo4j", "123456789"))

	def name2anime(self,value):
		sql = "MATCH (a:番剧名称{名称:'"+str(value)+"'}) return a;"
		answer = self.graph.run(sql).data()
		return answer

	def anime2author(self,value):
		sql = "MATCH(a)-[r:制作]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def anime2classify(self,value):
		sql = "MATCH(a)-[r:类型]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def anime2platform(self,value):
		sql = "MATCH(a)-[r:播放]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def anime2role(self,value):
		sql = "MATCH(a)-[r:属于]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def name2role(self,value):
		sql = "MATCH (a:角色列表{名称:'"+str(value)+"'}) return a;"
		answer = self.graph.run(sql).data()
		return answer

	def role2anime(self,value):
		sql = "MATCH(b)-[r:属于]->(a) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def role2seiyuu(self,value):
		sql = "MATCH(a)-[r:配音]->(b) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def name2seiyuu(self,value):
		sql = "MATCH (a:声优列表{名称:'"+str(value)+"'}) return a;"
		answer = self.graph.run(sql).data()
		return answer

	def seiyuu2role(self,value):
		sql = "MATCH(b)-[r:配音]->(a) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer

	def name2author(self,value):
		sql = "MATCH (a:制作公司{名称:'"+str(value)+"'}) return a;"
		answer = self.graph.run(sql).data()
		return answer

	def author2anime(self,value):
		sql = "MATCH(b)-[r:制作]->(a) where b.名称 = '"+str(value)+"' RETURN a;"
		answer = self.graph.run(sql).data()
		return answer