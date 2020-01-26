import os
import sys
from MR.Kernel import Loading, Error
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from Configure_Windows.Window import MainWindow as mw


class FunctionMainWindow(mw.Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(FunctionMainWindow, self).__init__(parent)
        self.setupUi(self)

        # 声明变量
        self.is_saved = True

        # region 如果配置文件存在则读取，不存在则创建配置文件
        if not os.path.exists("mrdb.conf"):
            # 配置文件不存在
            QMessageBox.information(None, "Warning", "Configuration file not found.\n"
                    "We are going to create a new one using default values.")
            Loading.init_config()
        # endregion

        # region 读取配置文件
        try:
            # 尝试读取配置文件
            self.config = Loading.read_config()
        except Error.ConfigFileBroken:
            # 读取出错，配置文件遭到破坏
            QMessageBox.warning(None, "Warning", "Configuration file is broken."
                                                 "Please delete it anyway.")
            sys.exit(0)
        # endregion

        # 根据配置文件填充默认值
        running_mode_index = {"PlasticMemories": 0,
                              "SingleFile": 1,
                              "MultiFile": 2}
        self.Label_Address_Value.setText(self.config["Address"])
        self.SpinBox_Port_Value.setValue(self.config["Port"])
        self.ComboBox_RunningMode_Value.setCurrentIndex(running_mode_index[self.config["RunningMode"]])

    def PushButton_Exit_Clicked(self):
        # 退出按钮
        if self.is_saved:
            # 已经保存，直接退出
            sys.exit(0)
        else:
            # 未保存，询问是否退出前先保存
            reply = QMessageBox.question(None, "Information", "Leave without saving ?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                # 不保存就退出
                sys.exit(0)
            elif reply == QMessageBox.No:
                # 保存并退出
                Loading.save_config(self.config)
                QMessageBox.information(None, "Information", "Configuration file saved successfully !")
                sys.exit(0)
            elif reply == QMessageBox.Cancel:
                # 取消按钮，啥事不干
                pass

    def PushButton_Save_Clicked(self):
        # 保存按钮
        Loading.save_config(self.config)
        QMessageBox.information(None, "Information", "Configuration file saved successfully !")
        self.PushButton_Save.setEnabled(False)
        self.is_saved = True

    # region 值变动的一系列事件
    def Label_Address_Value_TextChanged(self):
        # 地址变动
        self.config["Address"] = self.Label_Address_Value.text()
        self.PushButton_Save.setEnabled(True)
        self.is_saved = False

    def SpinBox_Port_Value_ValueChanged(self):
        # 端口变动，同上
        self.config["Port"] = self.SpinBox_Port_Value.value()
        self.PushButton_Save.setEnabled(True)
        self.is_saved = False

    def ComboBox_RunningMode_Value_CurrentIndexChanged(self):
        # 运行模式变动，同上
        self.config["RunningMode"] = self.ComboBox_RunningMode_Value.currentText()
        self.PushButton_Save.setEnabled(True)
        self.is_saved = False
    # endregion
