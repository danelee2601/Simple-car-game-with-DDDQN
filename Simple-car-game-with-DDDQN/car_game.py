# Simple car game without a button - Class version
import numpy as np

class env_train():

    def __init__(self):
        import pygame
        import time
        import random

        # Initialize pygame
        #pygame.init()

        # Window size (unit = pixel)
        self.display_width = 700
        self.display_height = 800

        # RGB
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.block_color = (53, 115, 255)

        # Car image's width (To calculate if it avoids the obstacle)
        self.car_width = 60

        # Set a window
        #self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))

        # Set a title of the window
        #pygame.display.set_caption('A bit Racey')

        # Set speed of the game preceeding at the end of the loop with it
        self.clock = pygame.time.Clock()

        # Import a car image
        #self.carImg = pygame.image.load('C:\\python64\\envs\\venv\\python64\\car.png')

        ##############  Key information for the agent   ###################
        # Car's coordinate
        self.x = 0  # initialize
        self.y = 0

        # Obstacle's coordinate
        self.obs_x = 0  # initialize
        self.obs_y = 0
        self.obs_x2 = 0  # initialize
        self.obs_y2 = 0

        # Reward
        self.reward = 0  # initialize

        # Done
        self.done = False  # initialize

        # next_state
        self.next_state = 0  # initialize
        #################################

        ###########  Parameters for the agent , the obstacle  ###########

        # How much the agent will move by one step.
        self.acc_change = 0.2

        # How fast the obstacle will come down.
        self.obs_change = 0

        # How big the obstacle will be.
        self.thing_width = 100
        self.thing_height = 100

        ##################################################################

        self.accumulated_acc = 0

        self.speed_booster = 3


    def things_dodged(self, count):
        import pygame
        font = pygame.font.SysFont(None, 25)
        text = font.render("Reward: " + str(count), True, self.black)
        self.gameDisplay.blit(text, (0, 0))

    def things(self, thingx, thingy, thingw, thingh, color):
        import pygame
        pygame.draw.rect(self.gameDisplay, color, [thingx, thingy, thingw, thingh])

    def car(self, x, y):
        self.gameDisplay.blit(self.carImg, (self.x, self.y))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    def message_display(self, text):  # for a message, when the car crashes.
        import pygame
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((self.display_width / 2), (self.display_height / 2))
        self.gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()

    # "RESET" THE ENVIRONMENT!
    # When you restart your game after crashed, you use this function in agent.py.
    def reset(self):
        import random

        # We will restart the same with this function.
        # In agent.py, "state = env.reset()" will be used.

        # Car's coordinate
        self.x = (self.display_width * 0.45)
        self.y = (self.display_height * 0.87)

        # Obstacle's coordinate
        self.obs_x = random.randrange(0, self.display_width)
        self.obs_y = 0
        self.obs_x2 = random.randrange(0, self.display_width)
        self.obs_y2 = -self.display_height/2

        # How fast the obstacle will come down.
        self.obs_change = 8 * self.speed_booster

        # Reward
        self.reward = 0

        # Done
        self.done = False
        self.accumulated_acc = 0

        # Distance detector
        distance_1 = np.sqrt( self.obs_x**2 + self.obs_y**2 )
        distance_2 = np.sqrt( self.obs_x2**2 + self.obs_y2**2 )

        return [self.x, self.accumulated_acc, self.obs_x , self.obs_y  ] # self.obs_change : speed of the obstacle

    def crash(self, ):
        self.message_display('You Crashed')

    def step(self, action):  # "step( action )" Part
        '''
        NOTE : If you'd like to change the state, change that in reset(), step() both.
        '''
        import pygame
        import random

        #########################################################################################
        # Move the agent
        encoded_action = action
        action_decoder = {0: -1 * self.acc_change, 1: self.accumulated_acc * 0.9,
                          2: self.acc_change}  # 0:left / 1:stop / 2:right

        self.accumulated_acc += action_decoder[encoded_action] * self.speed_booster

        if self.accumulated_acc >= 10:
            self.accumulated_acc = 10

        elif self.accumulated_acc <= -10:
            self.accumulated_acc = -10

        #print('self.accumulated_acc :', self.accumulated_acc)

        t = 1  # We're considering 1 second later scene.

        if self.accumulated_acc >= 0:
            self.x += 0.05 * self.accumulated_acc ** 2
        if self.accumulated_acc < 0:
            self.x += -1 * 0.05 * self.accumulated_acc ** 2

        # Move the obstacle
        self.obs_y += self.obs_change
        #self.obs_y2 += self.obs_change
        #########################################################################################

        # Color the background
        #self.gameDisplay.fill(self.white)

        # Draw the car in the window
        #self.car(self.x, self.y)

        # Draw the obstacle in the window
        #self.things(self.obs_x, self.obs_y, self.thing_width, self.thing_height, self.block_color)

        # Draw the dodged count = self.reward
        #self.things_dodged(self.reward)

        # Reward at each step
        reward_at_this_step = 0

        # Success condition ( = the agent successfully dodges the obstacle )
        if self.obs_y > self.display_height:
            # Re-initialize the obstacle's position
            self.obs_x = random.randrange(0, self.display_width)  # Must be removed by excuted by reset() function.
            self.obs_y = 0 - self.thing_height

            # Get +1 reward
            self.reward += 1
            reward_at_this_step = 1

        ''' 2nd obstacle - success condition
        if self.obs_y2 > self.display_height:
            # Re-initialize the obstacle's position
            self.obs_x2 = random.randrange(0, self.display_width)  # Must be removed by excuted by reset() function.
            self.obs_y2 = 0 - self.thing_height

            # Get +1 reward
            self.reward += 1
            reward_at_this_step = 1
            '''

        # 1st crash condition
        if self.x > self.display_width - self.car_width or self.x < 0:
            #self.crash()
            reward_at_this_step = -20

            # Get -2 reward
            self.reward = self.reward - 20

            # Make done True
            self.done = True

        # 2st crash condition
        if self.y < self.obs_y + self.thing_height:
            if self.x > self.obs_x and self.x < self.obs_x + self.thing_width or self.x + self.car_width > self.obs_x and self.x + self.car_width < self.obs_x + self.thing_width:
                #self.crash()

                # Get -2 reward
                self.reward = self.reward - 20
                reward_at_this_step = -20

                # Make done True
                self.done = True

        # Distance detector
        distance_1 = np.sqrt(self.obs_x ** 2 + self.obs_y ** 2)
        distance_2 = np.sqrt(self.obs_x2 ** 2 + self.obs_y2 ** 2)

        # Define next_state
        self.next_state = [self.x, self.accumulated_acc , self.obs_x , self.obs_y  ]  # Don't forget to pre-process it!


        #pygame.display.update()
        # self.clock.tick(60) # Based on FPS (Frame Per Second)
        # print('Proceed')

        return [self.next_state, reward_at_this_step , self.done ] # self.rewarad = total_reward

    def reset_terminal(self):
        self.done = False












class env_replay():
    '''
    NOTE : If you'd like to change the state, change that in reset(), step() both.
    '''
    def __init__(self):
        import pygame
        import time
        import random

        # Initialize pygame
        pygame.init()

        # Window size (unit = pixel)
        self.display_width = 700
        self.display_height = 800

        # RGB
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.block_color = (53, 115, 255)

        # Car image's width (To calculate if it avoids the obstacle)
        self.car_width = 60

        # Set a window
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))

        # Set a title of the window
        pygame.display.set_caption('A bit Racey')

        # Set speed of the game preceeding at the end of the loop with it
        self.clock = pygame.time.Clock()

        # Import a car image
        self.carImg = pygame.image.load('car.png')

        ##############  Key information for the agent   ###################
        # Car's coordinate
        self.x = 0  # initialize
        self.y = 0

        # Obstacle's coordinate
        self.obs_x = 0  # initialize
        self.obs_y = 0
        self.obs_x2 = 0  # initialize
        self.obs_y2 = 0

        # Reward
        self.reward = 0  # initialize

        # Done
        self.done = False  # initialize

        # next_state
        self.next_state = 0  # initialize
        #################################

        ###########  Parameters for the agent , the obstacle  ###########

        # How much the agent will move by one step.
        self.acc_change = 0.2

        # How fast the obstacle will come down.
        self.obs_change = 0

        # How big the obstacle will be.
        self.thing_width = 100
        self.thing_height = 100

        ##################################################################

        self.accumulated_acc = 0

        self.speed_booster = 3

    def things_dodged(self, count):
        import pygame
        font = pygame.font.SysFont(None, 25)
        text = font.render("Reward: " + str(count), True, self.black)
        self.gameDisplay.blit(text, (0, 0))

    def things(self, thingx, thingy, thingw, thingh, color):
        import pygame
        pygame.draw.rect(self.gameDisplay, color, [thingx, thingy, thingw, thingh])

    def car(self, x, y):
        self.gameDisplay.blit(self.carImg, (self.x, self.y))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    def message_display(self, text):  # for a message, when the car crashes.
        import pygame
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((self.display_width / 2), (self.display_height / 2))
        self.gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()

    # "RESET" THE ENVIRONMENT!
    # When you restart your game after crashed, you use this function in agent.py.
    def reset(self):
        import random

        # We will restart the same with this function.
        # In agent.py, "state = env.reset()" will be used.

        # Car's coordinate
        self.x = (self.display_width * 0.45)
        self.y = (self.display_height * 0.87)

        # Obstacle's coordinate
        self.obs_x = random.randrange(0, self.display_width)
        self.obs_y = 0
        self.obs_x2 = random.randrange(0, self.display_width)
        self.obs_y2 = -self.display_height / 2

        # How fast the obstacle will come down.
        self.obs_change = 8 * self.speed_booster

        # Reward
        self.reward = 0

        # Done
        self.done = False
        self.accumulated_acc = 0

        # Distance detector
        distance_1 = np.sqrt(self.obs_x ** 2 + self.obs_y ** 2)
        distance_2 = np.sqrt(self.obs_x2 ** 2 + self.obs_y2 ** 2)

        return [self.x, self.accumulated_acc, self.obs_x , self.obs_y ] # self.obs_change : speed of the obstacle

    def crash(self, ):
        self.message_display('You Crashed')

    def step(self, action):  # "step( action )" Part
        '''
        NOTE : If you'd like to change the state, change that in reset(), step() both.
        '''
        import pygame
        import random

        #########################################################################################
        # Move the agent
        encoded_action = action
        action_decoder = {0: -1 * self.acc_change, 1: self.accumulated_acc * 0.9 , 2: self.acc_change}  # 0:left / 1:stop / 2:right

        self.accumulated_acc += action_decoder[encoded_action] * self.speed_booster

        if self.accumulated_acc >= 10:
            self.accumulated_acc = 10

        elif self.accumulated_acc <= -10:
            self.accumulated_acc = -10

        #print('self.accumulated_acc :',self.accumulated_acc)

        t = 1  # We're considering 1 second later scene.

        if self.accumulated_acc >= 0:
            self.x += 0.05 * self.accumulated_acc ** 2
        if self.accumulated_acc < 0:
            self.x += -1* 0.05 * self.accumulated_acc ** 2

        # Move the obstacle
        self.obs_y += self.obs_change
        self.obs_y2 += self.obs_change
        #########################################################################################

        # Color the background
        self.gameDisplay.fill(self.white)

        # Draw the car in the window
        self.car(self.x, self.y)

        # Draw the obstacle in the window
        self.things(self.obs_x, self.obs_y, self.thing_width, self.thing_height, self.block_color)
        #self.things(self.obs_x2, self.obs_y2, self.thing_width, self.thing_height, self.block_color)

        # Draw the dodged count = self.reward
        self.things_dodged(self.reward)

        # Reward at each step
        reward_at_this_step = 0

        # Success condition ( = the agent successfully dodges the obstacle )
        if self.obs_y > self.display_height:
            # Re-initialize the obstacle's position
            self.obs_x = random.randrange(0, self.display_width)  # Must be removed by excuted by reset() function.
            self.obs_y = 0 - self.thing_height

            # Get +1 reward
            self.reward += 1
            reward_at_this_step = 1

        ''' 2nd obstacle
        if self.obs_y2 > self.display_height:
            # Re-initialize the obstacle's position
            self.obs_x2 = random.randrange(0, self.display_width)  # Must be removed by excuted by reset() function.
            self.obs_y2 = 0 - self.thing_height

            # Get +1 reward
            self.reward += 1
            reward_at_this_step = 1
            '''

        # 1st crash condition
        if self.x > self.display_width - self.car_width or self.x < 0:
            #self.crash()
            reward_at_this_step = -20

            # Get -2 reward
            self.reward = self.reward - 20

            # Make done True
            self.done = True

        # 2st crash condition
        if self.y < self.obs_y + self.thing_height:
            if self.x > self.obs_x and self.x < self.obs_x + self.thing_width or self.x + self.car_width > self.obs_x and self.x + self.car_width < self.obs_x + self.thing_width:
                #self.crash()

                # Get -2 reward
                self.reward = self.reward - 20
                reward_at_this_step = -20

                # Make done True
                self.done = True

        ''' 2nd obstacle
        if self.y < self.obs_y2 + self.thing_height:
            if self.x > self.obs_x2 and self.x < self.obs_x2 + self.thing_width or self.x + self.car_width > self.obs_x2 and self.x + self.car_width < self.obs_x2 + self.thing_width:
                # self.crash()

                # Get -2 reward
                self.reward = self.reward - 20
                reward_at_this_step = -20

                # Make done True
                self.done = True
                '''

        # Distance detector
        distance_1 = np.sqrt(self.obs_x ** 2 + self.obs_y ** 2)
        distance_2 = np.sqrt(self.obs_x2 ** 2 + self.obs_y2 ** 2)

        # Define next_state
        self.next_state = [self.x, self.accumulated_acc , self.obs_x , self.obs_y ]

        pygame.display.update()
        import time
        time.sleep(0.02) # 0.01

        # self.clock.tick(60) # Based on FPS (Frame Per Second)
        # print('Proceed')

        return [self.next_state, reward_at_this_step , self.done  ] # self.rewarad = total_reward

    def total_reward_clear(self):
        self.reward = 0

    def reset_terminal(self):
        self.done = False

# 'EXECUTE
import pygame

'''
import time

env = env()

# Reset
env.reset()

# Proceed
env.step( 2 )
time.sleep(2)

# Proceed
env.step(2)
time.sleep(2)

# Proceed
env.step(2)
time.sleep(2)

# The game window will be closed whehter or not the codes below exist.
pygame.quit()
quit()
'''


'''
NOTE : YOU CAN VISUALIZE DP OR WHATEVER SYSTEM WITH PYGAME!!

- As long as game_loop()s are followed by another game_loop()s, the window is not closed. ( It's not even closed while waiting for DQN to be calculated. )
- Make this "class" format.
e.g.
game_loop() # 1st scene
..
state = env.reset()
..
next_state, reward, done = env.step(action)
..
game_loop() # Updated scene from the 1st
'''
