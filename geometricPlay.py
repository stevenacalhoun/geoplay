#! /usr/bin/env/python

import pygame
from pygame.locals import *
import math
from random import randint
import time

# Screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# McSquare size
MCSQUARE_HEIGHT = 100
MCSQUARE_WIDTH = 100
MCSQUARE_SPEED = 15
MCSQUARE_JUMP_SPEED = 30

# Platform size
PLATFORM_WIDTH = 240
PLATFORM_HEIGHT = 40

# Rectangle size
RECTANGLE_WIDTH = 40
RECTANGLE_HEIGHT = 100
RECTANGLE_SPAWN_RATE = 100

# Gravity and ground constants
GRAVITY = 15
GROUND_THICKNESS = 40
GROUND_Y = SCREEN_HEIGHT - GROUND_THICKNESS

# Locations for HUD
SCORE_POS = (25, 10)
LIVES_POS = (1125, 25)
SCORE_FONT_SIZE = 72
HUD_HEIGHT = 100

# Triangle testing stuff
TRIANGLE_HEIGHT = 75
triangleLocations = [(SCREEN_WIDTH * 0.25, 400), (SCREEN_WIDTH * 0.75, 400)]
currentTriangle = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Help text placeholder
BUNCH_O_TEXT_LINES = ["Random task. Cellar door. Watermellon. The boy went down to the", "city with the little puppy. Random task. Cellar door. ", "Watermellon. The boy went down to the city with the little ", "puppy. Random task. Cellar door. Watermellon. The boy went down ", "to the city with the little puppy. Random task. Cellar door. ", "Watermellon. The boy went down to the city with the little ", "puppy."]

# Global variable to draw on the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)

def main():
    # Initialize the screen
    pygame.init()
    pygame.font.init()
    running = True

    # Keep us running until the 'x' is hit
    while running:
        # Check for new events
        event = pygame.event.poll()
    
        scene.displayCurrentScreen()

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                scene.playGame()

# McSquare class
class Mcsquare(pygame.sprite.Sprite):
    # Initializer
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Draw a simple black square
        self.image = pygame.Surface((MCSQUARE_WIDTH, MCSQUARE_HEIGHT))
        self.image.fill(BLACK)

        # Start him on the ground in the center of the screen
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH / 2) - (MCSQUARE_WIDTH / 2)
        self.rect.y = GROUND_Y - MCSQUARE_HEIGHT

        # Set up to update instantly
        self.nextUpdateTime = 0

        # Start of not moving, jumping, or falling
        self.xMove = 0
        self.yMove = 0
        self.movingRight = False
        self.movingLeft = False
        self.jumping = False
        self.falling = False

    # Update based on the current number of ticks
    def update(self, currentTime):
        if self.nextUpdateTime < currentTime:
            # Move the sprite and plan the next update
            self.move()
            self.checkCollisions()
            self.checkBounds()
            self.nextUpdateTime = currentTime + 10

    # Moves McSquare on the screen
    def move(self):
        # Clean up old location
        self.old = self.rect
        blank = pygame.Surface((MCSQUARE_WIDTH, MCSQUARE_HEIGHT))
        blank.fill(WHITE)
        screen.blit(blank, self.old)

        # Move horizontally within the screen bounds
        if (self.rect.x >= 0) and (self.rect.x <= (SCREEN_WIDTH - MCSQUARE_WIDTH)):
            self.rect.x += self.xMove

        # Move vertically
        if self.yMove != 0:
            self.rect.y += self.yMove
            if self.jumping:
                # Slow down the jump
                self.yMove += MCSQUARE_JUMP_SPEED * .04
                if self.yMove >= 0:
                    # Peak of the jump
                    self.falling = True
                    self.jumping = False
                    self.yMove = GRAVITY * .1
            if self.falling:
                if self.yMove < GRAVITY:
                    self.yMove += GRAVITY * .1
                else:
                    self.yMove = GRAVITY

    # Check to see if we've collided with anything
    def checkCollisions(self):
        for platform in scene.platforms:
            if self.rect.colliderect(platform.rect):
                # Moving up
                if self.yMove < 0:
                    self.rect.y = platform.rect.y + PLATFORM_HEIGHT
                # Moving down
                if self.yMove > 0:
                    self.falling = False
                    self.rect.y = platform.rect.y - MCSQUARE_HEIGHT

        # Check to see if we've gotten to the triangle
        if self.rect.colliderect(scene.tri.rect):
            global currentTriangle, triangleLocations

            # Capture the triangle and spawn a new one
            scene.tri.capture()
            scene.removeTriangle()
            if currentTriangle == 0:
                currentTriangle = 1
            else:
                currentTriangle = 0
            scene.spawnTriangle(triangleLocations[currentTriangle])

    # Just to make sure we haven't crossed any bounds
    def checkBounds(self):
        # Left side
        if (self.rect.x < 0):
            self.rect.x = 0
        # Right side
        if (self.rect.x > SCREEN_WIDTH - MCSQUARE_WIDTH):
            self.rect.x = SCREEN_WIDTH - MCSQUARE_WIDTH
        # Ground
        if (self.rect.y > GROUND_Y - MCSQUARE_HEIGHT):
            self.rect.y = GROUND_Y - MCSQUARE_HEIGHT
            self.falling = False
        # Ceiling
        if (self.rect.y < HUD_HEIGHT):
            self.rect.y = HUD_HEIGHT + 1

    def moveLeft(self):
        self.xMove = -MCSQUARE_SPEED

    def moveRight(self):
        self.xMove = MCSQUARE_SPEED

    def stopMoving(self):
        self.xMove = 0

    def jump(self):
        # No double jumping allowed
        if self.jumping == False and self.falling == False:
            self.jumping = True
            self.yMove = -MCSQUARE_JUMP_SPEED

# Platform class
class Platform(pygame.sprite.Sprite):
    # Initializer
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        # Simple rectangular image
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(BLACK)

        # Position the platform by the passed in value
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.nextUpdateTime = 0

    def update(self, currentTime):
        if self.nextUpdateTime < currentTime:
            self.nextUpdateTime = currentTime + 100


# Rectangle rain class
class Rectangle(pygame.sprite.Sprite):
    # Initializer
    def __init__(self, initialPosition):
        pygame.sprite.Sprite.__init__(self)

        # Draw a simple black rectangle
        self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.topleft = initialPosition

        self.fallingSpeed = GRAVITY * .3

        self.nextUpdateTime = 0

        self.alive = True

    def update(self, currentTime):
        if self.nextUpdateTime < currentTime:
            # Move the sprite and plan the next update
            self.move()
            self.checkCollisions()
            self.nextUpdateTime = currentTime + 10

    def move(self):
        # Clean up old location
        self.old = self.rect
        blank = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
        blank.fill(WHITE)
        screen.blit(blank, self.old)

        self.rect.y += self.fallingSpeed

        if self.alive == False:
            # Blank out last location
            self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
            self.image.fill(WHITE)
            

    def despawn(self):
        self.fallingSpeed = 0
        self.alive = False

        # Blank out last location
        blank = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
        blank.fill(WHITE)
        self.image = blank

    def checkCollisions(self):
        # Check collisions with platforms
        for platform in scene.platforms:
            if self.rect.colliderect(platform.rect):
                self.despawn()

        # Check collisions with ground
        if self.rect.y + RECTANGLE_HEIGHT >= GROUND_Y:
            self.despawn()

        # Check collisions with McSquare
        if self.rect.colliderect(scene.mcSquare.rect):
            scene.HUD.removeLife()
            self.despawn()

# Triangle class
class Triangle(pygame.sprite.Sprite):
    # Initializer
    def __init__(self, topPoint, height):
        pygame.sprite.Sprite.__init__(self)

        # C point is simply the passed in topPoint
        cX, cY = topPoint

        # Find the x offset for the other two points
        xOffset = height * math.tan(math.radians(30))

        # bY is simply cY minus the height, and bX is cX minus the offset
        bX = cX - xOffset
        bY = cY + height
        
        # aY is simply cY minus the height, and aX is cX plus the offset
        aX = cX + xOffset
        aY = cY + height

        self.points = [[aX, aY], [bX, bY], [cX, cY]]

        # Draw the triangle and place a rectangle around it for collision detection
        self.height = height
        self.width = 2*xOffset
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image = pygame.image.load("images/triangle.png")
        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))
        # pygame.draw.polygon(screen, (0,0,0), self.points)
        self.rect = pygame.Rect(bX, cY, self.width, self.height)

        self.nextUpdateTime = 0

    # Remove the triangle when it is captured
    def capture(self):
        scene.HUD.addPoint()
        blank = pygame.Surface((self.width, self.height + 1))
        blank.fill(WHITE)
        screen.blit(blank, self.rect)

    def update(self, currentTime):
        if self.nextUpdateTime < currentTime:
            self.nextUpdateTime = currentTime + 100

class HUD():
    def __init__(self):
        # Draw a line to section off the hud
        pygame.draw.line(screen, BLACK, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT))

        # Display the score
        self.score = 0
        self.displayScore()

        # Display lives
        self.remainingLives = 3
        self.displayLives()

    def displayScore(self):
        # Blank out the old score
        blank = pygame.Surface((100, 65))
        blank.fill(WHITE)
        screen.blit(blank, SCORE_POS)

        # Draw new score
        self.font = pygame.font.SysFont('monospace', SCORE_FONT_SIZE)
        self.label = self.font.render(str(self.score), 1, BLACK)
        screen.blit(self.label, SCORE_POS)

    def addPoint(self):
        # Increment the score and redisplay it
        self.score += 1

    def displayLives(self):
        xLoc, yLoc = LIVES_POS

        blank = pygame.Surface((200, 40))
        blank.fill(WHITE)
        screen.blit(blank, (xLoc - 160, yLoc))

        for x in range(self.remainingLives):
            pygame.draw.rect(screen, BLACK, (xLoc - (x * 80), yLoc, 40, 40))

    def removeLife(self):
        self.remainingLives -= 1

    def outOfLives(self):
        return self.remainingLives <= 0

    def resetLives(self):
        self.remainingLives = 3
        self.displayLives()

    def update(self):
        pygame.draw.line(screen, BLACK, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT))
        self.displayScore()
        self.displayLives()


# Class to hold all the different sprites on scrren at one time
class Scene():
    # Initializer
    def __init__(self):
        self.display = 3
        self.difficulty = 2

    def displayCurrentScreen(self):
        if self.display == 0:
            self.playGame()
        elif self.display == 1: 
            self.showDifficulty()
        elif self.display == 2:
            self.showHelp()
        elif self.display == 3:
            self.showMenu()


    # Show the main menu where you can select play, difficulty, or help
    def showMenu(self):
        # Constants for the boxes
        menuBoxWidth = SCREEN_WIDTH/3
        menuBoxHeight = 80
        topBoxY = SCREEN_HEIGHT/4 + 40
        midBoxY = (SCREEN_HEIGHT/2) - (menuBoxHeight/2) + 40
        botBoxY = midBoxY + (midBoxY - topBoxY) + 40

        outlineBoxWidth = menuBoxWidth * 1.05
        outlineBoxHeight = menuBoxHeight * 1.20

        yOffset = (outlineBoxHeight - menuBoxHeight)/2

        menuSelection = 0

        selectionMade = False
        while selectionMade == False:
            screen.fill(WHITE)
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False

            # Key up and down the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menuSelection += 1
                    if menuSelection >= 3:
                        menuSelection = 0
                if event.key == pygame.K_UP:
                    menuSelection -= 1
                    if menuSelection < 0:
                        menuSelection = 2
                if event.key == pygame.K_RETURN:
                    self.display = menuSelection
                    selectionMade = True

            font = pygame.font.SysFont('monospace', 108)
            titleLabel = font.render("Geo-Play", 1, BLACK)
            titleLabelWidth, titleLabelHeight = font.size("Geo-Play")
            screen.blit(titleLabel, ((((SCREEN_WIDTH/2) - (titleLabelWidth/2)), 75)))

            font = pygame.font.SysFont('monospace', 36)

            # Draw top, mid, and bot boxes and their labels
            topLabel = font.render("Play Game", 1, WHITE)
            topLabelWidth, topLabelHeight = font.size("Play Game")
            pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (menuBoxWidth/2), topBoxY, menuBoxWidth, menuBoxHeight))
            screen.blit(topLabel, ((((SCREEN_WIDTH/2) - (topLabelWidth/2)), topBoxY + (menuBoxHeight/2) - (topLabelHeight/2))))

            midLabel = font.render("Select Difficulty", 1, WHITE)
            midLabelWidth, midLabelHeight = font.size("Select Difficulty")
            pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (menuBoxWidth/2), midBoxY, menuBoxWidth, menuBoxHeight))
            screen.blit(midLabel, ((((SCREEN_WIDTH/2) - (midLabelWidth/2)), midBoxY + (menuBoxHeight/2) -( midLabelHeight/2))))

            botLabel = font.render("Game Help", 1, WHITE)
            botLabelWidth, botLabelHeight = font.size("Game Help")
            pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (menuBoxWidth/2), botBoxY, menuBoxWidth, menuBoxHeight))
            screen.blit(botLabel, ((((SCREEN_WIDTH/2) - (botLabelWidth/2)), botBoxY + (menuBoxHeight/2) - (botLabelHeight/2))))

            # Draw a box around the currently selected menu item
            if menuSelection == 0:        
                pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (outlineBoxWidth/2), topBoxY - yOffset, outlineBoxWidth, outlineBoxHeight), 2)
            elif menuSelection == 1:        
                pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (outlineBoxWidth/2), midBoxY - yOffset, outlineBoxWidth, outlineBoxHeight), 2)
            elif menuSelection == 2:        
                pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (outlineBoxWidth/2), botBoxY - yOffset, outlineBoxWidth, outlineBoxHeight), 2)


            pygame.display.flip()

    # Show difficulty options
    def showDifficulty(self):
        # Constants for the boxes
        menuBoxWidth = SCREEN_WIDTH/3
        menuBoxHeight = 80
        topBoxY = SCREEN_HEIGHT/4
        midBoxY = (SCREEN_HEIGHT/2) - (menuBoxHeight/2)
        botBoxY = midBoxY + (midBoxY - topBoxY)

        outlineBoxWidth = menuBoxWidth * 1.05
        outlineBoxHeight = menuBoxHeight * 1.20

        yOffset = (outlineBoxHeight - menuBoxHeight)/2

        menuSelection = 1

        selectionMade = False
        while selectionMade == False:
            screen.fill(WHITE)
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False

            # Key up and down the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menuSelection += 1
                    if menuSelection > 3:
                        menuSelection = 1
                if event.key == pygame.K_UP:
                    menuSelection -= 1
                    if menuSelection < 0:
                        menuSelection = 2
                if event.key == pygame.K_RETURN:
                    self.display = 3
                    self.difficulty = menuSelection
                    selectionMade = True

            font = pygame.font.SysFont('monospace', 36)

            # Draw top, mid, and bot boxes and their labels
            topLabel = font.render("Easy", 1, WHITE)
            topLabelWidth, topLabelHeight = font.size("Easy")
            pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (menuBoxWidth/2), topBoxY, menuBoxWidth, menuBoxHeight))
            screen.blit(topLabel, ((((SCREEN_WIDTH/2) - (topLabelWidth/2)), topBoxY + (menuBoxHeight/2) - (topLabelHeight/2))))

            midLabel = font.render("Medium", 1, WHITE)
            midLabelWidth, midLabelHeight = font.size("Medium")
            pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (menuBoxWidth/2), midBoxY, menuBoxWidth, menuBoxHeight))
            screen.blit(midLabel, ((((SCREEN_WIDTH/2) - (midLabelWidth/2)), midBoxY + (menuBoxHeight/2) -( midLabelHeight/2))))

            botLabel = font.render("Hard", 1, WHITE)
            botLabelWidth, botLabelHeight = font.size("Hard")
            pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (menuBoxWidth/2), botBoxY, menuBoxWidth, menuBoxHeight))
            screen.blit(botLabel, ((((SCREEN_WIDTH/2) - (botLabelWidth/2)), botBoxY + (menuBoxHeight/2) - (botLabelHeight/2))))

            # Draw a box around the currently selected menu item
            if menuSelection == 1:        
                pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (outlineBoxWidth/2), topBoxY - yOffset, outlineBoxWidth, outlineBoxHeight), 2)
            elif menuSelection == 2:        
                pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (outlineBoxWidth/2), midBoxY - yOffset, outlineBoxWidth, outlineBoxHeight), 2)
            elif menuSelection == 3:        
                pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH/2) - (outlineBoxWidth/2), botBoxY - yOffset, outlineBoxWidth, outlineBoxHeight), 2)


            pygame.display.flip()

    # Show the help menu
    def showHelp(self):
        screen.fill(WHITE)
        helpBoxWidth = SCREEN_WIDTH * 0.75
        helpBoxHeight = SCREEN_HEIGHT/2

        backButtonWidth = SCREEN_WIDTH/3
        backButtonHeight = 80

        helpX = (SCREEN_WIDTH/2) - (helpBoxWidth/2)
        helpY = (SCREEN_HEIGHT*0.10)

        backButtonX = (SCREEN_WIDTH/2) - (backButtonWidth/2)
        backButtonY = SCREEN_HEIGHT*0.75

        font = pygame.font.SysFont('monospace', 24)

        pygame.draw.rect(screen, WHITE, (helpX, helpY, helpBoxWidth, helpBoxHeight))

        for lineNum, line in enumerate(BUNCH_O_TEXT_LINES):
            helpText = font.render(line, 1, BLACK)
            screen.blit(helpText, (helpX, helpY + (25*lineNum), helpBoxWidth, helpBoxHeight))
    
        topLabelWidth, topLabelHeight = font.size("Easy")
        pygame.draw.rect(screen, BLACK, (helpX - 10, helpY - 10, helpBoxWidth + 20, helpBoxHeight + 20), 2)

        font = pygame.font.SysFont('monospace', 36)
        backButtonLabel = font.render("Back", 1, WHITE)
        backButtonLabelWidth, backButtonLabelHeight = font.size("Back")
        pygame.draw.rect(screen, BLACK, (backButtonX, backButtonY, backButtonWidth, backButtonHeight))
        screen.blit(backButtonLabel, (backButtonX + (backButtonWidth/2) - (backButtonLabelWidth/2), backButtonY + (backButtonLabelHeight/2), backButtonLabelWidth, backButtonLabelHeight))
        pygame.draw.rect(screen, BLACK, (backButtonX - 10, backButtonY - 10, backButtonWidth + 20, backButtonHeight + 20), 2)

        goBack = False
        while goBack == False:
            event = pygame.event.poll()
            # Key up and down the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    goBack = True
                    self.display = 3

            pygame.display.flip()

    # Start the game
    def playGame(self):
        screen.fill(WHITE)

        platformOne = Platform(((SCREEN_WIDTH * 0.25) - (PLATFORM_WIDTH / 2), 500))
        platformTwo = Platform(((SCREEN_WIDTH * 0.75) - (PLATFORM_WIDTH / 2), 500))
        self.platforms = [platformOne, platformTwo]

        # Draw the hud
        self.HUD = HUD()

        # Get our square character and add him to the dynamic sprite group
        self.mcSquare = Mcsquare()
        self.dynamicSpriteGroup = pygame.sprite.Group(self.mcSquare)
        self.spawnTriangle(triangleLocations[currentTriangle])

        # Create a sprite group to hold the rain
        self.rectangleSpriteGroup = pygame.sprite.Group()

        # Get our platforms from the screen and draw them
        self.staticSpriteGroup = pygame.sprite.Group(self.platforms)
        self.staticSpriteGroup.draw(screen)

        # Draw a ground
        pygame.draw.rect(screen, BLACK, (0, GROUND_Y, SCREEN_WIDTH, GROUND_THICKNESS))

        self.rectangleCounter = 0

        running = True
        while self.HUD.outOfLives() == False and running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False

            # Let the scene handle the movement
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.handleKeyEvent(event)

            currentTime = pygame.time.get_ticks()
            self.update(currentTime)
            pygame.display.flip()

        self.showGameOver()

    # Show game over screen
    def showGameOver(self):
        screen.fill(WHITE)

        mainMenuButtonWidth = SCREEN_WIDTH/3
        mainMenuButtonHeight = 80

        mainMenuButtonX = (SCREEN_WIDTH/2)  - (mainMenuButtonWidth/2)
        mainMenuButtonY = SCREEN_HEIGHT * 0.66

        self.font = pygame.font.SysFont('monospace', SCORE_FONT_SIZE)
        self.label = self.font.render("Game Over", 1, BLACK)
        labelWidth, labelHeight = self.font.size("Game Over")
        screen.blit(self.label, ((SCREEN_WIDTH/2) - (labelWidth/2), SCREEN_HEIGHT*0.25))

        font = pygame.font.SysFont('monospace', 36)
        mainMenuButtonLabel = font.render("Main Menu", 1, WHITE)
        mainMenuButtonLabelWidth, mainMenuButtonLabelHeight = font.size("Main Menu")
        pygame.draw.rect(screen, BLACK, (mainMenuButtonX, mainMenuButtonY, mainMenuButtonWidth, mainMenuButtonHeight))
        screen.blit(mainMenuButtonLabel, (mainMenuButtonX + (mainMenuButtonWidth/2) - (mainMenuButtonLabelWidth/2), mainMenuButtonY + (mainMenuButtonLabelHeight/2), mainMenuButtonLabelWidth, mainMenuButtonLabelHeight))
        pygame.draw.rect(screen, BLACK, (mainMenuButtonX - 10, mainMenuButtonY - 10, mainMenuButtonWidth + 20, mainMenuButtonHeight + 20), 2)


        goBack = False
        while goBack == False:
            event = pygame.event.poll()
            # Key up and down the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    goBack = True
                    self.display = 3

            pygame.display.flip()


    def spawnTriangle(self, topPoint):
        # Spawn a new triangle with the given top point
        self.tri = Triangle(topPoint, TRIANGLE_HEIGHT)
        self.dynamicSpriteGroup.add(self.tri)

    def removeTriangle(self):
        self.dynamicSpriteGroup.remove(self.tri)

    # Hand key input
    def handleKeyEvent(self, event):
        # Key pushed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.mcSquare.moveLeft()
            elif event.key == pygame.K_RIGHT:
                self.mcSquare.moveRight()
            elif event.key == pygame.K_SPACE:
                self.mcSquare.jump()

        # Movement keys let go 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.mcSquare.stopMoving()

    # Update all the sprites on scren
    def update(self, currentTime):
        # Update our dynamic sprite and refresh the screen
        self.dynamicSpriteGroup.update(currentTime)
        self.dynamicSpriteGroup.draw(screen)

        # Remove any dead rectangles
        for rectangle in self.rectangleSpriteGroup:
            if rectangle.alive == False:
                self.rectangleSpriteGroup.remove(rectangle)
                rectangle = None

        # See if we need to spawn a new rectangle
        if self.rectangleCounter >= (RECTANGLE_SPAWN_RATE / self.difficulty):
            self.rectangleCounter = 0
            randomX = randint(0, SCREEN_WIDTH - RECTANGLE_WIDTH)
            self.rectangleSpriteGroup.add(Rectangle((randomX, HUD_HEIGHT + 1)))
        else:
            self.rectangleCounter += 1

        # Update the rectangle rain
        self.rectangleSpriteGroup.update(currentTime)
        self.rectangleSpriteGroup.draw(screen)

        # Update the static sprites
        self.staticSpriteGroup.update(currentTime)
        self.staticSpriteGroup.draw(screen)

        # Update the HUD
        self.HUD.update()

        # Draw a ground
        pygame.draw.rect(screen, BLACK, (0, GROUND_Y, SCREEN_WIDTH, GROUND_THICKNESS))

scene = Scene()

# Run our program
if __name__ == "__main__":
    main()
