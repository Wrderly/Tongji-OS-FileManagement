import pickle
import os
import time
from fat import FAT
from block import Block
from treenode import TreeNode
from config import *


# 获取当前时间
def getTime():
    return time.localtime(time.time())


class Manager:
    def __init__(self):
        self.root = None
        self.disk = None
        self.fat = None
        self.block_num = BLOCK_NUM
        self.loadFileSystem()  # 加载数据
        self.cur = self.root
        self.path_record = ['root/']

    # 打开子节点
    def openChild(self, node: TreeNode, index):
        child_node = node.children[index]
        if child_node.type == FOLDER:
            self.cur = child_node
            self.path_record.append(self.cur.name + '/')
        elif child_node.type == FILE:
            return child_node.file.read(self.fat, self.disk)

    # 打开节点
    def openNode(self, node: TreeNode):
        if node.type == FOLDER:
            self.cur = node
            self.path_record.append(self.cur.name + '/')
        elif node.type == FILE:
            return node.file.read(self.fat, self.disk)

    # 读文件
    def readFile(self, node: TreeNode):
        if node.type != FILE:
            return ''
        return node.file.read(self.fat, self.disk)

    # 写文件
    def writeFile(self, node: TreeNode, data):
        if node.type != FILE:
            return
        node.file.write(self.fat, self.disk, data, getTime())

    # 删除文件
    def deleteFile(self, node: TreeNode):
        if node.type != FILE:
            return
        node.file.delete(self.fat, self.disk)

    # 删除子节点
    def deleteChild(self, node: TreeNode, index):
        child_node: TreeNode = node.children[index]
        if child_node.type == FOLDER:
            while child_node.children:
                self.deleteChild(child_node, 0)
            node.children.pop(index)
        elif child_node.type == FILE:
            child_node.file.delete(self.fat, self.disk)
            node.children.pop(index)

    # 创建子节点
    def createChild(self, node: TreeNode, name: str, type, data=''):
        new_node = TreeNode(name, type, getTime(), node, data)
        node.children.append(new_node)

    # 返回父节点
    def backParent(self):
        self.path_record.pop()
        self.cur = self.cur.parent

    # 获取当前路径
    def getCurPath(self):
        paths = ''
        for path in self.path_record:
            paths += path
        return paths

    # 获取当前节点指定子节点的路径
    def getCurChildPath(self, index):
        paths = ''
        for path in self.path_record:
            paths += path
        paths += self.cur.children[index].name
        return paths

    # 打印
    def show(self):
        print(' ')
        print(self.path_record)
        print(self.cur.name + '/')
        for i in range(len(self.cur.children)):
            child_node = self.cur.children[i]
            print(child_node.name.ljust(10) + ' ' + ('FILE' if child_node.type == FILE else 'FOLDER'))

    # 保存数据
    def saveFileSystem(self):
        open('fat', 'wb').write(pickle.dumps(self.fat))
        open('disk', 'wb').write(pickle.dumps(self.disk))
        open('catalog', 'wb').write(pickle.dumps(self.root))

    # 加载数据
    def loadFileSystem(self):
        if not os.path.exists('fat'):
            self.fat = FAT(self.block_num)
            open('fat', 'wb').write(pickle.dumps(self.fat))
        else:
            self.fat = pickle.load(open('fat', 'rb'))

        if not os.path.exists('disk'):
            self.disk = [Block(i) for i in range(self.block_num)]
            open('disk', 'wb').write(pickle.dumps(self.disk))
        else:
            self.disk = pickle.load(open('disk', 'rb'))

        if not os.path.exists('catalog'):
            self.root = TreeNode('root', FOLDER, getTime(), )
            open('catalog', 'wb').write(pickle.dumps(self.root))
        else:
            self.root = pickle.load(open('catalog', 'rb'))

    # 格式化
    def format(self):
        self.fat = FAT(self.block_num)
        open('fat', 'wb').write(pickle.dumps(self.fat))
        self.disk = [Block(i) for i in range(self.block_num)]
        open('disk', 'wb').write(pickle.dumps(self.disk))
        self.root = TreeNode('root', FOLDER, getTime(), )
        open('catalog', 'wb').write(pickle.dumps(self.root))
