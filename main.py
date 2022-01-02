import pygame
import sys
import json
from snake import Snake, Generation

genes = None
if len(sys.argv) > 1:
	fname = sys.argv[1]
	with open(fname, 'r', encoding='utf-8') as f:
		data = f.read()
		obj = json.loads(data)
		genes = [obj['i2h_1'], obj['i2h_2'], obj['h2o_1'], obj['h2o_2']]
		print(f'genes parsed from file {fname}')

cell_size = 15
cells = 40
BG_COLOR = (0, 0, 0)
resolution = (cell_size * cells, cell_size * cells)
fps = 20

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.display.set_caption('snake')

def draw_rect(y: int, x: int, color):
	pygame.draw.rect(screen, color, (x * cell_size - 1, y * cell_size - 1, cell_size - 2, cell_size - 2))

gen = Generation(genes=genes)
silent_mode = False
auto_mode = False
while True:
	# handle events
	exit_flag = False
	step = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:			
			pygame.quit()
			exit_flag = True
		if event.type == pygame.KEYDOWN:
			dir = None			
			if event.key == pygame.K_LEFT: dir = (0, -1)
			elif event.key == pygame.K_RIGHT: dir = (0, 1)
			elif event.key == pygame.K_UP: dir = (-1, 0)
			elif event.key == pygame.K_DOWN: dir = (1, 0)
			elif event.key == pygame.K_SPACE: step = True
			elif event.key == pygame.K_s: silent_mode = not silent_mode
			elif event.key == pygame.K_a: auto_mode = not auto_mode
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
	# silent mode
	if auto_mode: gen.step()
	# draw snakes
	if not silent_mode:
		screen.fill(BG_COLOR)
		for snake in gen.snakes:
			if not snake.alive: continue
			for body in snake.body:
				if snake == gen.best_snake:
					draw_rect(body[0], body[1], (0, 255, 0))
				else:
					draw_rect(body[0], body[1], (196, 196, 196))
			draw_rect(snake.food[0], snake.food[1], (255, 0, 0))
		# flip buffers
		pygame.display.flip()
	if auto_mode: clock.tick(fps)

print('exit')
