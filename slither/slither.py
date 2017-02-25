# Snake eats apple and gets bigger

import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Slither")

img = pygame.image.load('snake.png')

block_size = 20
clock = pygame.time.Clock()

FPS = 10

direction = "right"

smallfont = pygame.font.SysFont("arial", 25)
medfont = pygame.font.SysFont("arial", 50)
largefont = pygame.font.SysFont("arial", 80)

def snake(block_size, snakelist):
	if direction == "right":
		head = pygame.transform.rotate(img, 270)
	elif direction == "left":
		head = pygame.transform.rotate(img, 90)
	elif direction == "up":
		head = img
	elif direction == "down":
		head = pygame.transform.rotate(img, 180)

	gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
	for x_y in snakelist[:-1]:
		pygame.draw.rect(gameDisplay, green, [x_y[0], x_y[1], block_size, block_size])

def text_objects(text, color, size):
	if size == "small":	
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)
	elif size == "large":
		textSurface = largefont.render(text, True, color)

	return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
	# screen_text = font.render(msg,True, color)
	# gameDisplay.blit(screen_text, [display_width/2, display_height/2])
	textSurface, textRect = text_objects(msg, color, size)
	textRect.center = display_width/2 , display_height/2 + y_displace
	gameDisplay.blit(textSurface, textRect)

# game loop
def gameLoop():
	global direction
	gameExit = False
	gameOver = False

	lead_x = display_width/2
	lead_y = display_height/2

	lead_x_change = 10
	lead_y_change = 0

	snakelist = []

	snakeLength = 1

	AppleThickness = 30

	randAppleX = round(random.randrange(0, display_width-block_size))#/10.0)*10.0
	randAppleY = round(random.randrange(0, display_height-block_size))#/10.0)*10.0

	while not gameExit:

		while gameOver == True:
			gameDisplay.fill(white)
			message_to_screen("Game over.", red, y_displace=-50, size="large")
			message_to_screen("Press C to play again or Q to quit",
			black, y_displace=50, size="medium")
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						gameLoop()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					direction = "left"
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					direction = "right"
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					direction = "up"
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					direction = "down"
					lead_y_change = block_size
					lead_x_change = 0

		if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
			gameOver = True
			
		lead_x += lead_x_change
		lead_y += lead_y_change

		gameDisplay.fill(white)
		pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
		
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakelist.append(snakeHead)

		if len(snakelist) > snakeLength:
			del snakelist[0]

		for eachSegment in snakelist[:-1]:
			if eachSegment == snakeHead:
				gameOver = True

		snake(block_size, snakelist)
		pygame.display.update()

		# # cross-over/collision-detection code 
		# if lead_x >= randAppleX  and lead_x <= randAppleX + AppleThickness:
		# 	if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
		# 		randAppleX = round(random.randrange(0, display_width-block_size))#/10.0)*10.0
		# 		randAppleY = round(random.randrange(0, display_height-block_size))#/10.0)*10.0
		# 		snakeLength += 1

		if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
			if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
				randAppleX = round(random.randrange(0, display_width-block_size))#/10.0)*10.0
		 		randAppleY = round(random.randrange(0, display_height-block_size))#/10.0)*10.0
				snakeLength += 1

		clock.tick(FPS)

	pygame.quit()
	quit()

gameLoop()