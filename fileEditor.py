import PyQt5.QtCore
from PyQt5.Qt import QWidget, QIcon, QTextEdit, QHBoxLayout, QVBoxLayout, QMessageBox


# 文本编辑器
class EditForm(QWidget):
    _signal = PyQt5.QtCore.pyqtSignal(str)

    def __init__(self, name, data):
        super().__init__()
        # 编辑器外观设置
        self.resize(480, 480)
        self.setMinimumSize(320, 320)
        self.setWindowTitle(name)
        self.name = name
        self.setWindowIcon(QIcon('img/file.png'))

        # qt文本编辑器
        self.file_editor = QTextEdit(self)  # 文本编辑器
        self.file_editor.setText(data)  # 初始文本
        self.file_editor.setPlaceholderText("在此输入文件内容")  # 设置占位字符串
        # 保存初始数据
        self.original_data = data
        # 布局
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.file_editor)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)

    # 关闭文本编辑器
    def closeEvent(self, event):
        # 如果没有对文本做出修改
        if self.original_data == self.file_editor.toPlainText():
            # 直接退出
            event.accept()
            return

        # 提示信息
        reply_info = QMessageBox()
        reply_info.setWindowTitle('提醒')
        reply_info.setText('是否保存修改?')
        reply_info.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Ignore)
        button_save = reply_info.button(QMessageBox.Yes)
        button_save.setText('保存')
        button_not_save = reply_info.button(QMessageBox.No)
        button_not_save.setText('不保存')
        button_cancel = reply_info.button(QMessageBox.Ignore)
        button_cancel.setText('取消')
        reply_info.exec_()

        if reply_info.clickedButton() == button_cancel:  # 取消则忽略事件
            event.ignore()
        elif reply_info.clickedButton() == button_save:  # 保存则返回新数据
            self._signal.emit(self.file_editor.toPlainText())
            event.accept()  # 退出
        else:
            event.accept()  # 退出

