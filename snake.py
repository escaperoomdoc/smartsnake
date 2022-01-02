import numpy as np
import random
import json
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
	DIRS = (Up, Right, Down, Left, UpRight, UpLeft, DownRight, DownLeft)
	Wall = 0
	Body = 1
	Food = 2
	def __init__(self, MAX=40, size=5, genes=None):
		self.MAX = MAX
		self.body = [(random.randint(0, self.MAX-1), random.randint(0, self.MAX-1-size))]
		for i in range(size-1):
			self.body.append((self.body[-1][0], self.body[-1][1] + 1))
		self.food = None
		self.genfood()
		self.i2h = None
		self.h2o = None
		self.moves = 0
		self.foods = 0
		self.alive = True
		if genes:
			self.genesis(genes)
		else:
			self.i2h = np.random.rand(12, 24)
			self.h2o = np.random.rand(4, 12)
	
	def genesis(self, genes):
		self.i2h = np.zeros((12, 24))
		self.h2o = np.zeros((4, 12))
		for y in range(12):
			for x in range(24):
				self.i2h[y][x] = genes[0][y][x] if random.random() < 0.5 else genes[1][y][x]
				if random.random() < 0.02: self.i2h[y][x] = random.random()
		for y in range(4):
			for x in range(12):
				self.h2o[y][x] = genes[2][y][x] if random.random() < 0.5 else genes[3][y][x]
				if random.random() < 0.02: self.h2o[y][x] = random.random()
		pass

	def genfood(self):
		while not self.food or self.food in self.body:
			self.food = (random.randint(0, self.MAX-1), random.randint(0, self.MAX-1))

	def scan(self, dir, target):
		count = 0
		candidate = self.body[-1]
		for i in range(self.MAX):
			count += 1
			candidate = (candidate[0] + dir[0], candidate[1] + dir[1])
			if target == Snake.Wall:
				if (candidate[0] < 0 or candidate[1] < 0 or
					candidate[0] >= self.MAX or candidate[1] >= self.MAX): break
			elif target == Snake.Body:
				if candidate in self.body: break
			elif target == Snake.Food:
				if candidate == self.food: break
			else: return 0
		return (self.MAX - count) / self.MAX
	
	def move(self, dir):
		candidate = self.body[-1]
		candidate = (candidate[0] + dir[0], candidate[1] + dir[1])
		if (candidate[0] < 0 or candidate[1] < 0 or
			 candidate[0] >= self.MAX or candidate[1] >= self.MAX or
			 candidate in self.body or self.moves > (200 + self.foods * 100)):
			 self.alive = False
			 return
		self.body.append(candidate)
		if candidate == self.food:
			self.foods += 1
			self.genfood()
		else: self.body.pop(0)
		self.moves += 1

	def sensors(self):
		input = []
		for dir in Snake.DIRS:
			input.append(self.scan(dir, Snake.Wall))
			input.append(self.scan(dir, Snake.Body))
			input.append(self.scan(dir, Snake.Food))
		return input

	def relu(self, values):
		for value in values:
			value[0] = max(0.0, value[0])
		return values
	
	def think(self):
		input = self.sensors()
		input.append(1.0)
		input_vector = np.array(input).reshape(25,1)
		i2h = np.append(self.i2h, np.ones(12).reshape(12,1), axis=1)
		sums = np.dot(i2h, input_vector)
		hidden = self.relu(sums)
		hidden_vector = np.vstack([hidden, [1.0]])
		h2o = np.append(self.h2o, np.ones(4).reshape(4,1), axis=1)
		outputs = np.dot(h2o, hidden_vector)
		index = np.argmax(outputs)
		if index < 0: index = 0
		if index > 3: index = 3
		return Snake.DIRS[index]
	
	def fitness(self):
		return self.moves**2 * 2**min(self.foods, 10) * max(1, self.foods - 9)


class Generation:
	def __init__(self, population=100, cells=40, genes=None):
		self.generation_count = 0
		self.population = population
		self.cells = cells
		self.best_snake = None
		self.best_fitness = -1.0		
		self.new(genes)
	
	def step(self):
		snakes_alive = 0	
		for snake in self.snakes:
			if not snake.alive: continue
			dir = snake.think()
			snake.move(dir)
			if snake.alive:snakes_alive += 1
			fitness = snake.fitness()
			if fitness > self.best_fitness:
				self.best_fitness = fitness
				self.best_snake = snake
		if snakes_alive == 0: self.regenerate()
	
	def regenerate(self):
		snakes = sorted(self.snakes, key=lambda x: x.fitness())
		genes = [snakes[-1].i2h, snakes[-2].i2h, snakes[-1].h2o, snakes[-2].h2o]
		if self.best_snake:
			print(f'gen={self.generation_count}, moves={self.best_snake.moves}, foods={self.best_snake.foods}, fitness={self.best_snake.fitness()}')
			if self.generation_count % 1 == 0:
				fname = f'./logs/{self.generation_count}_{self.best_snake.moves}_{self.best_snake.foods}_{self.best_snake.fitness()}.json'
				json_dump = json.dumps({'i2h_1': snakes[-1].i2h.tolist(),
												'i2h_2': snakes[-2].i2h.tolist(),
												'h2o_1': snakes[-1].h2o.tolist(),
												'h2o_2': snakes[-2].h2o.tolist()})
				with open(fname, 'w') as f:
					f.write(json_dump)
		self.best_snake = None
		self.best_fitness = -1.0
		self.generation_count += 1
		snakes = None
		self.new(genes)

	def new(self, genes=None):
		self.snakes = []
		for i in range(self.population):
			self.snakes.append(Snake(MAX=self.cells, size=5, genes=genes))
		pass
