from config import *


# 物理存储块
class Block:
    def __init__(self, id: int, data=''):
        self.block_size = BLOCK_SIZE
        self.id = id
        self.data = data

    def read(self):
        return self.data

    def write(self, new_data: str):
        self.data = new_data[:self.block_size]
        return new_data[self.block_size:]

    def append(self, new_data: str):
        self.data += new_data[:self.block_size-len(self.data)]
        return new_data[self.block_size-len(self.data):]

    def size(self):
        return len(self.data)

    def clear(self):
        self.data = ''
