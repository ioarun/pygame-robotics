# The tank game - shoot and destroy the enemy tank

import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

green = (0, 155, 0)
light_green = (0, 255, 0)

display_width = 800
display_height = 600

tankHeight = 20
tankWidth = 40


gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tanks")

clock = pygame.time.Clock()

FPS = 10

direction = "right"

smallfont = pygame.font.SysFont("arial", 25)
medfont = pygame.font.SysFont("arial", 50)
largefont = pygame.font.SysFont("arial", 80)

def tank(x, y, turPos):
	x = int(x)
	y = int(y)

	possibleTurrets = [(x-27, y - 2), 
						(x-26, y - 5),
						(x-25, y - 8),
						(x-23, y - 12),
						(x-20, y - 14),
						(x-18, y - 15),
						(x-15, y - 17),
						(x-13, y - 19),
						(x-11, y-21)]

	pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
	pygame.draw.rect(gameDisplay, black, (x - tankWidth/2, y, tankWidth, tankHeight))
	
	pygame.draw.line(gameDisplay, black, (x, y), possibleTurrets[turPos], 5)

	startX = 15
	# add wheels
	for i in range(7):
		pygame.draw.circle(gameDisplay, black, (x - startX, y + tankHeight), 5)
		startX -= 5

	# return turret position
	return possibleTurrets[turPos]

def pause():
	paused = True
	message_to_screen("Paused",
		black,
		-100,
		size="large")
	message_to_screen("Press C to continue or Q to continue.",
		black,
		25)
	pygame.display.update()
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False

				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		# gameDisplay.fill(white)
		
		clock.tick(5)

def score(score):
	text = smallfont.render("Score: "+str(score), True, black)
	gameDisplay.blit(text, [0, 0])	


def game_controls():

	gcont = True

	while gcont:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()


		gameDisplay.fill(white)
		message_to_screen("Controls", 
			green,
			-100,
			"large")

		message_to_screen("Fire: Spacebar",
			black,
			-30)
		message_to_screen("Move Turret: Up and Down arrows",
			black,
			10)
		message_to_screen("Move Tank: Left and Right arrows",
			black,
			50)

		message_to_screen("Pause: P",
			black,
			90)

		button("play", 150, 500, 100, 50, green, light_green, action="play")
		button("Main", 350, 500, 100, 50, yellow, light_yellow, action="main")
		button("quit", 550, 500, 100, 50, red, light_red, action="quit")

		pygame.display.update()
		clock.tick(15)



def barrier(xlocation, randomHeight, barrier_width):
	pygame.draw.rect(gameDisplay, black,[xlocation, display_height-randomHeight, barrier_width, randomHeight])


def fireShell(xy, tankx, tanky, turPos, gun_power):
	fire = True

	startingShell = list(xy) # from tuple to list conversion
	# print ("FIRE!", xy)

	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# print startingShell[0], startingShell[1]
		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

		startingShell[0] -= (12 - turPos)*2

		# y = x**2
		startingShell[1] += int((((startingShell[0] - xy[0])*0.015)**2) - (turPos + turPos/(12-turPos)))

		if startingShell[1] > display_height:
			fire = False

		pygame.display.update()
		clock.tick(60)

def fireShell2(xy, tankx, tanky, turPos, gun_power):
	fire = True

	startingShell = list(xy) # from tuple to list conversion
	# print ("FIRE!", xy)
	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# print startingShell[0], startingShell[1]
		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

		startingShell[0] -= (12 - turPos)*2

		# y = x**2
		startingShell[1] += int((((startingShell[0] - xy[0])*0.015/(gun_power/50.0))**2) - (turPos + turPos/(12-turPos)))

		if startingShell[1] > display_height:
			hit_x = int((startingShell[0]*display_height)/startingShell[1])
			hit_y = int(display_height)
			print "Last shell:", startingShell[0], startingShell[1]
			print "Impact:", hit_x, hit_y
			fire = False


		pygame.display.update()
		clock.tick(60)



def power(level):
	text = smallfont.render("Power: "+str(level)+"%",True, black)
	gameDisplay.blit(text, [display_width/2, 0])

def game_intro():

	intro = True

	while intro:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.fill(white)
		message_to_screen("Welcome to Tanks!", 
			green,
			-100,
			"large")

		message_to_screen("The objective of the game is to shoot and destroy.",
			black,
			-30)
		message_to_screen("the enemy tank before they destroy you.",
			black,
			10)
		message_to_screen("The more enemies you destroy, the harder they get.",
			black,
			50)

		button("play", 150, 500, 100, 50, green, light_green, action="play")
		button("controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
		button("quit", 550, 500, 100, 50, red, light_red, action="quit")

		pygame.display.update()
		clock.tick(15)

def text_objects(text, color, size):
	if size == "small":	
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)
	elif size == "large":
		textSurface = largefont.render(text, True, color)

	return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight,size = "small"):
	textSurface, textRect = text_objects(msg, color, size)
	textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
	gameDisplay.blit(textSurface, textRect)

def button(text, x, y, width, height, inactive_color, active_color, action=None):
	cur = pygame.mouse.get_pos()
	# returns a tuple (is_left?, is_center?, is_right?)
	click = pygame.mouse.get_pressed()

	if x + width > cur[0] > x and y + height > cur[1] > y:
		pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
		
		if click[0] == 1 and action != None:
			if action == "quit":
				pygame.quit()
				quit()
			if action == "controls":
				game_controls()
			if action == "play":
				gameLoop()
			if action == "main":
				game_intro()
			
	else:
		pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

	text_to_button(text, black, x, y, width, height)

def message_to_screen(msg, color, y_displace=0, size="small"):
	# screen_text = font.render(msg,True, color)
	# gameDisplay.blit(screen_text, [display_width/2, display_height/2])
	textSurface, textRect = text_objects(msg, color, size)
	textRect.center = display_width/2 , display_height/2 + y_displace
	gameDisplay.blit(textSurface, textRect)

# game loop
def gameLoop():
	global direction
	direction = "right"

	gameExit = False
	gameOver = False

	# main tank position on screen
	mainTankX = display_width*0.9
	mainTankY = display_height*0.9

	tankMove = 0

	currentTurPos = 0
	changeTur = 0

	fire_power = 50
	power_change = 0

	xlocation = (display_width/2)+random.randint(-0.2*display_width,0.2*display_width)
	randomHeight = random.randrange(display_height*0.1, display_height*0.6)

	barrier_width = 50

	while not gameExit:

		gameDisplay.fill(white)
		gun = tank(mainTankX, mainTankY, currentTurPos)

		if gameOver == True:
			message_to_screen("Game over.", red, y_displace=-50, size="large")
			message_to_screen("Press C to play again or Q to quit",
			black, y_displace=50, size="medium")
			pygame.display.update()

		while gameOver == True:
			# gameDisplay.fill(white)

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
					tankMove = -5
				elif event.key == pygame.K_RIGHT:
					tankMove = +5
				elif event.key == pygame.K_UP:
					changeTur = 1
				elif event.key == pygame.K_DOWN:
					changeTur = -1
				elif event.key == pygame.K_p:
					pause()
				elif event.key == pygame.K_SPACE:
					# argument = turret location
					# fireShell(gun, mainTankX, mainTankY, currentTurPos, fire_power)
					fireShell2(gun, mainTankX, mainTankY, currentTurPos, fire_power)

				elif event.key == pygame.K_a:
					power_change = -1
				elif event.key == pygame.K_d:
					power_change = 1

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					tankMove = 0

				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					changeTur = 0

				if event.key == pygame.K_a or event.key == pygame.K_d:
					power_change = 0

		mainTankX += tankMove

		currentTurPos += changeTur

		# current turret possition should be between 0 and 8
		if currentTurPos > 8:
			currentTurPos = 8
		elif currentTurPos < 0:
			currentTurPos = 0

		if mainTankX - (tankWidth/2)  < xlocation + barrier_width:
			mainTankX += 5

		fire_power += power_change

		# display the fire_power
		power(fire_power)

		barrier(xlocation, randomHeight, barrier_width)

		pygame.display.update()

		clock.tick(FPS)

	pygame.quit()
	quit()

game_intro()
gameLoop()