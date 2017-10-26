#import util, math, random
#from collections import defaultdict
from datetime import date, datetime, timedelta
import data


class Oracle:

	def __init__(self, first_day, last_day, initial_investment, stock_price_dict):
		self.actions = ["Buy", "Sell", "Hold"]
		self.states = set()
		self.first_day = first_day #datetime object
		self.last_day = last_day
		self.total_reward = 0
		self.investment = initial_investment
		self.stock_prices = stock_price_dict
		self.num_coins = 0

	def startState(self):
		return self.first_day

	def getAction(self, state): #first_day = min(d, key=d.get), last_day = max(d, key=d.get)
		if state == self.first_day: return "Buy"
		elif state == self.last_day: return "Sell"
		else: return "Hold"


	def succAndProbReward(self, state, action):
		stock_price = self.stock_prices[state]['btc_market_price']
		newState = state + timedelta(days=1)
		prob, reward = 1, 0 #stays at 0 if action == "Hold"

		if action == "Buy":
			while self.investment > stock_price:
				self.investment -= stock_price
				self.num_coins += 1
				self.total_reward -= stock_price
				reward = stock_price * -1
			print self.total_reward

		elif action == "Sell":
			print self.num_coins
			self.investment += stock_price * self.num_coins
			self.total_reward += stock_price * self.num_coins
			reward = stock_price * self.num_coins
			newState = None

		return newState, prob, reward

	def computeStates(self):
		cur_state = self.startState()
		self.states.add(self.startState())
		while cur_state:
			action = self.getAction(cur_state)
			newState, prob, reward = self.succAndProbReward(cur_state, action)
			if newState:
				self.states.add(newState)
				cur_state = newState
			else:
				cur_state = None

		#print "%d states" % len(self.states)
		#print self.states

	def getReward(self):
		return self.total_reward

	def investmentRemaining(self):
		return self.investment


if __name__ == '__main__':
	filepath = '/Users/harper/Desktop/Fall 2017/Bitcoin Project/238_221_project/bitcoin_dataset.csv'
	investment = 1000000
	dt = data.DataUtil()
	d = dt.read_file(filepath)
	first_day = min(d, key=lambda k: d[k])
	last_day = max(d, key=lambda k: d[k])
	print first_day, last_day
	#first_day = min(d, key=d.get)
	#last_day = max(d, key=d.get)
	oracle = Oracle(first_day, last_day, investment, d)
	oracle.computeStates()
	print oracle.getReward()

