from paddlenlp import Taskflow
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from . models import Neo4j
import re

choices_anime = ["动画", "动画片", "番剧", "动漫","作品"]
choices_role = ["角色", "人物"]
choices_seiyuu = ["声优", "配音"]
choices_author = ["公司", "团队", "作者"]
choices_classify = ["类型", "类别", "分类"]
choices_platform = ["平台", "播放平台"]

choices_anime_do = ["有","是","的"]
choices_seiyuu_do = ["给", "配", "配音"]
choices_author_do = ["制作", "创造", "创作"]
choices_role_do = ["属于","是","的"]

class NER():
    db = 0
    index = 0

    entity_list = []
    anime_list = []
    author_list = []
    classify_list = []
    platform_list = []
    role_list = []
    seiyuu_list = []

    entity = ""
    anime = ""
    author = ""
    classify = ""
    platform = ""
    role = ""
    seiyuu = ""

    entityRelation = []

    def question_answering(self,entity):
        self.db = Neo4j()
        self.db.connectDB()
        tag = Taskflow("pos_tagging")
        self.entity = entity
        self.entity_list = tag(entity)
        self.get_major()
        if(self.anime_list or self.author_list or self.classify_list or
        self.platform_list or self.role_list or self.seiyuu_list):
            self.entityRelation = [self.anime_list, self.author_list,
                                   self.classify_list, self.platform_list,
                                   self.role_list, self.seiyuu_list]
        return self.entityRelation

    def get_major(self):
        for i in range(len(self.entity_list)):
            if (self.entity_list[i][1] == 'n'):
                if (i+1 < len(self.entity_list)):
                    if (process.extractOne(self.entity_list[i][0], choices_anime)[1] > 60):
                        if (len(self.entity_list[i + 2]) != 0):
                            self.anime = re.findall('《(.*?)》',self.entity)[0]
                            self.index = i-1
                            print(self.anime)
                            self.get_minor_anime()
                    elif (process.extractOne(self.entity_list[i][0], choices_role)[1] > 60):
                        self.role = self.entity_list[i + 1][0]
                        self.index = i-1
                        print(self.role)
                        self.get_minor_role()
                    elif (process.extractOne(self.entity_list[i][0], choices_seiyuu)[1] > 60):
                        self.seiyuu = self.entity_list[i + 1][0]
                        self.index = i-1
                        print(self.seiyuu)
                        self.get_minor_seiyuu()
                    elif (process.extractOne(self.entity_list[i][0], choices_author)[1] > 60):
                        self.author = self.entity_list[i + 1][0]
                        self.index = i-1
                        print(self.author)
                        self.get_minor_author()
                break

    def get_minor_anime(self):
        self.anime_list = self.db.name2anime(self.anime)
        for i in range(len(self.entity_list) - self.index):
            if (process.extractOne(self.entity_list[i + self.index][0], choices_anime_do)[1] > 60):
                for j in range(8):
                    if (i+self.index+j>=len(self.entity_list)):
                        break
                    if (process.extractOne(self.entity_list[i + self.index + j][0], choices_role)[1] > 60):
                        print("角色")
                        self.role_list = self.db.anime2role(self.anime)
                        break
                    elif (process.extractOne(self.entity_list[i + self.index + j][0], choices_classify)[1] > 60):
                        print("类型")
                        self.classify_list = self.db.anime2classify(self.anime)
                        break
                    elif (process.extractOne(self.entity_list[i + self.index + j][0], choices_platform)[1] > 60):
                        print("平台")
                        self.platform_list = self.db.anime2platform(self.anime)
                        break
                break

    def get_minor_role(self):
        self.role_list = self.db.name2role(self.role)
        for i in range(len(self.entity_list) - self.index):
            if (process.extractOne(self.entity_list[i + self.index][0], choices_role_do)[1] > 60):
                for j in range(8):
                    if (i+self.index+j>=len(self.entity_list)):
                        break
                    if (process.extractOne(self.entity_list[i + self.index + j][0], choices_anime)[1] > 60):
                        print("番剧")
                        self.anime_list = self.db.role2anime(self.role)
                        break
                    if (process.extractOne(self.entity_list[i + self.index + j][0], choices_seiyuu)[1] > 60):
                        print("配音")
                        self.seiyuu_list = self.db.role2seiyuu(self.role)
                        break
                break

    def get_minor_seiyuu(self):
        self.seiyuu_list = self.db.name2seiyuu(self.seiyuu)
        for i in range(len(self.entity_list) - self.index):
            if (process.extractOne(self.entity_list[i + self.index][0], choices_seiyuu_do)[1] > 60):
                for j in range(8):
                    if (i+self.index+j>=len(self.entity_list)):
                        break
                    """
                    if (process.extractOne(self.entity_list[i + self.index + j][0], choices_anime)[1] > 60):
                        print("番剧")
                        self.anime_list = self.db.
                        break
                    """
                    if (process.extractOne(self.entity_list[i + self.index + j][0], choices_role)[1] > 60):
                        print("角色")
                        self.role_list = self.db.seiyuu2role(self.seiyuu)
                        break
                break

    def get_minor_author(self):
        self.author_list = self.db.name2author(self.author)
        for i in range(len(self.entity_list) - self.index):
            if (i+self.index>=len(self.entity_list)):
                break
            if (process.extractOne(self.entity_list[i + self.index][0], choices_anime)[1] > 60):
                print("番剧")
                self.anime_list = self.db.author2anime(self.author)
                break

"""
声优花泽香菜配音过的角色
公司EMTSquared的作品
角色藤户千雪的声优是谁
番剧《普通女高中生要做当地偶像》的角色有哪些
"""