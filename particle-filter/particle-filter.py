import pygame
import random
from math import *


display_width = 500
display_height = 500

red = (200, 0, 0)
blue = (0, 0, 255)import pygame
import random
from math import *
import time


display_width = 500
display_height = 500

world_size = min(display_width - 10, display_height - 10)

red = (200, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

car_length = 40
car_width = 20

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Particle Filter Demo")
clock = pygame.time.Clock()

screen.fill(white)


def car(x, y):
	pygame.draw.rect(screen, blue, (x, y, car_length, car_width))

def landmarks(locations):
	for loc in locations:
		pygame.draw.circle(screen, black, loc, 20)

def sense(car_x, car_y, landmarks_loc, noise=False):
	measurements = []
	for i in range(len(landmarks_loc)):
		dist = sqrt((car_x - landmarks_loc[i][0])**2 + (car_y - landmarks_loc[i][1])**2)

		if noise:
			## add gaussian noise to the sensed distance
			dist += random.gauss(0.0, 5.0)

		measurements.append(dist)

	return measurements

def measurement_prob(x, y, landmarks_loc, measurements):
	predicted_measurements = sense(x, y, landmarks_loc, noise=False)

	prob = 1.0
	for i in range(len(landmarks_loc)):
		prob *= Gaussian(predicted_measurements[i], 5.0, measurements[i])

	return prob


def Gaussian(mu, sigma, x):
	return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


def main_loop():

	gameExit = False

	car_x = random.randint(10, world_size)
	car_y = random.randint(10, world_size)

	# draw car
	car(car_x, car_y)

	landmarks_loc = []
	# create 4 random landmarks
	for _ in range(4):
		loc_x = random.randint(10, world_size)
		loc_y = random.randint(10, world_size)
		landmarks_loc.append([loc_x, loc_y])

	# draw landmarks based on landmars_loc just found
	landmarks(landmarks_loc)

	measurements = sense(car_x, car_y, landmarks_loc, noise=True)

	# create 1000 random particles and draw them on screen
	particles = []
	for i in range(1000):
		p_x = random.randint(10, world_size)
		p_y = random.randint(10, world_size)
		pygame.draw.circle(screen, red, (p_x, p_y), 2)
		particles.append([p_x, p_y])

	# assign weights to each particle according to measurement prob.
	weights = []
	for i in range(1000):
		weights.append(measurement_prob(particles[i][0], particles[i][1], landmarks_loc, measurements))

	# resampling
	p = []
	index = int(random.random() * 1000)
	beta = 0.0
	mw = max(weights)
	print mw
	for i in range(1000):
		beta += random.random() * 2.0 * mw
		while beta > weights[index]:

	   		beta -= weights[index]
	     	index = (index + 1) % 1000
	     	
		p.append(particles[index])



	particles = p

	#print particles

	for i in range(1000):
		
		pygame.draw.circle(screen, red, (particles[i][0], particles[i][1]), 2)

	pygame.display.update()
	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True

		pygame.display.update()
		clock.tick(60)



main_loop()


green = (0, 155, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Particle Filter Demo")
clock = pygame.time.Clock()

screen.fill(white)

def car(x, y):
	pygame.draw.rect(screen, blue, (x, y, 40, 20))

def landmarks(count):
	landmarks = []
	for i in range(count):
		l_x = random.randrange(10, display_width - 10)
		l_y = random.randrange(10, display_height - 10)
		landmarks.append([l_x, l_y])
		pygame.draw.circle(screen, black, (l_x, l_y), 10)

	return landmarks

def particles():
	p = []
	for _ in range(1000):
		x = int(random.randrange(10, display_width - 10))
		y = int(random.randrange(10, display_height - 10))
		p.append([x, y])
		pygame.draw.circle(screen, red, (x+20, y+10), 1)
	return p

def particles_move(p, delta_x, delta_y):
	for _ in range(1000):
		p[_][0] += delta_x + 0
		p[_][1] += delta_y + 0

	return p


def resample(p, w):
	p2 = []
	# chose index from a uniform distribution
	index = int(random.random() * 1000)
	beta = 0.0
	mw = max(w)
	for i in range(1000):import pygame
import random
from math import *
import time


display_width = 500
display_height = 500

world_size = min(display_width - 10, display_height - 10)

red = (200, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

car_length = 40
car_width = 20

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Particle Filter Demo")
clock = pygame.time.Clock()

screen.fill(white)


def car(x, y):
	pygame.draw.rect(screen, blue, (x, y, car_length, car_width))

def landmarks(locations):
	for loc in locations:
		pygame.draw.circle(screen, black, loc, 20)

def sense(car_x, car_y, landmarks_loc, noise=False):
	measurements = []
	for i in range(len(landmarks_loc)):
		dist = sqrt((car_x - landmarks_loc[i][0])**2 + (car_y - landmarks_loc[i][1])**2)

		if noise:
			## add gaussian noise to the sensed distance
			dist += random.gauss(0.0, 5.0)

		measurements.append(dist)

	return measurements

def measurement_prob(x, y, landmarks_loc, measurements):
	predicted_measurements = sense(x, y, landmarks_loc, noise=False)

	prob = 1.0
	for i in range(len(landmarks_loc)):
		prob *= Gaussian(predicted_measurements[i], 5.0, measurements[i])

	return prob


def Gaussian(mu, sigma, x):
	return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


def main_loop():

	gameExit = False

	car_x = random.randint(10, world_size)
	car_y = random.randint(10, world_size)

	# draw car
	car(car_x, car_y)

	landmarks_loc = []
	# create 4 random landmarks
	for _ in range(4):
		loc_x = random.randint(10, world_size)
		loc_y = random.randint(10, world_size)
		landmarks_loc.append([loc_x, loc_y])

	# draw landmarks based on landmars_loc just found
	landmarks(landmarks_loc)

	measurements = sense(car_x, car_y, landmarks_loc, noise=True)

	# create 1000 random particles and draw them on screen
	particles = []
	for i in range(1000):
		p_x = random.randint(10, world_size)
		p_y = random.randint(10, world_size)
		pygame.draw.circle(screen, red, (p_x, p_y), 2)
		particles.append([p_x, p_y])

	# assign weights to each particle according to measurement prob.
	weights = []
	for i in range(1000):
		weights.append(measurement_prob(particles[i][0], particles[i][1], landmarks_loc, measurements))

	# resampling
	p = []
	index = int(random.random() * 1000)
	beta = 0.0
	mw = max(weights)
	print mw
	for i in range(1000):
		beta += random.random() * 2.0 * mw
		while beta > weights[index]:

	   		beta -= weights[index]
	     	index = (index + 1) % 1000
	     	
		p.append(particles[index])



	particles = p

	#print particles

	for i in range(1000):
		
		pygame.draw.circle(screen, red, (particles[i][0], particles[i][1]), 2)

	pygame.display.update()
	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True

		pygame.display.update()
		clock.tick(60)



main_loop()


	    # randomly chose between 0 and 2*w max
	    beta = beta + random.random()*2*mw
	    while (w[index] < beta):
	        beta = beta - w[index]
	        # considering wheel (indices 1000,1001,1002,...
	        # mean 0,1,2,3,...)
	        index = (index + 1) % 1000 
	    # select current index
	    p2.append(p[index])
	p = p2

	return p

def find_noisy_distance(point1, point2):
	x1 = point1[0]
	y1 = point1[1]
	x2 = point2[0]
	y2 = point2[1]
	return sqrt((x1-x2)**2 + (y1-y2)**2) + random.gauss(0.0, 5.0)

def find_actual_distance(point1, point2):
	x1 = point1[0]
	y1 = point1[1]
	x2 = point2[0]
	y2 = point2[1]
	return sqrt((x1-x2)**2 + (y1-y2)**2)


def measurement_prob(particle, measurement, landmarks):
        
    # calculates how likely a measurement should be
    
    prob = 1.0;
    for i in range(4):
        dist = find_actual_distance(particle, landmarks[i])
        prob *= Gaussian(dist, 5.0, measurement[i])
    return prob 

def Gaussian(mu, sigma, x):
        
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2)) 

def main_loop():
	exit = False
	x = random.randrange(10, display_width - 10)
	y = random.randrange(10, display_height - 10)

	delta_x = 0
	delta_y = 0

	# draw landmarks
	landmarks_list = landmarks(4)
	# draw car
	car(x, y)
	# draw particles
	particles_list = particles()

	# calculate distances from each landmark
	measurements = []
	for l in landmarks_list:
		measurements.append(find_noisy_distance([x, y], l))

	while not exit:
		#screen.fill(white)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					delta_x = 5
				elif event.key == pygame.K_LEFT:
					delta_x = -5
				elif event.key == pygame.K_UP:
					delta_y = -5
				elif event.key == pygame.K_DOWN:
					delta_y = 5

			if event.type == pygame.KEYUP:
				if event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
					delta_x = 0
					delta_y = 0

				particles_list = particles_move(particles_list, delta_x, delta_y)
				print particles_list
		
		x += delta_x
		y += delta_y

		if display_width < x:
			x = display_width
		elif display_height < y:
			y = display_height

		# draw car
		car(x, y)

		# # calculate distances from each landmark
		measurements = []
		for l in landmarks_list:
			measurements.append(find_noisy_distance([x, y], l))

		# # particles_list = particles()
		weights = []
		for i in range(1000):
			weights.append(measurement_prob(particles_list[i],measurements, landmarks_list))

   		particles_list = resample(particles_list, weights)
 	 	
 	# 	sum_x = 0
 	# 	sum_y = 0

  		for p in range(1000):
  		  	pygame.draw.circle(screen, red, (particles_list[p][0]+20, particles_list[p][1]+10), 1)
  		  	# sum_x += particles_list[p][0]
  		  	# sum_y += particles_list[p][1]

  # 		# print sum_x/len(particles_list), sum_y/len(particles_list)
  # 		# print "error in x :", x - sum_x/len(particles_list)
  # 		# print "error in y :", y - sum_y/len(particles_list)
		pygame.display.update()
		clock.tick(30)

main_loop()


