import sys
from PyQt5 import QtWidgets
from ui.main_window import SortingHatApp

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SortingHatApp()
    window.show()
    sys.exit(app.exec_())
