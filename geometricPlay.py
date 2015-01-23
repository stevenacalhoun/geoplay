#! /usr/bin/env/python

import sys
sys.path.insert(0, 'lib')

import pygame
import math
from pygame.locals import *
from random import randint
from fonts import *
from boxes import *
from sprites import *
from constants import *


# Triangle testing stuff
TRIANGLE_HEIGHT = 75
triangleLocations = [(SCREEN_WIDTH * 0.25, 400), (SCREEN_WIDTH * 0.75, 400)]
currentTriangle = 0

# Help text placeholder
BUNCH_O_TEXT_LINES = ["Random task. Cellar door. Watermellon. The boy went down to the", "city with the little puppy. Random task. Cellar door. ", "Watermellon. The boy went down to the city with the little ", "puppy. Random task. Cellar door. Watermellon. The boy went down ", "to the city with the little puppy. Random task. Cellar door. ", "Watermellon. The boy went down to the city with the little ", "puppy."]

# Global variable to draw on the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
screen.fill(WHITE)
clock = pygame.time.Clock()

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
    title = TextLine(str(self.score), color=BLACK, size=76)
    title.drawByTopLeft(screen, topLeft=SCORE_POS)

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

    playBoxY = SCREEN_HEIGHT/4 + 40
    diffBoxY = playBoxY + 150
    helpBoxY = diffBoxY + 150
    quitBoxY = helpBoxY + 150

    menuSelection = 0

    selectionMade = False
    while selectionMade == False:
      screen.fill(WHITE)
      event = pygame.event.poll()

      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
          menuSelection += 1
          if menuSelection >= 4:
            menuSelection = 0
        if event.key == pygame.K_UP:
          menuSelection -= 1
          if menuSelection < 0:
            menuSelection = 3
        if event.key == pygame.K_RETURN:
          if menuSelection == 3:
            pygame.quit()
          else:
            self.display = menuSelection
            selectionMade = True

      # Draw the title
      title = TextLine("Geo-Play", color=BLACK, size=76)
      title.drawByCenter(screen, center=(SCREEN_WIDTH/2, 100))

      # Draw all the menu options
      playBox = Box(menuBoxWidth, menuBoxHeight, BLACK)
      playBox.drawByCenter(screen, (SCREEN_WIDTH/2, playBoxY))
      playLabel = TextLine("Play Game", color=WHITE, size=36)
      playLabel.drawByCenter(screen, center=(SCREEN_WIDTH/2, playBoxY))

      diffBox = Box(menuBoxWidth, menuBoxHeight, BLACK)
      diffBox.drawByCenter(screen, (SCREEN_WIDTH/2, diffBoxY))
      diffLabel = TextLine("Select Difficulty", color=WHITE, size=36)
      diffLabel.drawByCenter(screen, center=(SCREEN_WIDTH/2, diffBoxY))
 
      helpBox = Box(menuBoxWidth, menuBoxHeight, BLACK)
      helpBox.drawByCenter(screen, (SCREEN_WIDTH/2, helpBoxY))
      helpLabel = TextLine("Game Help", color=WHITE, size=36)
      helpLabel.drawByCenter(screen, center=(SCREEN_WIDTH/2, helpBoxY))

      quitBox = Box(menuBoxWidth, menuBoxHeight, BLACK)
      quitBox.drawByCenter(screen, (SCREEN_WIDTH/2, quitBoxY))
      quitLabel = TextLine("Quit", color=WHITE, size=36)
      quitLabel.drawByCenter(screen, center=(SCREEN_WIDTH/2, quitBoxY))

      # Draw a box around the currently selected menu item
      if menuSelection == 0:
        playBox.outline(screen)
      elif menuSelection == 1:
        diffBox.outline(screen)
      elif menuSelection == 2:
        helpBox.outline(screen)
      elif menuSelection == 3:
        quitBox.outline(screen)

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
      topBox = Box(menuBoxWidth, menuBoxHeight, BLACK)
      topBox.drawByCenter(screen, (SCREEN_WIDTH/2, topBoxY))
      topLabel = TextLine("Easy", color=WHITE, size=36)
      topLabel.drawByCenter(screen, center=(SCREEN_WIDTH/2, topBoxY))

      midBox = Box(menuBoxWidth, menuBoxHeight, BLACK)
      midBox.drawByCenter(screen, (SCREEN_WIDTH/2, midBoxY))
      midLabel = TextLine("Medium", color=WHITE, size=36)
      midLabel.drawByCenter(screen, center=(SCREEN_WIDTH/2, midBoxY))

      botBox = Box(menuBoxWidth, menuBoxHeight, BLACK)
      botBox.drawByCenter(screen, (SCREEN_WIDTH/2, botBoxY))
      botLabel = TextLine("Hard", color=WHITE, size=36)
      botLabel.drawByCenter(screen, center=(SCREEN_WIDTH/2, botBoxY))

      # Draw a box around the currently selected menu item
      if menuSelection == 1:
        topBox.outline(screen)
      elif menuSelection == 2:    
        midBox.outline(screen)
      elif menuSelection == 3:
        botBox.outline(screen)


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

    backButtonX = SCREEN_WIDTH/2
    backButtonY = SCREEN_HEIGHT*0.75

    font = pygame.font.SysFont('monospace', 24)

    pygame.draw.rect(screen, WHITE, (helpX, helpY, helpBoxWidth, helpBoxHeight))

    for lineNum, line in enumerate(BUNCH_O_TEXT_LINES):
      helpText = font.render(line, 1, BLACK)
      screen.blit(helpText, (helpX, helpY + (25*lineNum), helpBoxWidth, helpBoxHeight))
  
    topLabelWidth, topLabelHeight = font.size("Easy")
    pygame.draw.rect(screen, BLACK, (helpX - 10, helpY - 10, helpBoxWidth + 20, helpBoxHeight + 20), 2)

    backBox = Box(backButtonWidth, backButtonHeight, BLACK)
    backBox.drawByCenter(screen, (backButtonX, backButtonY))
    backButtonLabel = TextLine("Back", color=WHITE, size=36)
    backButtonLabel.drawByCenter(screen, center=(backButtonX, backButtonY))
    backBox.outline(screen)

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

    platformOne = Platform(screen, ((SCREEN_WIDTH * 0.25) - (PLATFORM_WIDTH / 2), 500))
    platformTwo = Platform(screen, ((SCREEN_WIDTH * 0.75) - (PLATFORM_WIDTH / 2), 500))
    self.platforms = [platformOne, platformTwo]

    # Draw the hud
    self.HUD = HUD()

    # Get our square character and add him to the dynamic sprite group
    self.mcSquare = Mcsquare(screen)
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

      self.update()
      self.checkCollisions()
      pygame.display.flip()
      clock.tick(FRAME_RATE)

    self.showGameOver()

  # Show game over screen
  def showGameOver(self):
    screen.fill(WHITE)

    mainMenuButtonWidth = SCREEN_WIDTH/3
    mainMenuButtonHeight = 80

    mainMenuButtonX = SCREEN_WIDTH/2
    mainMenuButtonY = SCREEN_HEIGHT * 0.66


    endLabel = TextLine("Game Over", color=BLACK, size=SCORE_FONT_SIZE)
    endLabel.drawByCenter(screen, center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.25))

    backBox = Box(mainMenuButtonWidth, mainMenuButtonHeight, BLACK)
    backBox.drawByCenter(screen, (mainMenuButtonX, mainMenuButtonY))
    backButtonLabel = TextLine("Main Menu", color=WHITE, size=36)
    backButtonLabel.drawByCenter(screen, center=(mainMenuButtonX, mainMenuButtonY))
    backBox.outline(screen)

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
    self.tri = Triangle(screen, topPoint, TRIANGLE_HEIGHT)
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

  # Update all the sprites on screen
  def update(self):
    # Update our dynamic sprite and refresh the screen
    self.dynamicSpriteGroup.update()
    self.dynamicSpriteGroup.draw(screen)

    # Remove any dead rectangles
    for rectangle in self.rectangleSpriteGroup:
      if rectangle.alive == False:
        rectangle.update()
        self.rectangleSpriteGroup.remove(rectangle)
        rectangle = None

    # See if we need to spawn a new rectangle
    if self.rectangleCounter >= (RECTANGLE_SPAWN_RATE / self.difficulty):
      self.rectangleCounter = 0
      randomX = randint(0, SCREEN_WIDTH - RECTANGLE_WIDTH)
      self.rectangleSpriteGroup.add(NormalRectangleRain(screen, (randomX, HUD_HEIGHT + 1)))
    else:
      self.rectangleCounter += 1

    # Update the rectangle rain
    self.rectangleSpriteGroup.update()
    self.rectangleSpriteGroup.draw(screen)

    # Update the static sprites
    self.staticSpriteGroup.update()
    self.staticSpriteGroup.draw(screen)

    # Update the HUD
    self.HUD.update()

    # Draw a ground
    pygame.draw.rect(screen, BLACK, (0, GROUND_Y, SCREEN_WIDTH, GROUND_THICKNESS))

  # Update all the sprites on screen
  def checkCollisions(self):
    global currentTriangle, triangleLocations

    capture = self.mcSquare.checkCollisions(self.platforms, self.tri)
    if capture:
      # Capture the triangle and spawn a new one
      self.tri.capture()
      self.removeTriangle()
      if currentTriangle == 0:
        currentTriangle = 1
      else:
        currentTriangle = 0
      self.spawnTriangle(triangleLocations[currentTriangle])
      self.HUD.addPoint()

    for rectangle in self.rectangleSpriteGroup:
        hit = rectangle.checkCollisions(self.platforms, self.mcSquare)
        if hit:
          scene.HUD.removeLife()



scene = Scene()

# Run our program
if __name__ == "__main__":
  main()
