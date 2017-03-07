import pygame
import random
import time
from math import *

display_width = 800
display_height = 800

world_size = display_width

red = (200, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

car_length = 60
car_width = 40

car_img = pygame.image.load("car60_40.png")

origin = (display_width/2, display_height/2)

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Moving robot")
clock = pygame.time.Clock()

screen.fill(white)

class robot:
	def __init__(self):
		self.x = random.random()*world_size
		self.y = random.random()*world_size
		self.orientation = random.random() * 2.0 * pi
		self.forward_noise = 0.0
		self.turn_noise	= 0.0
		self.sense_noise = 0.0
	
	def set(self, x, y, orientation):
		if x >= world_size or x < 0:
			raise ValueError, 'X coordinate out of bound'
		if y >= world_size or y < 0:
			raise ValueError, 'Y coordinate out of bound'
		if orientation >= 2*pi or orientation < 0:
			raise ValueError, 'Orientation must be in [0..2pi]'

		self.x = x
		self.y = y
		self.orientation = orientation


	def set_noise(self, f_noise, t_noise, s_noise):
		self.forward_noise = f_noise
		self.turn_noise = t_noise
		self.sense_noise = s_noise


	def move(self, turn, forward):
		if forward < 0:
			raise ValueError, 'Cant move backwards'

		self.orientation = self.orientation + turn + random.gauss(0.0, self.turn_noise)
		self.orientation %= 2*pi

		dist = forward + random.gauss(0.0, self.forward_noise)
		self.x = self.x + dist*cos(self.orientation)
		self.y = self.y - dist*sin(self.orientation)

		self.x %= world_size
		self.y %= world_size

	def sense(self, landmarks_loc, add_noise=False):
		Z = []
		for i in range(len(landmarks_loc)):
			dist = sqrt((self.x - landmarks_loc[i][0])**2 + ((self.y - landmarks_loc[i][1])**2))
			if add_noise:
				dist += random.gauss(0.0, self.sense_noise)

			Z.append(dist)

		return Z


def draw_robot(robot):
	x = robot.x
	y = robot.y
	orientation = robot.orientation
	img = pygame.transform.rotate(car_img, orientation*180/pi)
	screen.blit(img, (x-30, y-20))
	# # in radians
	# print orientation
	# # in degrees
	# print orientation*180/pi
	pygame.draw.circle(screen, blue, (int(x), int(y)), 5)
	# rect = pygame.draw.polygon(screen, blue, ((x-car_length/2,y-car_width/2),(x+car_length/2,y-car_width/2), \
	# 	(x + car_length/2, y + car_width/2), (x-car_length/2, y+car_width/2)))
	


landmarks_loc  = [[200, 200], [600, 600], [200, 600], [600, 200]]

robot = robot()
# robot.set_noise(0.1, 0.01, 5.0)

orientation = 0
#in radians
orientation = orientation*pi/180
robot.set(origin[0], origin[1], orientation)

exit = False

delta_orient = 0.0
delta_forward = 0.0

while exit == False:

	screen.fill(white)
	pygame.draw.line(screen, green, (display_width/2, 0), (display_width/2, display_height), 1)
	pygame.draw.line(screen, black, (0, display_height/2), (display_width, display_height/2), 1)
	for i in range(len(landmarks_loc)):
		pygame.draw.circle(screen, blue, landmarks_loc[i], 20)

	draw_robot(robot)
	pygame.display.update()
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				delta_orient = 0.0175
			elif event.key == pygame.K_RIGHT:
				delta_orient = -0.0175
			elif event.key == pygame.K_UP:
				delta_forward = 1
			elif event.key == pygame.K_DOWN:
				delta_forward = -1
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP \
			or event.key == pygame.K_DOWN:
				delta_orient = 0.0
				delta_forward = 0.0

	robot.move(delta_orient, delta_forward)
	print robot.sense(landmarks_loc)
