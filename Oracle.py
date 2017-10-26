#import util, math, random
#from collections import defaultdict


Class Oracle():

	def __init__(self):
		self.actions = ["Buy", "Sell", "Hold"]

	def getAction(self, date, first_day, last_day): #first_day = min(d, key=d.get), last_day = max(d, key=d.get)
    		if date == first_day: return "Buy"
    		elif date == last_day: return "Sell"
    		else: return "Hold"


