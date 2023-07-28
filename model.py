class Machine_2DFA:
    def __init__(self, Q, sigma, delta, start, accept, reject):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.start = start
        self.accept = accept
        self.reject = reject