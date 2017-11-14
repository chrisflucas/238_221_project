from datetime import date, datetime, timedelta
import data, random, collections

class ModelBasedRL():
	def __init__(self, start_date, last_date, initial_investment, stock_price_dict):
		self.start_date = start_date
		self.last_date = last_date
		self.investment = investment
		self.stock_price_dict = stock_price_dict
		self.num_coins = 0.0
		self.epsilon = 0.05
		self.actions = ['BUY', 'SELL', 'HOLD']
		max_price = float('-inf')
		for k, v in stock_price_dict.iteritems():
			if self.stock_price_dict[k]['btc_market_price'] > max_price:
				max_price = self.stock_price_dict[k]['btc_market_price']

		def _discretize(num):
			num = float(num)
			return round(num, 1)

		def drange(start, stop, step):
		    while start < stop:
		            yield start
		            start += step  
		states = []
		for i in drange(0, max_price, 0.10):
			states.append((_discretize(i), False))
			states.append((_discretize(i), True))

		self.states = states
		# for state in states:
		# 	new_dict = collections.defaultdict(lambda: 0)
		# 	new_dict['BUY'] = 0
		# 	new_dict['SELL'] = 0
		# 	new_dict['HOLD'] = 0
		# 	self.states[state] = new_dict
	
		#self.states = {state: collections.defaultdict(lambda: 0) for state in states}

		# k = random.choice(self.states.keys())
		# print k, self.states[k]
		dates = sorted(self.stock_price_dict.keys())

		state_action_dict = collections.defaultdict(lambda: 0)
		state_action_state_prime_dict = collections.defaultdict(lambda: 0)
		reward_dict = collections.defaultdict(dict)

		for i in range(len(dates)-1):
			day = dates[i]
			next_day = dates[i+1]

			current_bitcoin_dict = self.stock_price_dict[day]
			tomorrow_bitcoin_dict = self.stock_price_dict[next_day]
			current_price = _discretize(current_bitcoin_dict['btc_market_price'])
			tomorrow_price = _discretize(tomorrow_bitcoin_dict['btc_market_price'])

			buy_reward = tomorrow_bitcoin_dict['btc_market_price']-current_bitcoin_dict['btc_market_price']
			sell_reward = current_bitcoin_dict['btc_market_price']-tomorrow_bitcoin_dict['btc_market_price']
			hold_reward = float((buy_reward+sell_reward))/2
			#hold_reward = tomorrow_bitcoin_dict['btc_market_price']-current_bitcoin_dict['btc_market_price']


			state_action_dict[((current_price, True), 'BUY')] += 1
			state_action_dict[((current_price, False), 'BUY')] += 1

			state_action_dict[((current_price, True), 'SELL')] += 1
			state_action_dict[((current_price, False), 'SELL')] += 1

			state_action_dict[((current_price, True), 'HOLD')] += 1
			state_action_dict[((current_price, False), 'HOLD')] += 1

			current_state = (current_price, True)
			current_state2 = (current_price, False)

			if 'BUY' not in reward_dict[current_state]:
				reward_dict[current_state]['BUY'] = 0.0
			if 'SELL' not in reward_dict[current_state]:
				reward_dict[current_state]['SELL'] = 0.0
			if 'HOLD' not in reward_dict[current_state]:
				reward_dict[current_state]['HOLD'] = 0.0

			if 'BUY' not in reward_dict[current_state2]:
				reward_dict[current_state2]['BUY'] = 0.0
			if 'SELL' not in reward_dict[current_state2]:
				reward_dict[current_state2]['SELL'] = 0.0
			if 'HOLD' not in reward_dict[current_state2]:
				reward_dict[current_state2]['HOLD'] = 0.0

			reward_dict[current_state]['BUY'] += buy_reward
			reward_dict[current_state2]['BUY'] += buy_reward
			reward_dict[current_state]['SELL'] += sell_reward
			reward_dict[current_state2]['SELL']+= sell_reward
			reward_dict[current_state]['HOLD'] += hold_reward
			reward_dict[current_state2]['HOLD'] += hold_reward

			if buy_reward > 0:
				state_action_state_prime_dict[(current_state, 'BUY', (tomorrow_price, True))] += 1
				state_action_state_prime_dict[(current_state2, 'BUY', (tomorrow_price, True))] += 1
			else:
				state_action_state_prime_dict[(current_state, 'BUY', (tomorrow_price, False))] += 1
				state_action_state_prime_dict[(current_state2, 'BUY', (tomorrow_price, False))] += 1

			if sell_reward > 0:
				state_action_state_prime_dict[(current_state, 'SELL', (tomorrow_price, True))] += 1
				state_action_state_prime_dict[(current_state2, 'SELL', (tomorrow_price, True))] += 1
			else:
				state_action_state_prime_dict[(current_state, 'SELL', (tomorrow_price, False))] += 1
				state_action_state_prime_dict[(current_state2, 'SELL', (tomorrow_price, False))] += 1

			if hold_reward > 0:
				state_action_state_prime_dict[(current_state, 'HOLD', (tomorrow_price, True))] += 1
				state_action_state_prime_dict[(current_state2, 'HOLD', (tomorrow_price, True))] += 1
			else:
				state_action_state_prime_dict[(current_state, 'HOLD', (tomorrow_price, False))] += 1
				state_action_state_prime_dict[(current_state2, 'HOLD', (tomorrow_price, False))] += 1

		print 'FINISHED FIRST ITER OVER DATA'

		final_dict = collections.defaultdict(dict)
		for i in range(len(dates)-1):
			day = dates[i]
			next_day = dates[i+1]

			current_bitcoin_dict = self.stock_price_dict[day]
			tomorrow_bitcoin_dict = self.stock_price_dict[next_day]
			current_price = _discretize(current_bitcoin_dict['btc_market_price'])
			tomorrow_price = _discretize(tomorrow_bitcoin_dict['btc_market_price'])

			current_state = (current_price, True)
			current_state2 = (current_price, False)

			prob = float(state_action_state_prime_dict[(current_state, 'BUY', (tomorrow_price, True))]+state_action_state_prime_dict[(current_state2, 'BUY', (tomorrow_price, True))])/(state_action_dict[(current_state2, 'BUY')]+state_action_dict[(current_state, 'BUY')])
			final_dict[current_state]['BUY'] = prob
			final_dict[current_state2]['BUY'] = prob

			rew = (reward_dict[current_state2]['BUY']+reward_dict[current_state]['BUY'])/(state_action_dict[(current_state2, 'BUY')]+state_action_dict[(current_state, 'BUY')])
			reward_dict[current_state]['BUY'] = rew
			reward_dict[current_state2]['BUY'] = rew

			prob = float(state_action_state_prime_dict[(current_state, 'SELL', (tomorrow_price, True))]+state_action_state_prime_dict[(current_state2, 'SELL', (tomorrow_price, True))])/(state_action_dict[(current_state2, 'SELL')]+state_action_dict[(current_state, 'SELL')])
			final_dict[current_state]['SELL'] = prob
			final_dict[current_state2]['SELL'] = prob

			rew = (reward_dict[current_state2]['SELL']+reward_dict[current_state]['SELL'])/(state_action_dict[(current_state2, 'SELL')]+state_action_dict[(current_state, 'SELL')])
			reward_dict[current_state]['SELL'] = rew
			reward_dict[current_state2]['SELL'] = rew

			prob = float(state_action_state_prime_dict[(current_state, 'HOLD', (tomorrow_price, True))]+state_action_state_prime_dict[(current_state2, 'HOLD', (tomorrow_price, True))])/(state_action_dict[(current_state2, 'HOLD')]+state_action_dict[(current_state, 'HOLD')])
			final_dict[current_state]['HOLD'] = prob
			final_dict[current_state2]['HOLD'] = prob

			rew = (reward_dict[current_state2]['HOLD']+reward_dict[current_state]['HOLD'])/(state_action_dict[(current_state2, 'HOLD')]+state_action_dict[(current_state, 'HOLD')])
			reward_dict[current_state]['HOLD'] = rew
			reward_dict[current_state2]['HOLD'] = rew

		self.transition_probabilites = final_dict
		self.rewards = reward_dict
		#print self.rewards
		self.value, self.policy = self.valueIteration()

	# Start state => (Price of bitcoin at Day 1, None)
	def start_state(self):
		return (self.stock_price_dict[self.start_date], None)

	def is_end(self, state):
		return state == self.last_date

	def actions(self, state):
		if self.investment >= self.stock_price_dict[state]['btc_market_price']:
			return ['BUY', 'SELL', 'HOLD']
		if self.num_coins > 0:
			return ['SELL', 'HOLD']
		return ['HOLD']

	def discount(self):
		return 0.9


	def valueIteration(self):
		k = 0
		gamma = 0.95
		U = {state: 0.0 for state in self.states}
		pi = {state: None for state in self.states}
		while True: 
			Unew = U
			for s in self.states:
				max_action = None
				max_value = float('-inf')
				for a in self.actions:
					if s not in self.rewards or s not in self.transition_probabilites:
						max_action = random.choice(self.actions)
						continue
					val = self.rewards[s][a]*self.transition_probabilites[s][a]
					if val > max_value:
						max_value = val
						max_action = a
				U[s] = max_value
				pi[s] = max_action
			if Unew == U: break
		return U, pi

	def test(self, test_rows):
		

		def _discretize(num):
			num = float(num)
			return round(num, 1)

		def _getAction(state):
			if state not in self.policy: return ['HOLD']
			return self.policy[state]

		def _succAndProbReward():
			investment = 1000000
			made_money = True
			total_reward = 0.0

			for tr in test_rows:

				stock_price = test_rows[tr]['btc_market_price']
				state = (_discretize(stock_price), made_money)

				action = _getAction(state)

				if action == "BUY":
					investment -= stock_price
					total_reward -= stock_price
					reward = stock_price * -1

				elif action == "SELL":
					investment += stock_price
					total_reward += stock_price
					reward = stock_price
			return total_reward
		return _succAndProbReward()

if __name__ == '__main__':


	# def _reformat_test(test):
	# 	new_map = {}
	# 	for k, v in test.iteritems():
	# 		new_key = round(v['btc_market_price'],1)
	# 		new_map[new_key] = new_key
	# 	return new_map


	filepath = 'bitcoin_dataset.csv'
	investment = 1000000
	dt = data.DataUtil()
	train, test = dt.read_file(filepath)
	first_day = min(test)
	last_day = max(train)

	#test = _reformat_test(test)

	rl = ModelBasedRL(first_day, last_day, investment, train)
	reward = rl.test(test)
	print reward
	

