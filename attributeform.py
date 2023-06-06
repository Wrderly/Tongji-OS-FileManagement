import PyQt5.QtCore
from PyQt5.Qt import QWidget, QIcon, QGridLayout, QFont, QLabel


# 属性面板
class AttributeForm(QWidget):
    def __init__(self, node, node_path):
        super().__init__()
        # 外观设置
        self.resize(256, 196)
        self.setWindowTitle('属性')
        self.name = node.name
        self.setWindowIcon(QIcon('img/attribute.png'))
        # grid布局
        grid = QGridLayout()
        # 字体
        font = QFont()
        font.setPointSize(12)
        # 文件名
        file_name = QLabel(self)
        file_name.setText('名称:' + self.name)
        file_name.setFont(font)
        grid.addWidget(file_name, 0, 0)
        # 路径
        file_path = QLabel(self)
        if node.isFile():
            file_path.setText('文件路径:' + node_path)
        else:
            file_path.setText('目录路径:' + node_path)
        file_path.setFont(font)
        grid.addWidget(file_path, 1, 0)
        # 更新时间
        update_label = QLabel(self)
        update_time = node.last_update
        year = str(update_time.tm_year)
        month = str(update_time.tm_mon)
        day = str(update_time.tm_mday)
        hour = str(update_time.tm_hour)
        hour = hour.zfill(2)
        minute = str(update_time.tm_min)
        minute = minute.zfill(2)
        update_label.setText(f'修改时间：{year}年{month}月{day}日 {hour}:{minute}')
        update_label.setFont(font)
        if node.isFile():
            grid.addWidget(update_label, 2, 0)
        else:
            grid.addWidget(update_label, 2, 0)
            num_label = QLabel(self)
            num_label.setText('包含' + str(len(node.children)) + '个项目')
            num_label.setFont(font)
            grid.addWidget(num_label, 3, 0)
        self.setLayout(grid)
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
