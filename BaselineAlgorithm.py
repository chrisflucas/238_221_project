import random
from datetime import date, datetime
import data

#import util, math
#from collections import defaultdict


class BaselineAlgorithm:

    def __init__(self, start_state, initial_investment, stock_price_dict):
        self.filepath = '/Users/harper/Desktop/Fall 2017/Bitcoin Project/238_221_project/bitcoin_dataset.csv'
		self.actions = ["Buy", "Sell", "Hold"]
		self.start = start_state #date object
		self.total_reward = 0
		self.investment = initial_investment
		self.stock_prices = stock_price_dict
        self.data = DataUtil().read_file(filepath)


	def startState(self):
        return self.start


    def getAction(state):
    	return random.choice(self.actions)


    def succAndProbReward(self, state, action):
        stock_price = self.stock_prices(state)
        newState = state + datetime.timedelta(days=1)
        prob, reward = 1, 0 #stays at 0 if action == "Hold"

        if action == "Buy":
        	self.investment -= stock_price
        	self.total_reward -= stock_price
        	reward = stock_price * -1

        elif action == "Sell":
        	self.investment += stock_price
        	self.total_reward += stock_price
        	reward = stock_price

		return (newState, prob, reward)


	def getReward(self):
		return self.total_reward


	def investmentRemaining(self):
		return self.investment
