# row, col pair in matrix is col, row in pygame

import pygame
import random
import time


display_width = 400
display_height = 400

red = (200, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()

exit = False

init = [0, 0]
goal = [100, 100]
landmarks_loc = [[30, 40], [30, 50], [0, 50], [0, 80], [0, 90], [0, 99]]

def draw_path(path):
	pygame.draw.lines(screen, green, False, [(i[1], i[0]) for i in path], 2)

def draw_landmarks(landmarks_loc):
	for i in (landmarks_loc):
		pygame.draw.circle(screen, blue, [i[1],i[0]], 4)

def calculate_heuristics(a, b):
	return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

def check_valid_state(state, grid):
	x = state[0]
	y = state[1]
	if x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0]) and grid[x][y] == 0:
		return True
	else:
		return False
 
def run_a_star(init, goal, cost):
	delta = [[-1,0], # go up
         [0,-1], # go left
         [1,0], # go down
         [0,1]] # go right

	grid = [[0 for column in range(101)] for row in range(101)]
	# assign 1 for landmarks
	for l in landmarks_loc:
		grid[l[0]][l[1]] = 1


	action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
	opened = []
	g = 0
	f = calculate_heuristics(init, goal)
	opened.append([f, g, init[0], init[1]])
	next = opened.pop()
	visited = []
	visited.append([next[2], next[3]])

	while [next[2], next[3]] != goal:
		x = next[2]
		y = next[3]
		g = next[1]
		f = next[0]
		for a in range(len(delta)):
			x2 = x + delta[a][0]
			y2 = y + delta[a][1]
			if check_valid_state([x2, y2], grid):
				if [x2, y2] not in visited:
					g2 = g + cost
					f2 = g2 + calculate_heuristics([x2, y2], goal)
					opened.append([f2, g2, x2, y2])
					visited.append([x2, y2])
					action[x2][y2] = a
					
		if len(opened) > 0:
			opened.sort()
			opened.reverse()
			next = opened.pop()

	# policy search
	x = goal[0]
	y = goal[1]
	path = []
	path.append([x, y])
	while([x, y] != init):
		x1 = x - delta[action[x][y]][0]
		y1 = y - delta[action[x][y]][1]
		x = x1
		y = y1
		path.append([x, y])
	path.reverse()
	return path



while exit == False:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True

	screen.fill(white)
	pygame.draw.circle(screen, blue, init, 5)
	pygame.draw.circle(screen, red, goal, 5)
	draw_landmarks(landmarks_loc)
	path = run_a_star(init, goal, cost=1)
	draw_path(path)
	pygame.display.update()
	clock.tick(60)