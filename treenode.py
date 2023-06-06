from FCB import FCB
from config import *


# 目录节点
class TreeNode:
    def __init__(self, name: str, type, update_time, parent=None, data=''):
        self.name = name
        self.type = type
        self.last_update = update_time
        self.parent: TreeNode = parent

        if self.type == FILE:
            self.file = FCB(self.name, self.last_update)
        elif self.type == FOLDER:
            self.children: [TreeNode] = []

    def isFile(self):
        return self.type == FILE
