# 位图
class Bitmap:
    def __init__(self, size):
        self.size = size
        # python中整型的长度不限 自动调整
        # 以最低位为下标0
        self.bitmap = 0

    # 设置一位
    def set_bit(self, index, value):
        if value:
            self.bitmap |= (1 << index)
        else:
            self.bitmap &= ~(1 << index)

    # 获取一位
    def get_bit(self, index):
        return (self.bitmap >> index) & 1

    # 查找首个0位
    def find_first_zero(self):
        tmp_bitmap = self.bitmap
        for i in range(self.size):
            if not tmp_bitmap & 1:
                return i
            tmp_bitmap = tmp_bitmap >> 1
        return -1
