# 保存文件信息
class FCB:
    def __init__(self, file_name, last_update):
        self.file_name = file_name  # 文件名
        self.last_update = last_update  # 文件修改时间
        self.start = -1  # 文件起始地址

    # 读文件
    def read(self, fat, disk):
        return fat.read(self.start, disk)

    # 写文件
    def write(self, fat, disk, data: str, update_time):
        fat.delete(self.start, disk)
        self.start = fat.write(data, disk)
        self.last_update = update_time

    # 删除文件
    def delete(self, fat, disk):
        fat.delete(self.start, disk)

    # 重命名文件
    def rename(self, new_name):
        self.file_name = new_name

    def size(self, fat, disk):
        return fat.size(self.start, disk)
