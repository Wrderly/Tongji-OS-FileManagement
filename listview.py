from typing import Optional
from PyQt5 import QtGui
from PyQt5.QtWidgets import QListWidget, QWidget, QAbstractItemView
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from config import *


# 文件系统显示窗口
class ListView(QListWidget):
    def __init__(self, cur_node, parents, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # 拖拽设置
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        # 选中变化事件
        self.edited_item = self.currentItem()
        self.currentItemChanged.connect(self.closeEdit)
        # 当前目录
        self.cur_node = cur_node
        # 父亲目录
        self.parents = parents
        # # 正在被编辑状态
        self.isEdit = False

    # 按键事件
    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        if e.key() == Qt.Key_Return:  # 回车事件
            self.closeEdit()

    # 鼠标点击事件
    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            item = self.itemAt(e.pos())
            if item is None:
                self.closeEdit()

    # 编辑最后一个项目
    def editLast(self, index=-1) -> None:
        self.closeEdit()
        # 获取最后一个图标
        item = self.item(self.count() - 1)
        self.setCurrentItem(item)
        self.edited_item = item
        self.openPersistentEditor(item)
        self.editItem(item)
        self.isEdit = True
        self.index = index

    # 编辑被选中项目
    def editSelected(self, index) -> None:
        self.closeEdit()
        # 获取被选中图标
        item = self.selectedItems()[-1]
        self.setCurrentItem(item)
        self.edited_item = item
        self.openPersistentEditor(item)
        self.editItem(item)
        self.isEdit = True
        self.index = index

    # 关闭编辑
    def closeEdit(self, *_) -> None:
        if self.edited_item and self.isEdit:  # 被选中图标
            self.isEdit = False
            self.closePersistentEditor(self.edited_item)
            # 重名检查
            while True:
                same_name_flag = False
                for i in range(len(self.cur_node.children) - 1):
                    if self.edited_item.text() == self.cur_node.children[i].name and self.index != i:
                        self.edited_item.setText(self.edited_item.text() + "(1)")
                        same_name_flag = True
                        break
                if not same_name_flag:
                    break
            self.cur_node.children[self.index].name = self.edited_item.text()
            self.edited_item = None
