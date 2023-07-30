from view import*

from model import*
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    view_Machine = Machine()
    view_Machine.show()
    model = Machine_2DFA()
    controller = Controller(view_Machine, model)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
