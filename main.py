import pygame
from snake import Snake

cell_size = 15
cells = 40
BG_COLOR = (0, 0, 0)
resolution = (cell_size * cells, cell_size * cells)
snakes = [Snake(cells)]

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('snake')

def drawRect(y: int, x: int, color):
	pygame.draw.rect(screen, color, (x * cell_size - 1, y * cell_size - 1, cell_size - 2, cell_size - 2))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print('exit')
			pygame.quit()
			break
		
		if event.type == pygame.KEYDOWN:
			dir = None
			if event.key == pygame.K_LEFT: dir = (0, -1)
			elif event.key == pygame.K_RIGHT: dir = (0, 1)
			elif event.key == pygame.K_UP: dir = (-1, 0)
			elif event.key == pygame.K_DOWN: dir = (1, 0)
			if dir:
				for snake in snakes:
					snake.move(dir)
	screen.fill(BG_COLOR)
	for snake in snakes:
		for body in snake.body:
			drawRect(body[0], body[1], (196, 196, 196))
		drawRect(snake.food[0], snake.food[1], (255, 0, 0))

	pygame.display.flip()
