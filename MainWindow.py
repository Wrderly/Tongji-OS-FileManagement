from PyQt5.Qt import *
from manager import Manager
from listview import ListView
from fileEditor import EditForm
from attributeform import AttributeForm
from config import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建文件系统管理器
        self.manager = Manager()
        # 窗口创建
        self.resize(1080, 720)
        self.setWindowTitle('操作系统课程项目 文件管理系统')
        # 窗口布局
        grid = QGridLayout()
        grid.setSpacing(10)
        self.widGet = QWidget()
        self.widGet.setLayout(grid)
        self.setCentralWidget(self.widGet)
        # 菜单栏
        menu_bar = self.menuBar()
        # 添加菜单
        menu_bar.addAction('格式化', self.format)
        self.tool_bar = self.addToolBar('工具栏')
        # 返回
        self.backAction = QAction(QIcon('img/back.png'), '&返回', self)
        self.backAction.triggered.connect(self.backEvent)
        self.tool_bar.addAction(self.backAction)
        self.backAction.setEnabled(False)
        self.tool_bar.addSeparator()
        # 当前所在路径
        self.cur_path = QLineEdit()
        self.cur_path.setText('root/')
        self.cur_path.setReadOnly(True)
        # 图标
        self.cur_path.addAction(QIcon('img/folder.png'), QLineEdit.LeadingPosition)
        self.cur_path.setMinimumHeight(40)
        ptr_layout = QFormLayout()
        ptr_layout.addRow(self.cur_path)
        ptr_widget = QWidget()
        ptr_widget.setLayout(ptr_layout)
        ptr_widget.adjustSize()
        self.tool_bar.addWidget(ptr_widget)
        self.tool_bar.setMovable(False)
        # 文件显示窗口
        self.list_view = ListView(self.manager.cur, parents=self)
        self.list_view.setMinimumHeight(600)
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setIconSize(QSize(72, 72))
        self.list_view.setGridSize(QSize(100, 100))
        self.list_view.setResizeMode(QListView.Adjust)
        self.list_view.setMovement(QListView.Static)
        self.list_view.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.list_view.doubleClicked.connect(self.openFile)
        self.loadCurFile()
        grid.addWidget(self.list_view, 1, 1)
        # 右击菜单绑定
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_menu)
        # 底栏信息
        self.update_bottom_label()

    # 加载文件信息图标 仅在打开/退出文件夹时调用
    def loadCurFile(self):
        # 清空
        self.list_view.clear()
        for node in self.manager.cur.children:
            if node.type == FILE:
                self.item = QListWidgetItem(QIcon("img/file.png"), node.name)
                self.list_view.addItem(self.item)
            else:
                if len(node.children) == 0:  # 空文件夹
                    self.item = QListWidgetItem(QIcon("img/folder.png"), node.name)
                else:
                    self.item = QListWidgetItem(QIcon("img/folderWithFile.png"), node.name)
                self.list_view.addItem(self.item)

    # 打开文件
    def openFile(self, modelindex: QModelIndex)->None:
        # 关闭编辑
        self.list_view.closeEdit()
        # 获取点击的图标
        try:  # 双击
            item = self.list_view.item(modelindex.row())
        except:  # 右键
            if len(self.list_view.selectedItems()) == 0:
                return
            item = self.list_view.selectedItems()[-1]
        clicked_node = None
        # 根据文件名从文件系统中获取节点
        for node in self.manager.cur.children:
            if node.name == item.text():
                clicked_node = node
                break
        if clicked_node.type == FILE:  # 打开文件
            data = self.manager.readFile(clicked_node)
            # 在界面上创建文本编辑器子节点并绑定写文件事件
            self.child = EditForm(clicked_node.name, data)
            self.child._signal.connect(self.writeEvent)
            self.child.show()
            self.file_be_writen = clicked_node  # 记录被写文件 在写文件事件中被调用
        elif clicked_node.type == FOLDER:  # 进入下一级目录
            # 关编辑
            self.list_view.closeEdit()
            # 打开文件夹
            self.manager.openNode(clicked_node)
            # 加载新的界面
            self.loadCurFile()
            self.list_view.cur_node = self.manager.cur
            # 允许返回上一级事件
            self.backAction.setEnabled(True)
            # 更新底栏
            self.update_bottom_label()

    # 删除文件
    def deleteFile(self):
        if len(self.list_view.selectedItems()) == 0:
            return
        # 获取被选中图标
        item = self.list_view.selectedItems()[-1]
        index = self.list_view.selectedIndexes()[-1].row()
        # 提示框
        reply = QMessageBox()
        reply.setWindowTitle('提醒')
        if self.manager.cur.children[index].type == FILE:
            reply.setText('确定要删除文件' + item.text() + '吗？')
        else:
            reply.setText('确定要删除文件夹' + item.text() + '及其内部所有文件吗？')
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button_yes = reply.button(QMessageBox.Yes)
        button_yes.setText('确定')
        button_no = reply.button(QMessageBox.No)
        button_no.setText('取消')
        reply.exec_()

        if reply.clickedButton() == button_no:
            return
        # 加载界面
        self.listView.takeItem(index)
        del item
        # 删除文件(子节点)
        self.manager.deleteChild(self.manager.cur, index)
        # 更新底栏
        self.update_bottom_label()

    # 重命名
    def rename(self):
        if len(self.list_view.selectedItems()) == 0:
            return
        self.list_view.editSelected(self.list_view.selectedIndexes()[-1].row())

    # 创建文件夹
    def createFolder(self):
        self.list_view.closeEdit()
        self.item = QListWidgetItem(QIcon("img/folder.png"), "新建文件夹")
        self.list_view.addItem(self.item)
        self.list_view.editLast(self.list_view.count() - 1)
        self.manager.createChild(self.manager.cur, "新建文件夹", FOLDER)

    # 创建文件
    def createFile(self):
        self.list_view.closeEdit()
        self.item = QListWidgetItem(QIcon("img/file.png"), "新建文件")
        self.list_view.addItem(self.item)
        self.list_view.editLast(self.list_view.count() - 1)
        self.manager.createChild(self.manager.cur, "新建文件", FILE)

    # 底栏
    def update_bottom_label(self):
        self.statusBar().showMessage(str(len(self.manager.cur.children)) + '个项目'.ljust(211) + '学号:2154168 姓名:王鹏')
        s = ''
        for i in range(len(self.manager.path_record)):
            s += self.manager.path_record[i]
        self.cur_path.setText(s)

    # 查看属性面板
    def viewAttribute(self):
        if len(self.list_view.selectedItems()) == 0:  # 选中的当前目录
            path = self.manager.getCurPath()
            self.child = AttributeForm(self.manager.cur, path)
            self.child.show()
        else:
            index = self.list_view.selectedIndexes()[-1].row()
            node = self.manager.cur.children[index]
            path = self.manager.getCurChildPath(index)
            if node.type == FILE:
                self.child = AttributeForm(node, path)
            else:
                self.child = AttributeForm(node, path)
            self.child.show()

    # 右键菜单
    def show_menu(self, point):
        # 右键菜单
        menu = QMenu(self.list_view)
        if len(self.list_view.selectedItems()) != 0:  # 右击选中文件
            # 菜单项
            open_file_action = QAction(QIcon(), '打开')
            open_file_action.triggered.connect(self.openFile)
            menu.addAction(open_file_action)

            delete_action = QAction(QIcon(), '删除')
            delete_action.triggered.connect(self.deleteFile)
            menu.addAction(delete_action)

            rename_action = QAction(QIcon(), '重命名')
            rename_action.triggered.connect(self.rename)
            menu.addAction(rename_action)

            view_attribute_action = QAction(QIcon('img/attribute.png'), '属性')
            view_attribute_action.triggered.connect(self.viewAttribute)
            menu.addAction(view_attribute_action)
            # 在右键位置显示菜单
            dest_point = self.list_view.mapToGlobal(point)
            menu.exec_(dest_point)

        else:  # 右击空白位置
            # 右键菜单的二级菜单:新建
            create_menu = QMenu(menu)
            create_menu.setTitle('新建')

            # 新建文件夹
            create_folder_action = QAction(QIcon('img/folder.png'), '文件夹')
            create_folder_action.triggered.connect(self.createFolder)
            create_menu.addAction(create_folder_action)

            # 新建文件
            create_file_action = QAction(QIcon('img/file.png'), '文件')
            create_file_action.triggered.connect(self.createFile)
            create_menu.addAction(create_file_action)

            create_menu.setIcon(QIcon('img/create.png'))
            menu.addMenu(create_menu)
            # 属性选项
            view_attribute_action = QAction(QIcon('img/attribute.png'), '属性')
            view_attribute_action.triggered.connect(self.viewAttribute)
            menu.addAction(view_attribute_action)
            # 在右键位置显示菜单
            dest_point = self.list_view.mapToGlobal(point)
            menu.exec_(dest_point)

    # 格式化事件
    def format(self):
        # 结束编辑
        self.list_view.closeEdit()
        # 提示框
        reply = QMessageBox()
        reply.setWindowTitle('警告')
        reply.setText('确定要格式化磁盘吗？此操作将清空所有数据')
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button_yes = reply.button(QMessageBox.Yes)
        button_yes.setText('确定')
        button_no = reply.button(QMessageBox.No)
        button_no.setText('取消')
        reply.exec_()
        reply.show()

        if reply.clickedButton() == button_no:
            return
        self.manager.format()  # 格式化文件系统
        # 重启界面
        self.hide()
        self.new_form = MainWindow()
        self.new_form.show()

    # 返回上一级事件
    def backEvent(self):
        # 关闭编辑
        self.list_view.closeEdit()
        if self.manager.cur == self.manager.root:
            return False
        # 返回父节点
        self.manager.backParent()
        # 更新界面
        self.loadCurFile()
        self.list_view.cur_node = self.manager.cur
        self.update_bottom_label()
        # 返回到根目录则禁用返回事件
        if self.manager.cur == self.manager.root:
            self.backAction.setEnabled(False)
        return True

    # 写文件事件
    def writeEvent(self, data):
        self.manager.writeFile(self.file_be_writen, data)

    # 关闭文件系统事件
    def closeEvent(self, event):
        # 结束编辑
        self.list_view.closeEdit()
        self.manager.saveFileSystem()
        event.accept()
