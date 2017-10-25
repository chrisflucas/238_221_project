from data import DataUtil
import random
import collections
from itertools import chain, combinations

'''
	Maybe have precomputed master dict mapping college name to all of this relevant information about the 
	college. 'Stanford' => {'median': 100000, ...}

	So state can just be current_college (str), list of applied to colleges (list[str])

	WORK IN PROGRESS: BUGGY RIGHT NOW.
		realizing there is no clear ordering to the states...
		need to keep track of colleges you have not applied to....blows up the search space even more. fuck us.
'''
class BasicMDP():

	'''
		Given a dataset of colleges and certain qualities about that college,
		this MDP defines a basic approach for choosing whether or not to apply to 
		a given college. 
	'''
	def __init__(self, rows, columns=None, column_weights=None, threshold=5):
		self.column_names = columns
		self.data_rows = rows
		self.threshold = 10
		self.column_weights = column_weights
		self._states = self._all_states(rows.keys())


	'''
		Shitty code.
		Return:
			List of all possible states.
	'''
	def _all_states(self, elems):
		def powerset(iterable):
		    s = list(iterable)
		    return chain.from_iterable(combinations(s, r) for r in range(self.threshold))
		def subsets(s):
		    return map(set, powerset(s))
		powerset = powerset(elems)
		states = []
		for ps in powerset:
			as_list = list(ps)
			states.extend( [(dr, as_list) for dr in elems if dr not in as_list] )
		return states
		

	'''
		Start state: (current_college, [colleges_we've_applied_to])
	'''
	def start_state(self):
		random_start = random.choice(self.data_rows.keys())
		return (random_start, [])


	'''
		Precomputed state space... fucking ridiculously large. Not feasible.
	'''
	def states(self):
		return self._states


	'''
		Return if we have applied to our threshold number of schools.
	'''
	def is_end(self, state):
		return len(state) == self.threshold


	'''
		For any given state, we can choose to either apply 
		or not apply for a school.
	'''
	def actions(self, state):
		current_college, applied_colleges = state
		if len(applied_colleges) < self.threshold:

			return ['apply', 'not-apply']
		return ['not-apply']


	'''
		Given our current state and action to apply or not apply, 
		we return a state for all colleges we could apply to. We also 
		update our list of colleges we have applied to.
	'''
	def succ_prob_reward(self, state, action):
		current_college, applied_colleges = state

		def _normalized_p(arr, exclude=False):
			colleges_left = [c for c in self.data_rows.keys() if c not in arr]
			if exclude: colleges_left = colleges_left[:len(colleges_left)-1]
			if len(colleges_left) == 0: return 0
			return float(1)/len(colleges_left)

		if action == 'apply': 
			p = _normalized_p(arr=applied_colleges+[current_college], exclude=False)
			return [ ((college, applied_colleges+[current_college]), p, int(self.data_rows[college]['starting-median-salary']))  \
						for college in self.data_rows.keys() if college not in applied_colleges+[current_college]]

		p = _normalized_p(arr=applied_colleges, exclude=True)
		return [ ((college, applied_colleges), p, 0) for college in self.data_rows.keys() \
					if college not in applied_colleges and college != current_college ]


	'''
		Discount hyperparameter.
		Something to think about modifying.
	'''
	def discount(self):
		return 1


'''
	Runs value iteration algorithm on an MDP.
	Calculates the optimal value for each state.

	VERY BROKEN RIGHT NOW.
'''
def valueIteration(mdp):

	V = collections.defaultdict(lambda: 0) # school-name => Vopt(state)

	def Q(state, action):
		# print state, action
		# for new_state, prob, reward in mdp.succ_prob_reward(state, action):
		# 	print new_state
		# 	print prob
		# 	print reward
		# print '' 
		# print sum(prob * reward + mdp.discount() * V[new_state[0]] \
		# 		for new_state, prob, reward in mdp.succ_prob_reward(state, action))
		return sum(prob * reward + mdp.discount() * V[new_state[0]] \
				for new_state, prob, reward in mdp.succ_prob_reward(state, action))

	while True:
		newV = {}
		for state in mdp.states():
			if mdp.is_end(state): newV[state[0]] = 0
			else:
				newV[state[0]] = max(Q(state, action) for action in mdp.actions(state))

		# print 'MAX'
		print max(abs(V[state[0]] - newV[state[0]]) for state in mdp.states()) 
		#if max(abs(V[state[0]] - newV[state[0]]) for state in mdp.states()) < 1e-10: break
		V = newV

		pi = {}
		for state in mdp.states():
			if mdp.is_end(state): pi[state[0]] = 0
			else:
				pi[state[0]] = max((Q(state, action), action) for action in mdp.actions(state))[1]

		# print ''
		# for state in mdp.states():
		# 	print '{}\t{}\t{}\t'.format(state, V[state[0]], pi[state[0]])
		# print '\n\n\n'


if __name__ == "__main__":
	data_util = DataUtil()
	data_rows = data_util.read_file('data/salaries-by-college-type.csv', extract_school_names=True)
	

	# Sampling very small amount of colleges for testing purposes #
	random_sample = random.sample( data_rows, 4 )
	subset = {}
	for k in random_sample: subset[k] = data_rows[k]
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

	mdp = BasicMDP(subset)
	# start_state = mdp.start_state()

	# print 'Start State: {}'.format(start_state)

	# for a in mdp.actions(start_state):
	# 	successors = mdp.succ_prob_reward(start_state, a)

	# 	print 'Action: {}\t State: {}\t Successors: {}\n'.format(a, start_state, successors)
	# valueIteration(mdp)


