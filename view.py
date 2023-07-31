"""
Author: Ralph Dawson G. Pineda
Section: STALGCM S13
Date: July 2023
Description: This file contains the view of the program. Make sure that the dependencies are installed in your device. Read the README.md for more information.
"""
from PyQt5.QtWidgets import QMessageBox, QLabel, QFileDialog, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QInputDialog
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt

from controller import *
from model import *

"""
@definition: This class is the view representation of a state in the machine. It is color coded to determine which type of state it is.
@param: color - the color of the state: yellow for start, green for accept, red for reject, and white for normal

"""
class State(QWidget):
    """
    @definition: This is the constructor of the State class
    @param: color - the color of the state: yellow for start, green for accept, red for reject, and white for normal
    """
    def __init__(self, color, parent=None):
        super().__init__(parent=parent)
        self.color= color
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 10))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    """
    @definition: This function paints the state with the color specified in the constructor
    @param: event - the event that triggers the paintEvent
    """
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawEllipse(self.rect())
    """
    @definition: This function sets the name of the state. It can reference the state it represents through its name.
    @param: text - the name of the state
    """
    def set_text(self, text):
        self.label.setText(text)
    """
    @definition: This function resizes the state to fit the window
    @param: event - the event that triggers the resizeEvent
    """
    def resizeEvent(self, event):
        self.label.setGeometry(self.rect())

        label_width = self.label.width()
        label_height = self.label.height()
        square_width = self.width()
        square_height = self.height()

        x = (square_width - label_width) / 2
        y = (square_height - label_height) / 2

        self.label.setGeometry(int(x), int(y), label_width, label_height)

"""
@definition : This class is the view representation of the entire machine. The flow of user input is: (open text file -> (input word -> start -> step *)*)*) where * means repetition
@attributes: machine - the DFA that is being represented by the view
            word - the word that is being inputted by the user
            curr_state - the current state of the machine
            head - the current character in the world that is being processed
            direction - the reading direction for the next input
            accepted - the boolean value that determines if the machine has accepted the word
            prev_state - the previous state of the machine
"""

class Machine(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('2-Way Deterministic Finite Automata')
        self.setFixedWidth(720)
        self.setFixedHeight(720)
        self.fileName = None

        self.machine = None
        self.size = None


        hbox = QHBoxLayout()
        self.openTextFileButton = QPushButton('Open Text File')
        self.startButton = QPushButton('Start')
        self.stepButton = QPushButton('Step')
        self.inputWordButton = QPushButton('Input Word')

        hbox.addWidget(self.openTextFileButton)
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.stepButton)
        hbox.addWidget(self.inputWordButton)

        self.openTextFileButton.clicked.connect(self.openFileNameDialog)
        self.startButton.clicked.connect(self.startFind)
        self.stepButton.clicked.connect(self.stepFind)
        self.inputWordButton.clicked.connect(self.setInput)

        self.inputWordButton.setEnabled(False)
        self.stepButton.setEnabled(False)
        self.startButton.setEnabled(False)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.vbox.setAlignment(Qt.AlignTop)
        self.setLayout(self.vbox)

        size = min(self.width(), self.height()) - 50
        for state in self.findChildren(State):
            state.setMinimumSize(size // self.size, size // self.size)


        self.curr_state_label = None
        self.head_label = None
        self.word_label = None
        self.transition_label =None
        self.direction_label = None
     
    """
    @definition: This function makes the states size dynamic depending on the window size
    @param: event - the event that triggers the resizeEvent
    """
    def resizeEvent(self, event):

        size = min(self.width(), self.height()) - 50

        for state in self.findChildren(State):
            state.setMinimumSize(size // self.size, size // self.size)

        self.update()
    """
    @definition: This function creates a grid to hold views the states of the machine
    """
    def createGrid(self):
        """
        Create a grid of squares for the maze
        """
        grid = QGridLayout()
        grid.setSpacing(2)

        self.inputWordButton.setEnabled(True)
        counter = 0
        for i in range (self.size):
            for j in range(self.size):
                if counter < len(self.machine.getQ()):
                    if self.machine.getQ()[counter] == self.machine.getStart():
                        state = State('yellow', self)
                    elif self.machine.getQ()[counter]== self.machine.getAccept():
                        state = State('green', self)
                    elif self.machine.getQ()[counter]== self.machine.getReject():
                        state = State('red', self)
                    else:
                        state = State('white', self)
                    state.set_text(self.machine.getQ()[counter])
                    state.setObjectName(f'state{self.machine.getQ()[counter]}')
                    grid.addWidget(state, i, j)
                counter += 1

        self.vbox.addLayout(grid)
        self.createStatusBar()

    def createStatusBar(self):

        self.head_label = QLabel("Head: 0 Character: -")
        self.word_label = QLabel("Word: ")
        self.transition_label = QLabel("Transition: ")
        self.direction_label = QLabel("Read Direction: right")
        self.curr_state_label = QLabel("Current State: " + self.machine.getCurrState())
        self.direction_label = QLabel("Direction: " + self.machine.getDirection())
        statusBox = QHBoxLayout()
        statusBox.addWidget(self.curr_state_label)
        statusBox.addWidget(self.head_label)
        statusBox.addWidget(self.word_label)
        statusBox.addWidget(self.transition_label)
        statusBox.addWidget(self.direction_label)
        
        self.vbox.addLayout(statusBox)

    """
    @definition: This function resets the attributes of the object instance of this 
                    class to read a new machine definition file
    """
    def resetMachine(self):
        self.machine = None
        self.size = None
        # Remove the old grid and status box
        if self.vbox.count() > 1:
            print(self.vbox.itemAt(2))
            self.vbox.layout().removeItem(self.vbox.itemAt(2))
            self.vbox.layout().removeItem(self.vbox.itemAt(1))
            self.curr_state_label.setParent(None)
            self.head_label.setParent(None)
            self.word_label.setParent(None)
            self.transition_label.setParent(None)
            self.direction_label.setParent(None)
        self.stepButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.update()
    """
    @definition: This function reads the machine definition file and creates a DFA object
                  Through this same function, the file is read and validated for errors.
                  In case of no errors, an object of the 2DFA is instantiated and its states
                  will be represented in a grid.    
    """
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
            code, machine = initializeMachine(Q, sigma, delta, start, accept, reject)
            flag_create_machine = self.validateMachineDefinition(code)
            if flag_create_machine:
                self.machine = machine
                self.size = determineGridSize(len(Q))
                self.createGrid()

    """
    @definition: This function validates the machine definition file for errors
    @param: code - determines the status of the machine definition file. If it is invalid
                    then the code will determine which type of error was committed
    @return - flag_create_machine - determines if the machine definition file is valid
    """
    def validateMachineDefinition(self, code):
        flag_create_machine = False
        if code == 0:
            self.inputWordButton.setEnabled(True)
            flag_create_machine = True
        else:
            if code ==1:
                err = "Invalid transition function"
            elif code ==2:
                err = "Machine is not deterministic"
            self.showNoGoalMessage(err)
            self.startButton.setEnabled(False)
            self.stepButton.setEnabled(False)
            self.inputWordButton.setEnabled(False)
        return flag_create_machine
    """
    @definition: This opens a display for getting the user input on which word is to be checked"""
    def setInput(self):
         name, done1 = QInputDialog.getText(self, 'Input Word', 'Enter a word:')
         if done1:
            self.machine.setWord(attachEndMarker(name))
         self.startButton.setEnabled(True)
    """
    @definition: This function is called when the user clicks the start button. It will
                    initialize the values needed to start tracing the transition of states
    """
    def startFind(self):
        """
        Start the path finding algorithm
        """
        self.openTextFileButton.setEnabled(False)
        self.inputWordButton.setEnabled(True)
        self.startButton.setEnabled(False)
        self.stepButton.setEnabled(True)
        self.inputWordButton.setEnabled(False)

        self.head_label.setText("Head: " + str(self.machine.getHead())+" Character: " + self.machine.getWord()[self.machine.getHead()])
        if len(self.machine.getWord()) ==0:
            self.word_label.setText("Word: ")
        else:
            self.word_label.setText("Word: " + self.machine.getWord()[:self.machine.getHead()]+"   " +self.machine.getWord()[self.machine.getHead()]+"   " +self.machine.getWord()[self.machine.getHead()+1:])
        

        
        #show current state
    """
    @definition: This function is called when the user clicks the step button. It will follow the appropriate transition depending
                 on the current state and the input character being read at the moment
    """
    def stepFind(self):
        
        """
        Step through the node traversal
        """
        
        if validateSymbol(self.machine.getWord()[self.machine.getHead()], self.machine.getSigma()):
            self.machine.setPrevState(self.machine.getCurrState())
            self.resetColor()
            curr_state, direction, transition_used = nextStep(self.machine.getDelta(), self.machine.getCurrState(), self.machine.getWord()[self.machine.getHead()])
            self.machine.setCurrState(curr_state)
            self.machine.setDirection(direction)
            self.showCurrentState(transition_used)
        else: #display error symbol does not exist in sigma
            self.showNoGoalMessage("Symbol "+self.machine.getWord()[self.getHead()]+" does not exist in sigma")
        if self.machine.getDirection() =="left":
            self.machine.setLeftHead()
        else:
            self.machine.setRightHead()

        if isEnd(self.machine.getCurrState(), self.machine.getAccept(), self.machine.getReject(), self.machine.getWord()[self.machine.getHead()]):
            if isAccepted(self.machine.getCurrState(), self.machine.getAccept()):
                self.machine.setAccepted(True)
                #show accept message
            else:
                #show reject message
                self.machine.setAccepted(False)
            self.showEndMessage(self.machine.getAccepted())
    """
    @definition: This function updates the views of the status of the machine. it displays the current state, the head, 
                    the word, the direction, and the transition used
    """
    def showCurrentState(self, transition_used):
        self.curr_state_label.setText("Current State: " + self.machine.getCurrState())
        self.head_label.setText("Head: " + str(self.machine.getHead()) + " Character: "+self.machine.getWord()[self.machine.getHead()])
        if len(self.machine.getWord()) ==0:
            self.word_label.setText("Word: ")
        else:
            self.word_label.setText("Word: " + self.machine.getWord()[:self.machine.getHead()]+"   "+ self.machine.getWord()[self.machine.getHead()]+ "   " +self.machine.getWord()[self.machine.getHead()+1:])
        self.direction_label.setText("Direction: " + self.machine.getDirection())
        self.transition_label.setText("Transition: " + ' '.join(map(str,transition_used)))
        self.direction_label.setText("Direction: " + self.machine.getDirection())
        state =self.findChild(State, f'state{self.machine.getCurrState()}')
        state.color = "blue"
        state.update()

    """

    @definition: This function resets the color of the state that 
                    was colored to be the current state

    """
    def resetColor(self):
        state = self.findChild(State, f'state{self.machine.getPrevState()}')
        if self.machine.getPrevState() == self.machine.getStart():
            state.color = "yellow"
        elif self.machine.getPrevState() == self.machine.getAccept():
            state.color = "green"
        elif self.machine.getPrevState() == self.machine.getReject():
            state.color = "red"
        else:
            state.color = "white"
        state.update()
        state.update()
    """
    @definition: This function resets the word, the head, the current state, and the previous state to their initial values
                This is called when the user wants to check another word
    """
    def resetWord(self):
        for q in self.machine.getQ():
            state = self.findChild(State, f'state{q}')
            if q == self.machine.getStart():
                state.color = "yellow"
            elif q == self.machine.getAccept():
                state.color = "green"
            elif q == self.machine.getReject():
                state.color = "red"
            else:
                state.color = "white"
            state.update()
            self.machine.resetState()
            self.startButton.setEnabled(False)
            self.stepButton.setEnabled(False)
            self.inputWordButton.setEnabled(True)
            self.openTextFileButton.setEnabled(True)
    """
    @definition: This function shows the message when the machine terminates. 
                 It will display whether the word was accepted or rejected
    """
    def showEndMessage(self, accept):
        message = QMessageBox()
        title = ""
        msg = ""
        message.setIcon(QMessageBox.Information)
        if accept:
            title = "Accepted"
            msg = f'The word {self.machine.getWord()} has been accepted by the provided machine!'
        else:
            title = "Rejected"
            msg = f'The word {self.machine.getWord()} has been rejected by the provided machine!'
        message.setWindowTitle(title)
        message.setText(msg)
        message.setStandardButtons(QMessageBox.Ok)

        message.exec_()
        self.resetWord()
    """
    @definition: This function shows the message when the machine can't be instantiated because
                the machine definition did not follow all restrictions. It will display the error
                depenging on whatever caused it.
    """
    def showNoGoalMessage(self, err):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Invalid Machine!")
        message.setText(err)
        message.setStandardButtons(QMessageBox.Ok)

        message.exec_()