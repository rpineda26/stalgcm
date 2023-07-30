import sys
import queue
import threading
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QSlider, QFileDialog, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QTimer

from controller import *
from model import *
class State(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(paren=parent)
        self.color= color
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 10))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawRect(self.rect())
    def set_text(self, text):
        self.label.setText(text)
    def resizeEvent(self, event):
        self.label.setGeometry(self.rect())

        label_width = self.label.width()
        label_height = self.label.height()
        square_width = self.width()
        square_height = self.height()

        x = (square_width - label_width) / 2
        y = (square_height - label_height) / 2

        self.label.setGeometry(int(x), int(y), label_width, label_height)

class Machine(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('2-Way Deterministic Finite Automata')
        self.setFixedWidth(720)
        self.setFixedHeight(720)
        self.size = None
        self.fileName = None
        self.machine = None
        self.traverseSpeed = 100
        self.machine = None

        hbox = QHBoxLayout()
        self.openTextFileButton = QPushButton('Open Text File')
        self.startButton = QPushButton('Start')
        self.stepButton = QPushButton('Step')

        self.slider_label = QLabel("Traverse Speed")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(3000)
        self.slider.setValue(3000)
        self.string_input = QLineEdit()

        hbox.addWidget(self.openTextFileButton)
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.stepButton)
        hbox.addWidget(self.slider_label)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.string_input)

        self.openTextFileButton.clicked.connect(self.openFileNameDialog)
        self.startButton.clicked.connect(self.quickStep)
        self.stepButton.clicked.connect(self.nextStep)
        self.slider.valueChanged.connect(self.changeTraverseSpeed)
        self.string_input.connect(self.setInput)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.vbox.setAlignment(Qt.AlignTop)
        self.setLayout(self.vbox)

        size = min(self.width(), self.height()) - 50
        for state in self.findChildren(State):
            state.setMinimumSize(size // self.size, size // self.size)

    def resizeEvent(self, event):
        """
        Makes the squares responsive to the size of the window
        """
        size = min(self.width(), self.height()) - 50

        for state in self.findChildren(State):
            state.setMinimumSize(size // self.size, size // self.size)

        self.update()

    def createGrid(self):
        """
        Create a grid of squares for the maze
        """
        grid = QGridLayout()
        grid.setSpacing(2)


        for i in range(self.machine.getQ()):
            if i == self.machine.getStart():
                state = State('yellow', self)
            elif i== self.machine.getAccept():
                state = State('green', self)
            elif i== self.machine.getReject():
                state = State('red', self)
            else:
                state = State('white', self)
            state.set_text(i)
            state.setObjectName(f'state{i}')
            grid.addWidget(state, i)

        self.vbox.addLayout(grid)

    def update_colors(self):
        """
        Timer function to update the colors of the optimal path
        """
        self.color_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state_color)
        self.timer.start(self.traverseSpeed)

    def update_state_color(self):
        """
        Update the colors of the optimal path
        """
        if self.color_index >= len(self.path_list):
            self.timer.stop()
            self.openTextFileButton.setEnabled(True)
            self.showGoalMessage()
            return

        coord = self.path_list[self.color_index]
        i, j = coord

        if self.goal[0] == i and self.goal[1] == j:
            pass
        elif self.start[0] == i and self.start[1] == j:
            pass
        else:
            square = self.findChild(Square, f'square{i * self.size + j}')
            square.color = 'yellow'
            square.update()

        self.color_index += 1

    def resetMachine(self):
        """
        Reset the maze
        """
        self.machine = None
        self.slider.setValue(3000)

        # Remove the old grid
        if self.vbox.count() > 1:
            self.vbox.layout().removeItem(self.vbox.itemAt(1))

    def openFileNameDialog(self):
        """
        Opens a file dialog to select a text file
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Text Files(*.txt)",
                                                  options=options)
        if fileName:
            # Reset the maze
            self.resetMachine()
            Q, sigma, start,  accept, reject, delta =  readMachine(fileName)
            code, machine = initializeMachine(Q, sigma, start, accept, reject, delta)
            flag_create_machine = self.validateMachineDefinition(code)
            if flag_create_machine:
                self.machine = machine


    def validateMachineDefinition(self, code):
        flag_create_machine = False
        if code == 0:
            self.string_input.setEnabled(True)
            self.createGrid()
            flag_create_machine = True
        else:
            if code ==1:
                err = "Invalid transition function"
            elif code ==2:
                err = "Machine is not deterministic"
            self.showNoGoalMessage(err)
            self.startButton.setEnabled(False)
            self.stepButton.setEnabled(False)
            self.slider.setEnabled(False)
            self.string_input.setEnabled(False)
        return flag_create_machine

    def setInput(self):
         self.startButton.setEnabled(True)
         self.stepButton.setEnabled(True)
         self.slider.setEnabled(True)
    def startFind(self):
        """
        Start the path finding algorithm
        """
        self.openTextFileButton.setEnabled(False)
        self.path_list = find_path(self.distances, self.start, self.goal)
        self.update_colors()

    def changeTraverseSpeed(self, value):
        """
        Changes the speed of the node traversal (slowest speed is 3000ms)

        Input: 
        - value - the value of the slider
        """
        self.traverseSpeed = 3000 - value

    def stepFind(self):
        if self.path_list is None:
            self.path_list = find_path(self.distances, self.start, self.goal)

        """
        Step through the node traversal
        """
        if len(self.path_list) > 0:
            coord = self.path_list.pop(0)
            i, j = coord

            if self.goal[0] == i and self.goal[1] == j:
                pass
            elif self.start[0] == i and self.start[1] == j:
                pass
            else:
                square = self.findChild(Square, f'square{i * self.size + j}')
                square.color = 'yellow'
                square.update()

        else:
            self.showGoalMessage()

    def showGoalMessage(self):
        message = QMessageBox()

        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Goal Reached!")
        message.setText(
            "Goal has been reached! Reset the maze by selecting a new text file.")
        message.setStandardButtons(QMessageBox.Ok)

        message.exec_()

    def showNoGoalMessage(self, err):
        message = QMessageBox()

        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Invalid Machine!")
        message.setText(err)
        message.setStandardButtons(QMessageBox.Ok)

        message.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    machine = Machine()
    machine.showMaximized()
    sys.exit(app.exec_())