import pygame
from pygame import Surface
from pygame.locals import *
from constants import *
from fonts import *
from boxes import *
from sprites import *
from random import randint

# Triangle testing stuff
TRIANGLE_HEIGHT = 75
triangleLocations = [(SCREEN_WIDTH * 0.25, 400), (SCREEN_WIDTH * 0.75, 400)]
currentTriangle = 0

clock = pygame.time.Clock()

class Scene(object):
  def __init__(self, screen):
    self.screen = screen

class MainMenu(Scene):
  def __init(self):
    pass

  # Show the main menu where you can select play, difficulty, or help
  def display(self, screen):
    # Constants for the boxes
    menuBoxWidth = SCREEN_WIDTH/3
    menuBoxHeight = 80

    # Locations for the menu items
    playBoxY = SCREEN_HEIGHT/4 + 40
    diffBoxY = playBoxY + 150
    helpBoxY = diffBoxY + 150
    quitBoxY = helpBoxY + 150

    # Keep up with what's selected
    menuSelection = 0

    # Keep looping unitl somehting has been selected
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
            return menuSelection

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

class HUD():
  def __init__(self, screen):
    # Draw a line to section off the hud
    pygame.draw.line(screen, BLACK, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT))

    self.screen = screen

    # Display the score
    self.score = 0

    # Display lives
    self.remainingLives = 3

  def displayScore(self):
    # Draw new score
    title = TextLine(str(self.score), color=BLACK, size=76)
    title.drawByTopLeft(self.screen, topLeft=SCORE_POS)

  def addPoints(self, points):
    self.score += points

  def displayLives(self):
    # Display current number of lives
    xLoc, yLoc = LIVES_POS

    for x in range(self.remainingLives):
      pygame.draw.rect(self.screen, BLACK, (xLoc - (x * 80), yLoc, 40, 40))

  def removeLife(self):
    self.remainingLives -= 1

  def outOfLives(self):
    return self.remainingLives <= 0

  def resetLives(self):
    self.remainingLives = 3

  def update(self):
    # Re draw the HUD
    pygame.draw.line(self.screen, BLACK, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT))
    self.displayScore()
    self.displayLives()

class LevelScene(Scene):
  def __init__(self, screen, difficulty):
    self.screen = screen
    self.difficulty = difficulty
    self.triangleSpriteGroup = pygame.sprite.Group()

  # Start the game
  def display(self, screen):
    screen.fill(WHITE)

    # Draw the hud
    self.HUD = HUD(screen)

    # Get our square character and add him to the dynamic sprite group
    self.mcSquare = Mcsquare(screen)
    self.dynamicSpriteGroup = pygame.sprite.Group(self.mcSquare)
    self.spawnTriangle(triangleLocations[currentTriangle])

    # Create a sprite group to hold the rain
    self.rectangleSpriteGroup = pygame.sprite.Group()

    # Get our platforms from the screen and draw them
    platformOne = Platform(screen, ((SCREEN_WIDTH * 0.25) - (PLATFORM_WIDTH / 2), 500))
    platformTwo = Platform(screen, ((SCREEN_WIDTH * 0.75) - (PLATFORM_WIDTH / 2), 500))
    self.platforms = [platformOne, platformTwo]
    self.platformSpriteGroup = pygame.sprite.Group(self.platforms)
    self.platformSpriteGroup.draw(screen)

    # Draw a ground
    pygame.draw.rect(screen, BLACK, (0, GROUND_Y, SCREEN_WIDTH, GROUND_THICKNESS))

    # Keep up with when we need to draw a new rectangle rain
    self.rectangleCounter = 0

    while self.HUD.outOfLives() == False:
      # Let the scene handle the movement
      event = pygame.event.poll()
      if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        self.handleKeyEvent(event)

      # Update the screen and check for collisions
      self.update()
      self.checkCollisions()
      pygame.display.flip()
      clock.tick(FRAME_RATE)

    return 4

  def spawnTriangle(self, topPoint):
    # Spawn a new triangle with the given top point
    self.triangleSpriteGroup.add(Triangle(self.screen, topPoint, TRIANGLE_HEIGHT))

  def removeTriangle(self, triangle):
    # Remove the capture triangle
    self.triangleSpriteGroup.remove(triangle)

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
    self.screen.fill(WHITE)
    self.dynamicSpriteGroup.update()
    self.dynamicSpriteGroup.draw(self.screen)

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
      self.rectangleSpriteGroup.add(NormalRectangleRain(self.screen, (randomX, HUD_HEIGHT + 1)))
    else:
      self.rectangleCounter += 1

    # Update the rectangle rain
    self.rectangleSpriteGroup.update()
    self.rectangleSpriteGroup.draw(self.screen)

    # Update the platform sprites
    self.platformSpriteGroup.update()
    self.platformSpriteGroup.draw(self.screen)

    # Update the triangles
    self.triangleSpriteGroup.update()
    self.triangleSpriteGroup.draw(self.screen)

    # Update the HUD
    self.HUD.update()

    # Draw a ground
    pygame.draw.rect(self.screen, BLACK, (0, GROUND_Y, SCREEN_WIDTH, GROUND_THICKNESS))

  # Update all the sprites on screen
  def checkCollisions(self):
    global currentTriangle, triangleLocations

    # Check for triangle collisions
    captureCount = self.mcSquare.checkCollisions(self.platforms, self.triangleSpriteGroup)

    # If one or more have been capture then increment the score and draw a new one
    if captureCount:
      # Capture the triangle and spawn a new one
      for triangle in self.triangleSpriteGroup:
        if triangle.captured:
          self.removeTriangle(triangle)
          triangle = None

      # Some test positions for the triangles
      if currentTriangle == 0:
        currentTriangle = 1
      else:
        currentTriangle = 0

      self.spawnTriangle(triangleLocations[currentTriangle])
      self.HUD.addPoints(captureCount)

    # Check for a hit by the rain
    for rectangle in self.rectangleSpriteGroup:
        hit = rectangle.checkCollisions(self.platforms, self.mcSquare)
        if hit:
          self.HUD.removeLife()

class DifficultyMenu(Scene):
  def __init(self):
    pass

  def display(self, screen):
    # Constants for the boxes
    menuBoxWidth = SCREEN_WIDTH/3
    menuBoxHeight = 80
    topBoxY = SCREEN_HEIGHT/4
    midBoxY = (SCREEN_HEIGHT/2) - (menuBoxHeight/2)
    botBoxY = midBoxY + (midBoxY - topBoxY)

    # Keep track of the current selection
    menuSelection = 1

    # Loop until we've made a selection
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
          return 3, menuSelection

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

class HelpScene(Scene):
  def __init(self):
    pass  # Show the help menu

  def display(self, screen):
    screen.fill(WHITE)

    # Constants for the help box
    helpBoxWidth = SCREEN_WIDTH * 0.75
    helpBoxHeight = SCREEN_HEIGHT * 0.5
    helpLoc = SCREEN_WIDTH/2, SCREEN_HEIGHT*0.33

    # Constants for the back button
    backButtonWidth = SCREEN_WIDTH/3
    backButtonHeight = 80
    backButtonLoc = SCREEN_WIDTH/2, SCREEN_HEIGHT*0.75

    # Draw the help box and label
    helpBox = Box(helpBoxWidth, helpBoxHeight, WHITE)
    helpBox.drawByCenter(screen, helpLoc)
    helpBox.outline(screen, color=BLACK)

    helpLabel = TextLine("Help Shtuff", color=BLACK, size=36)
    helpLabel.drawByCenter(screen, center=helpLoc)

    # Draw the back button
    backBox = Box(backButtonWidth, backButtonHeight, BLACK)
    backBox.drawByCenter(screen, backButtonLoc)
    backBox.outline(screen)

    backButtonLabel = TextLine("Back", color=WHITE, size=36)
    backButtonLabel.drawByCenter(screen, center=backButtonLoc)

    # Wait until we want to go back
    goBack = False
    while goBack == False:
      event = pygame.event.poll()
      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          goBack = True
          return 3
          self.display = 3

      pygame.display.flip()

class GameOverScene(Scene):
  def __init(self):
    pass

  # Show game over screen
  def display(self, screen):
    screen.fill(WHITE)

    # Constants to hold the main menu button
    mainMenuButtonWidth = SCREEN_WIDTH/3
    mainMenuButtonHeight = 80

    mainMenuButtonX = SCREEN_WIDTH/2
    mainMenuButtonY = SCREEN_HEIGHT * 0.66

    # Draw the game over text
    endLabel = TextLine("Game Over", color=BLACK, size=SCORE_FONT_SIZE)
    endLabel.drawByCenter(screen, center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.25))

    # Draw the back box
    backBox = Box(mainMenuButtonWidth, mainMenuButtonHeight, BLACK)
    backBox.drawByCenter(screen, (mainMenuButtonX, mainMenuButtonY))
    backButtonLabel = TextLine("Main Menu", color=WHITE, size=36)
    backButtonLabel.drawByCenter(screen, center=(mainMenuButtonX, mainMenuButtonY))
    backBox.outline(screen)

    # Wait until we want to go back
    goBack = False
    while goBack == False:
      event = pygame.event.poll()
      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          goBack = True
          self.display = 3
          return 3

      pygame.display.flip()
