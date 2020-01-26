import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from Configure_Windows.Function import MainWindow as mw


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mw.FunctionMainWindow()

    # region 自定义设置
    # 禁止调整窗口大小
    window.setFixedSize(window.width(), window.height())

    # 禁止右上角退出按钮
    window.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

    # 使居中窗体
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    window.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
    # endregion

    window.show()
    sys.exit(app.exec_())
