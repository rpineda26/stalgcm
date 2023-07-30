from PyQt5.QtWidgets import QApplication
import sys
from view import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    machine = Machine()
    machine.showMaximized()
    sys.exit(app.exec_())