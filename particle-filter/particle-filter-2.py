import pygame
import random
import time
from math import *
from copy import deepcopy

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
		self.sense_noise = 0.0 # or bearing_noise
	
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

		temp = robot()
		temp.set_noise(0.001, 0.1, 0.1)
		temp.set(self.x, self.y, self.orientation)
		temp.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
		return temp

	def sense(self, landmarks, add_noise=False):
		Z = []
		for i in range(len(landmarks)):
		    bearing_angle = atan2(landmarks[i][0] - self.y, landmarks[i][1] - self.x) - self.orientation
		    
		    if add_noise:
		        bearing_angle += random.gauss(0.0, self.bearing_noise)

		    # avoid angles greater than 2pi
		    bearing_angle %= 2*pi
		    Z.append(bearing_angle)
		    
		return Z # Return vector Z of 4 bearings.

	def measurement_prob(self, measurements, landmarks):
		# calculate the correct measurement
		predicted_measurements = self.sense(landmarks) 

		# compute errors
		error = 1.0
		for i in range(len(measurements)):
		    error_bearing = abs(measurements[i] - predicted_measurements[i])
		    error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
		    
		    # update Gaussian
		    error *= (exp(- (error_bearing ** 2) / (self.sense_noise ** 2) / 2.0) /  
		              sqrt(2.0 * pi * (self.sense_noise ** 2)))

		return error


	def Gaussian(self, mu, sigma, x):
        
		# calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
		return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

def draw_robot(car):
	x = car.x
	y = car.y
	orientation = car.orientation
	img = pygame.transform.rotate(car_img, orientation*180/pi)
	screen.blit(img, (x-30, y-20))
	# # in radians
	# print orientation
	# # in degrees
	# print orientation*180/pi
	# pygame.draw.circle(screen, blue, (int(x), int(y)), 5)
	# rect = pygame.draw.polygon(screen, blue, ((x-car_length/2,y-car_width/2),(x+car_length/2,y-car_width/2), \
	# 	(x + car_length/2, y + car_width/2), (x-car_length/2, y+car_width/2)))

def draw_particles(particles):
	for i in range(len(particles)):
		x = particles[i].x
		y = particles[i].y
		orientation = particles[i].orientation
		pygame.draw.circle(screen, green, (int(x), int(y)), 5)

	
landmarks_loc  = [[200, 200], [600, 600], [200, 600], [600, 200], [200, 300], [300, 200], [500, 200],\
					[200, 200], [200, 500], [300, 600],[500, 600], [600, 500], [600, 300], [400, 200],\
					[200, 400], [400, 600], [600, 400]]

car = robot()
# car.set_noise(0.1, 0.1, 0.1)

orientation = 0
#in radians
orientation = orientation*pi/180
car.set(origin[0], origin[1], orientation)

exit = False

delta_orient = 0.0
delta_forward = 0.0

particles = []
# create particles
for i in range(1000):
	particle = robot()
	# particle.orientation = orientation
	particle.set_noise(0.001, 0.1, 0.1)
	particles.append(particle)

while exit == False:

	screen.fill(white)
	pygame.draw.line(screen, green, (display_width/2, 0), (display_width/2, display_height), 1)
	pygame.draw.line(screen, black, (0, display_height/2), (display_width, display_height/2), 1)
	for i in range(len(landmarks_loc)):
		pygame.draw.circle(screen, blue, landmarks_loc[i], 20)

	draw_robot(car)
	draw_particles(particles)

	pygame.display.update()
	clock.tick(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				delta_orient = 0.0175
			elif event.key == pygame.K_RIGHT:
				delta_orient = -0.0175
			elif event.key == pygame.K_UP:
				delta_forward = 2
			elif event.key == pygame.K_DOWN:
				delta_forward = -2
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP \
			or event.key == pygame.K_DOWN:
				delta_orient = 0.0
				delta_forward = 0.0

	car.move(delta_orient, delta_forward)
	particles2 = []
	for particle in particles:
		# print "before :",particle.x, particle.y, particle.orientation
		# particle.orientation = car.orientation
		particles2.append(particle.move(delta_orient, delta_forward))
		# print "afer :",particle.x, particle.y, particle.orientation

	particles = particles2

	measurements = car.sense(landmarks_loc)

	weights = []
	for i in range(1000):
		weights.append(particles[i].measurement_prob(measurements, landmarks_loc))

	# resampling
	p = []
	index = int(random.random() * 1000)
	beta = 0.0
	mw = max(weights)
	for i in range(1000):
		beta += random.random() * 2.0 * mw
		while beta > weights[index]:
		    beta -= weights[index]
		    index = (index + 1) % 1000
		p.append(particles[index])
	particles = deepcopy(p)