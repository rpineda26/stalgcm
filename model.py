class Machine_2DFA:
    def __init__(self, Q, sigma, delta, start, accept, reject):
        self.Q = None
        self.sigma = None
        self.delta = None
        self.start = None
        self.accept = None
        self.reject = None
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
    def resetMachine(self):
        self.Q = None
        self.sigma = None
        self.delta = None
        self.start = None
        self.accept = None
        self.reject = None