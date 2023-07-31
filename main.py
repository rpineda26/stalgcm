from PyQt5.QtWidgets import QApplication
import sys
from view import *

"""
Author : Ralph Dawson G. Pineda
Section : STALGCM S13
Date : July 2023
Model of computation: 2-Way Deterministic Finite Automata

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    machine = Machine()
    machine.showMaximized()
    sys.exit(app.exec_())