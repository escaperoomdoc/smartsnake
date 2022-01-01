#import numpy as np
#import pandas as pd
import random
random.seed()

class Snake:
	Up = (-1, 0)
	Right = (0, 1)
	Down = (1, 0)
	Left = (0, -1)
	UpRight = (-1, 1)
	UpLeft = (-1, -1)
	DownRight = (1, 1)
	DownLeft = (1, -1)
	Wall = 0
	Body = 1
	Food = 2
	def __init__(self, MAX=40, gene=None):
		self.MAX = MAX
		self.body = [(random.randint(0, self.MAX-1), random.randint(0, self.MAX-3))]
		self.body.append((self.body[-1][0], self.body[-1][1] + 1))
		self.body.append((self.body[-1][0], self.body[-1][1] + 1))
		self.food = None
		self.genfood()
	
	def genfood(self):
		while not self.food or self.food in self.body:
			self.food = (random.randint(0, self.MAX-1), random.randint(0, self.MAX-1))

	def scan(self, dir, target):
		count = 0
		candidate = self.body[-1]
		for i in range(self.MAX):
			count += 1
			candidate = (candidate[0] + dir[0], candidate[1] + dir[1])
			if target == Wall:
				if (candidate[0] < 0 or candidate[1] < 0 or
					candidate[0] >= self.MAX or candidate[1] >= self.MAX): break
			elif target == Body:
				if candidate in body: break
			elif target == Food:
				if candidate == self.food: break
			else: return 0
		return (self.MAX - count) / self.MAX
	
	def move(self, dir):
		candidate = self.body[-1]
		candidate = (candidate[0] + dir[0], candidate[1] + dir[1])
		if (candidate[0] < 0 or candidate[1] < 0 or
			 candidate[0] >= self.MAX or candidate[1] >= self.MAX or
			 candidate in self.body): return False
		self.body.append(candidate)
		if candidate == self.food: self.genfood()
		else: self.body.pop(0)
		return True

	def think(self):
		pass
