class Machine_2DFA:
    def __init__(self, Q, sigma, delta, start, accept, reject):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.start = start
        self.accept = accept
        self.reject = reject
        self.machine_definition_file = None
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
    def setMachineDefinitionFile(self, machine_definition_file):
        self.machine_definition_file = machine_definition_file