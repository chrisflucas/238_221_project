import util, math, random
from collections import defaultdict


Class BaselineAlgorithm():

    def __init__(self):
		self.actions = ["Buy", "Sell", "Hold"]

    def getAction(self, state):
        return random.choice(self.actions)





