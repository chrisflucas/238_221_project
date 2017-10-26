#import util, math, random
#from collections import defaultdict
from datetime import date, datetime
import data


class Oracle:

	def __init__(self, start_state, initial_investment, stock_price_dict):
        self.filepath = '/Users/harper/Desktop/Fall 2017/Bitcoin Project/238_221_project'
		self.actions = ["Buy", "Sell", "Hold"]
		self.start = start_state #datetime object
		self.total_reward = 0
		self.investment = initial_investment
		self.stock_prices = stock_price_dict
        self.data = DataUtil().read_file(filepath)

	def startState(self):
        return self.start


    def getAction(self, state, first_day, last_day): #first_day = min(d, key=d.get), last_day = max(d, key=d.get)
    	if state == first_day: return "Buy"
    	elif state == last_day: return "Sell"
    	else: return "Hold"


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

