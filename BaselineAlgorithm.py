import random
from datetime import date, datetime, timedelta
import data, csv 

#import util, math
#from collections import defaultdict


class BaselineAlgorithm:

	def __init__(self, start_state, initial_investment, stock_price_dict):
		self.filepath = '/Users/harper/Desktop/Fall 2017/Bitcoin Project/238_221_project/bitcoin_dataset.csv'
		self.states = set()
		self.actions = ["Buy", "Sell", "Hold"]
		self.start = start_state #date object
		self.total_reward = 0
		self.investment = initial_investment
		self.stock_prices = stock_price_dict

	def startState(self):
		return self.start


	def getAction(self, state):
		if investment > self.stock_prices[state]['btc_market_price']:
			return random.choice(self.actions)
		else:
			return random.choice(["Sell", "Hold"])



	def succAndProbReward(self, state, action):
		stock_price = self.stock_prices[state]['btc_market_price']
		newState = state + timedelta(days=1)
		prob, reward = 1, 0 #stays at 0 if action == "Hold"

		if action == "Buy":
			self.investment -= stock_price
			self.total_reward -= stock_price
			reward = stock_price * -1

		elif action == "Sell":
			self.investment += stock_price
			self.total_reward += stock_price
			reward = stock_price

		return newState, prob, reward

	def computeStates(self):
		cur_state = self.startState()
		rewards = [[cur_state, 0]]
		self.states.add(self.startState())
		while cur_state:
			action = self.getAction(cur_state)
			newState, prob, reward = self.succAndProbReward(cur_state, action)
			if newState in self.stock_prices.keys():
				self.states.add(newState)
				cur_state = newState
			else:
				cur_state = None
			rewards.append([newState, action, self.total_reward])
		return rewards

	def getReward(self):
		return self.total_reward


	def investmentRemaining(self):
		return self.investment


def write_csv(rewards):
	with open('Reward_Data_Baseline_Algo2.csv', 'w') as dataFile:
		fileWriter = csv.writer(dataFile)
		for row in rewards:
			fileWriter.writerow(row)


if __name__ == '__main__':
	filepath = '/Users/harper/Desktop/Fall 2017/Bitcoin Project/238_221_project/bitcoin_dataset.csv'
	investment = 1000000
	dt = data.DataUtil()
	d = dt.read_file(filepath)
	first_day = min(d, key=lambda k: d[k])
	baseline = BaselineAlgorithm(first_day, investment, d)
	rewards = baseline.computeStates()
	write_csv(rewards)

