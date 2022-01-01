import pygame
from snake import Snake

cell_size = 15
cells = 40
BG_COLOR = (0, 0, 0)
resolution = (cell_size * cells, cell_size * cells)

class Generation:
	def __init__(self, population=100, cells=40):
		self.population = population
		self.cells = cells
		self.new()
	
	def step(self):
		snakes_alive = 0
		for snake in self.snakes:
			if not snake.alive: continue
			dir = snake.think()
			snake.move(dir)
			if snake.alive: snakes_alive += 1
		if snakes_alive == 0: self.regenerate()
	
	def regenerate(self):
		snakes = sorted(self.snakes, key=lambda x: x.fitness())
		genes = [snakes[-1].i2h, snakes[-2].i2h, snakes[-1].h2o, snakes[-2].h2o]
		snakes = None
		self.new(genes)

	def new(self, genes=None):
		self.snakes = []
		for i in range(self.population):
			self.snakes.append(Snake(MAX=cells, size=5, genes=genes))
		pass


gen = Generation()

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('snake')

def draw_rect(y: int, x: int, color):
	pygame.draw.rect(screen, color, (x * cell_size - 1, y * cell_size - 1, cell_size - 2, cell_size - 2))

while True:
	# handle events
	exit_flag = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:			
			pygame.quit()
			exit_flag = True
		if event.type == pygame.KEYDOWN:
			dir = None
			step = False
			if event.key == pygame.K_LEFT: dir = (0, -1)
			elif event.key == pygame.K_RIGHT: dir = (0, 1)
			elif event.key == pygame.K_UP: dir = (-1, 0)
			elif event.key == pygame.K_DOWN: dir = (1, 0)
			elif event.key == pygame.K_SPACE: step = True
			if dir:
				for snake in gen.snakes:
					if pygame.key.get_mods() & pygame.KMOD_SHIFT:
						wall = snake.scan(dir, Snake.Wall)
						body = snake.scan(dir, Snake.Body)
						food = snake.scan(dir, Snake.Food)
						print(f'wall={wall}, body={body}, food={food}')
					else:
						snake.move(dir)
			if step: gen.step()
	if exit_flag: break
	# draw snakes
	screen.fill(BG_COLOR)
	for snake in gen.snakes:
		if not snake.alive: continue
		for body in snake.body:
			draw_rect(body[0], body[1], (196, 196, 196))
		draw_rect(snake.food[0], snake.food[1], (255, 0, 0))
	# flip buffers
	pygame.display.flip()

print('exit')
