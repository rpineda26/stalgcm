import sys
import queue
import threading
from PyQt5.QtWidgets import QMessageBox, QApplication, QLabel, QSlider, QFileDialog, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QTimer

from controller import *
from model import *

class MazeBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Maze Bot')
        self.setFixedWidth(720)
        self.setFixedHeight(720)

        self.size = None
        self.fileName = None
        self.txtMaze = None
        self.distances = None
        self.path_list = None
        self.start, self.goal = None, None
        self.traverseSpeed = 100

        hbox = QHBoxLayout()
        self.openTextFileButton = QPushButton('Open Text File')
        self.startButton = QPushButton('Start')
        self.stepButton = QPushButton('Step')

        self.slider_label = QLabel("Traverse Speed")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(3000)
        self.slider.setValue(3000)

        hbox.addWidget(self.openTextFileButton)
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.stepButton)
        hbox.addWidget(self.slider_label)
        hbox.addWidget(self.slider)

        self.openTextFileButton.clicked.connect(self.openFileNameDialog)
        self.startButton.clicked.connect(self.startFind)
        self.stepButton.clicked.connect(self.stepFind)
        self.slider.valueChanged.connect(self.changeTraverseSpeed)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.vbox.setAlignment(Qt.AlignTop)
        self.setLayout(self.vbox)

        size = min(self.width(), self.height()) - 50
        for square in self.findChildren(Square):
            square.setMinimumSize(size // self.size, size // self.size)

    def resizeEvent(self, event):
        """
        Makes the squares responsive to the size of the window
        """
        size = min(self.width(), self.height()) - 50

        for square in self.findChildren(Square):
            square.setMinimumSize(size // self.size, size // self.size)

        self.update()

    def createGrid(self):
        """
        Create a grid of squares for the maze
        """
        grid = QGridLayout()
        grid.setSpacing(0)

        for i in range(self.size):
            for j in range(self.size):
                square = None
                if self.distances[i][j] == -2:
                    square = Square('black', self)
                elif self.goal[0] == i and self.goal[1] == j:
                    square = Square('red', self)
                elif self.start[0] == i and self.start[1] == j:
                    square = Square('green', self)
                else:
                    square = Square('white', self)

                square.setObjectName(f'square{i * self.size + j}')
                grid.addWidget(square, i, j)

        self.vbox.addLayout(grid)

    def update_colors(self):
        """
        Timer function to update the colors of the optimal path
        """
        self.color_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_square_color)
        self.timer.start(self.traverseSpeed)

    def update_square_color(self):
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

    def addDistancesText(self):
        """
        Add the distances of each square from the goal
        """
        for i in range(self.size):
            for j in range(self.size):
                square = self.findChild(Square, f'square{i * self.size + j}')
                square.set_text(str(self.distances[i][j]))

    def resetMaze(self):
        """
        Reset the maze
        """
        self.distances = None
        self.path_list = None
        self.fileName = None
        self.txtMaze = None
        self.start, self.goal = None, None
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
            self.resetMaze()

            # Read the new maze and set variables
            self.size, self.txtMaze = read_maze(fileName)
            self.start, self.goal, self.distances = start_goal_distances(
                self.txtMaze)
            self.distances = flood_fill(
                self.txtMaze, self.goal, self.distances)

            self.createGrid()
            self.addDistancesText()

            # Check if goal is reachable
            if self.distances[self.start[0]][self.start[1]] == -1:
                self.showNoGoalMessage()
                self.startButton.setEnabled(False)
                self.stepButton.setEnabled(False)
                self.slider.setEnabled(False)
                return
            else:
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

    def showNoGoalMessage(self):
        message = QMessageBox()

        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Goal cannot be reached!")
        message.setText(
            "The goal cannot be reached in this maze! Reset the maze by selecting a new text file.")
        message.setStandardButtons(QMessageBox.Ok)

        message.exec_()
