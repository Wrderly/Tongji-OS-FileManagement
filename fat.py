from bitmap import Bitmap


class FAT:
    def __init__(self, block_num: int):
        self.block_num = block_num  # 物理块数
        self.fat = [-2 for i in range(self.block_num)]  # 初始化fat
        self.bitmap = Bitmap(size=self.block_num)  # 使用位图表示空闲块

    # 查找空闲块
    def findEmpty(self):
        return self.bitmap.find_first_zero()  # 返回位图中的第一个0的索引

    # 读文件
    def read(self, cur, disk):
        data = ''
        while cur != -1:
            data += disk[cur].read()
            cur = self.fat[cur]
        return data

    # 写文件
    def write(self, data, disk):
        start = -1
        cur = -1
        while data != '':
            index = self.findEmpty()
            if index == -1:
                print('磁盘没有空闲空间')
                return start
            if cur == -1:  # 第一次分配记录为起始地址
                start = index
            else:  # 否则保存为当前的next
                self.fat[cur] = index
            cur = index  # 取分配的地址
            data = disk[cur].write(data)  # 覆盖式写数据
            self.bitmap.set_bit(index=cur, value=1)
            self.fat[cur] = -1  # 记为尾节点
        return start

    # 文件删除
    def delete(self, cur, disk):
        while cur != -1:  # 当前地址不为空
            next = self.fat[cur]  # 保存next
            self.fat[cur] = -2  # 索引置空
            # disk[cur].clear()
            self.bitmap.set_bit(index=cur, value=0)
            cur = next
