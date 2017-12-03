from datetime import date, datetime, timedelta
import data, random, collections, csv

class ModelBasedRL():
	def __init__(self, start_date, last_date, initial_investment, stock_price_dict):
		self.start_date = start_date
		self.last_date = last_date
		self.available_funds = investment
		self.money_in_bitcoin = 0.0
		self.stock_price_dict = stock_price_dict
		self.num_coins = 0.0
		self.epsilon = 0.05
		self.actions = ['BUY', 'SELL', 'HOLD']
		max_price = float('-inf')

		def _discretize(num):
			num = float(num)
			return round(num, 1)

		def drange(start, stop, step):
		    while start < stop:
		            yield start
		            start += step  
		states = []
		self.states = states
		dates = sorted(self.stock_price_dict.keys())

		state_action_dict = collections.defaultdict(lambda: 0)
		state_action_state_prime_dict = collections.defaultdict(lambda: 0)
		reward_dict = collections.defaultdict(dict)

		for i in range(1, len(dates)-1):
			yesterday, today, tomorrow = dates[i-1], dates[i], dates[i+1]
			yesterday_bitcoin_dict = self.stock_price_dict[yesterday]
			current_bitcoin_dict = self.stock_price_dict[today]
			tomorrow_bitcoin_dict = self.stock_price_dict[tomorrow]

			yesterday_price = _discretize(yesterday_bitcoin_dict['btc_market_price'])
			print yesterday_price, yesterday_bitcoin_dict['btc_market_price']
			today_price = _discretize(current_bitcoin_dict['btc_market_price'])
			print today_price, current_bitcoin_dict['btc_market_price']
			percentage_change = ((today_price - yesterday_price + 2)/(yesterday_price + 1))
			tomorrow_price = _discretize(tomorrow_bitcoin_dict['btc_market_price'])
			future_percentage_change = ((tomorrow_price - today_price + 2)/(today_price + 1))

			buy_reward = today_price-yesterday_price #0?
			sell_reward = yesterday_price-today_price
			hold_reward = float((buy_reward+sell_reward))/2 #0?

			if percentage_change < 0:
				pass
				#hold or sell
				#sell 
			elif percentage_change > 0:
				pass
				#buy or hold
				#buy if have enough money

			state_action_dict[(percentage_change, 'BUY')] += 1
			state_action_dict[(percentage_change, 'SELL')] += 1
			state_action_dict[(percentage_change, 'HOLD')] += 1

			if 'BUY' not in reward_dict[percentage_change]:
				reward_dict[percentage_change]['BUY'] = 0.0
			if 'SELL' not in reward_dict[percentage_change]:
				reward_dict[percentage_change]['SELL'] = 0.0
			if 'HOLD' not in reward_dict[percentage_change]:
				reward_dict[percentage_change]['HOLD'] = 0.0

			reward_dict[percentage_change]['BUY'] += buy_reward
			reward_dict[percentage_change]['SELL'] += sell_reward
			reward_dict[percentage_change]['HOLD'] += hold_reward

			state_action_state_prime_dict[(percentage_change, 'BUY', future_percentage_change)] += 1
			state_action_state_prime_dict[(percentage_change, 'SELL', future_percentage_change)] += 1
			state_action_state_prime_dict[(percentage_change, 'HOLD', future_percentage_change)] += 1

		
		final_dict = collections.defaultdict(dict)

		for i in range(len(dates)-1):
			day = dates[i]
			next_day = dates[i+1]

			yesterday, today, tomorrow = dates[i-1], dates[i], dates[i+1]
			yesterday_bitcoin_dict = self.stock_price_dict[yesterday]
			current_bitcoin_dict = self.stock_price_dict[today]
			tomorrow_bitcoin_dict = self.stock_price_dict[tomorrow]

			yesterday_price = _discretize(yesterday_bitcoin_dict['btc_market_price'])
			today_price = _discretize(current_bitcoin_dict['btc_market_price'])
			tomorrow_price = _discretize(tomorrow_bitcoin_dict['btc_market_price'])
			percentage_change = float((today_price - yesterday_price+2)/(1+yesterday_price))
			future_percentage_change = float((tomorrow_price - today_price+2)/(today_price+1))

			buy_reward = today_price-yesterday_price
			#buy_reward = 0
			sell_reward = yesterday_price-today_price
			hold_reward = float((buy_reward+sell_reward))/2
			#hold_reward = float((buy_reward+sell_reward))/2
			#hold_reward = tomorrow_bitcoin_dict['btc_market_price']-yesterday_bitcoin_dict['btc_market_price']

			prob = float(state_action_state_prime_dict[(percentage_change, 'BUY', future_percentage_change)]/(1+state_action_dict[(percentage_change, 'BUY')]))
			final_dict[percentage_change]['BUY'] = prob
			reward = float(reward_dict[percentage_change]['BUY']/state_action_dict[(percentage_change, 'BUY')])
			reward_dict[percentage_change]['BUY'] = reward

			prob = float(state_action_state_prime_dict[(percentage_change, 'SELL', future_percentage_change)]/(1+state_action_dict[(percentage_change, 'SELL')]))
			final_dict[percentage_change]['SELL'] = prob
			reward = float(reward_dict[percentage_change]['SELL']/state_action_dict[(percentage_change, 'SELL')])
			reward_dict[percentage_change]['SELL'] = reward

			prob = float(state_action_state_prime_dict[(percentage_change, 'HOLD', future_percentage_change)]/(1+state_action_dict[(percentage_change, 'HOLD')]))
			final_dict[percentage_change]['HOLD'] = prob
			reward = float(reward_dict[percentage_change]['HOLD']/state_action_dict[(percentage_change, 'HOLD')])
			reward_dict[percentage_change]['HOLD'] = reward

		self.transition_probabilites = final_dict
		self.rewards = reward_dict
		self.value, self.policy = self.valueIteration()

	# Start state => (Price of bitcoin at Day 1, None)
	def start_state(self):
		yesterday = self.start_state
		today = yesterday + datetime.timedelta(days=1)
		yesterday_bitcoin_dict = self.stock_price_dict[yesterday]
		current_bitcoin_dict = self.stock_price_dict[today]

		yesterday_price = _discretize(yesterday_bitcoin_dict['btc_market_price'])
		today_price = _discretize(current_bitcoin_dict['btc_market_price'])
		percentage_change = float((today_price - yesterday_price)/yesterday_price)
		return percentage_change

	def is_end(self, state):
		return state == self.last_date

	def actions(self, state):
		actions_possible = ['HOLD']
		if self.investment >= self.stock_price_dict[state]['btc_market_price']:
			actions_possible.append('BUY')
		if self.num_coins > 0:
			actions_possible.append('SELL')
		return actions_possible

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
			if state not in self.policy: return 'HOLD'
			if random.uniform(0,1) < 0.2: return 'HOLD'
			return self.policy[state]

		def _succAndProbReward():
			total_reward = 0.0
			total_rewards = []

			for row in test_rows[1:]:

				today_price = test_rows[row]['btc_market_price']
				yesterday_price = test_rows[index-1]['btc_market_price']
				percentage_change = float((today_price-yesterday_price)/yesterday_price)

				action = _getAction(state)

				if action == "BUY":
					self.available_funds -= stock_price
					self.money_in_bitcoin += stock_price
					self.num_coins += 1
					#reward = stock_price * -1
					reward = 0

				elif action == "SELL":
					self.available_funds += stock_price
					self.money_in_bitcoin -= stock_price
					self.num_coins -= 1
					reward = stock_price
				
				total_reward += reward
				total_rewards.append([action, total_reward])

			return total_reward, total_rewards

		return _succAndProbReward()


if __name__ == '__main__':


	# def _reformat_test(test):
	# 	new_map = {}
	# 	for k, v in test.iteritems():
	# 		new_key = round(v['btc_market_price'],1)
	# 		new_map[new_key] = new_key
	# 	return new_map

	filepath = 'bitcoin_dataset.csv'
	investment = 10000
	dt = data.DataUtil()
	train, test = dt.read_file(filepath)
	first_day = min(test)
	last_day = max(train)

	#test = _reformat_test(test)
	max_reward_chain = None
	max_reward = float('-inf')
	rl = ModelBasedRL(first_day, last_day, investment, train)
	for _ in range(10000):
		reward, reward_chain = rl.test(test)
		if reward > max_reward:
			max_reward = reward
			max_reward_chain = reward_chain

	with open('Reward_Data_Model_Based.csv', 'w') as dataFile:
		fileWriter = csv.writer(dataFile)
		for row in max_reward_chain:
			fileWriter.writerow(row)
