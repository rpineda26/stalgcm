
class Machine_2DFA:
    def __init__(self, Q, sigma, delta, start, accept, reject):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.start = start
        self.accept =  accept
        self.reject = reject

        self.word= None
        self.curr_state = start
        self.head = 0
        self.direction = "right"
        self.accepted = False
        self.prev_state = start

    """
    getters for the DFA
    """
    def getQ(self):
        return self.Q
    def getSigma(self):
        return self.sigma
    def getDelta(self):
        return self.delta
    def getStart(self):
        return self.start
    def getAccept(self):
        return self.accept
    def getReject(self):
        return self.reject
    def getWord(self):
        return self.word
    def getCurrState(self):
        return self.curr_state
    def getHead(self):
        return self.head
    def getDirection(self):
        return self.direction
    def getAccepted(self):
        return self.accepted
    def getPrevState(self):
        return self.prev_state
  
    """
    setters for the DFA
    """
    def setQ(self, Q):
        self.Q = Q
    def setSigma(self, sigma):
        self.sigma = sigma
    def setDelta(self, delta):
        self.delta = delta
    def setStart(self, start):
        self.start = start
    def setAccept(self, accept):
        self.accept = accept
    def setReject(self, reject):
        self.reject = reject
    def setWord(self, word):
        self.word = word
    def setCurrState(self, curr_state):
        self.curr_state = curr_state
    def setRightHead(self):
        self.head = self.head + 1
    def setLeftHead(self):
        self.head = self.head - 1
    def setDirection(self, direction):
        self.direction = direction
    def setAccepted(self, accepted):
        self.accepted = accepted
    def setPrevState(self, prev_state):
        self.prev_state = prev_state
    def resetMachine(self):
        self.Q = None
        self.sigma = None
        self.delta = None
        self.start = None
        self.accept = None
        self.reject = None
        self.word= None
        self.curr_state = None
        self.head = 0
        self.direction ="right"
        self.accepted = False
        self.prev_state = None
        
    def resetState(self):
        self.word = None
        self.curr_state = self.start
        self.head = 0
        self.direction = "right"
        self.accepted = False
        self.prev_state = self.curr_state