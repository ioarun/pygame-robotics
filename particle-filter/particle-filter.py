import pygame
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


def repeat(car_x, car_y, landmarks_loc, particles, particle_size):
	time.sleep(1)
	screen.fill(white)
	landmarks(landmarks_loc)

	# move the car
	car_x += 10
	car_y -= 10

	car_x %= world_size
	car_y %= world_size

	car(car_x, car_y)

	measurements = sense(car_x, car_y, landmarks_loc, noise=True)

	# create 1000 random particles and draw them on screen
	# particles = []
	# for i in range(1000):
	# 	p_x = random.randint(10, world_size)
	# 	p_y = random.randint(10, world_size)
	# 	pygame.draw.circle(screen, red, (p_x, p_y), 2)
	# 	particles.append([p_x, p_y])

	# move particles
	for i in range(1000):
		particles[i][0] += 10
		particles[i][1] -= 10
		particles[i][0] %= world_size
		particles[i][1] %= world_size
		pygame.draw.circle(screen, red, (particles[i][0] + car_length/2, particles[i][1] + car_width/2), 2)

	# assign weights to each particle according to measurement prob.
	weights = []
	for i in range(1000):
		weights.append(measurement_prob(particles[i][0], particles[i][1], landmarks_loc, measurements))

	# resampling
	p = []
	# chose index from a uniform distribution
	index = int(random.random() * 1000)
	beta = 0.0
	mw = max(weights)
	for i in range(1000):
	    # randomly chose between 0 and 2*w max
	    beta += random.random()*2*mw
	    while (weights[index] < beta):
	        beta -= weights[index]
	        index = (index + 1) % 1000
	    # select current index
	    p.append(particles[index])

	particles = p
	
	for i in range(1000):
		
		pygame.draw.circle(screen, red, (particles[i][0] + car_length/2, particles[i][1] + car_width/2), particle_size)

	pygame.display.update()

	return car_x, car_y, landmarks_loc, particles



def main_loop():

	gameExit = False

	car_x = random.randint(10, world_size)
	car_y = random.randint(10, world_size)

	# draw car
	car(car_x, car_y)

	# create 1000 random particles and draw them on screen
	particles = []
	for i in range(1000):
		p_x = random.randint(10, world_size)
		p_y = random.randint(10, world_size)
		pygame.draw.circle(screen, red, (p_x , p_y), 2)
		particles.append([p_x, p_y])

	landmarks_loc = []
	# create 4 random landmarks
	for _ in range(1):
		loc_x = random.randint(10, world_size)
		loc_y = random.randint(10, world_size)
		landmarks_loc.append([loc_x, loc_y])

	# draw landmarks based on landmars_loc just found
	landmarks(landmarks_loc)

	pygame.display.update()

	car_x, car_y, landmarks_loc, particles = repeat(car_x, car_y, landmarks_loc, particles, 2)
	car_x, car_y, landmarks_loc, particles = repeat(car_x, car_y , landmarks_loc, particles, 8)
	car_x, car_y, landmarks_loc, particles = repeat(car_x, car_y, landmarks_loc, particles, 12)
	car_x, car_y, landmarks_loc, particles = repeat(car_x, car_y, landmarks_loc, particles, 12)


	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True

		pygame.display.update()
		clock.tick(60)



main_loop()

