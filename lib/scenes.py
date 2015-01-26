import pygame
from pygame import Surface
from pygame.locals import *
from constants import *
from fonts import *
from boxes import *
from sprites import *
import random
from levels import *

clock = pygame.time.Clock()

class Scene(object):
  mainMenuScene = 0
  levelScene = 1
  difficultyScene = 2
  helpScene = 3
  gameOverScene = 4
  quit = 5

  def __init__(self, screen):
    self.screen = screen

class MainMenu(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)

  # Show the main menu where you can select play, difficulty, or help
  def display(self):
    # Constants for the boxes
    menuBoxWidth = SCREEN_WIDTH/3
    menuBoxHeight = 80

    # Locations for the menu items
    playBoxY = SCREEN_HEIGHT/4 + 40
    diffBoxY = playBoxY + 150
    helpBoxY = diffBoxY + 150
    quitBoxY = helpBoxY + 150

    # Keep up with what's selected
    menuSelection = Scene.levelScene

    # Keep looping unitl somehting has been selected
    selectionMade = False
    while selectionMade == False:
      self.screen.fill(WHITE)
      event = pygame.event.poll()

      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        # Go down one option
        if event.key == pygame.K_DOWN:
          menuSelection += 1
          if menuSelection >= 5:
            menuSelection = Scene.levelScene
        # Go up one option
        if event.key == pygame.K_UP:
          menuSelection -= 1
          if menuSelection < Scene.levelScene:
            menuSelection = Scene.quit
        # Select the current option
        if event.key == pygame.K_RETURN:
          selectionMade = True
          return menuSelection

      # Draw the title
      title = TextLine(self.screen, "Geo-Play", color=BLACK, size=76)
      title.drawByCenter((SCREEN_WIDTH/2, 100))

      # Draw all the menu options
      playBox = Box(self.screen, menuBoxWidth, menuBoxHeight, BLACK)
      playBox.drawByCenter((SCREEN_WIDTH/2, playBoxY))
      playLabel = TextLine(self.screen, "Play Game", color=WHITE, size=36)
      playLabel.drawByCenter((SCREEN_WIDTH/2, playBoxY))

      diffBox = Box(self.screen, menuBoxWidth, menuBoxHeight, BLACK)
      diffBox.drawByCenter((SCREEN_WIDTH/2, diffBoxY))
      diffLabel = TextLine(self.screen, "Select Difficulty", color=WHITE, size=36)
      diffLabel.drawByCenter((SCREEN_WIDTH/2, diffBoxY))

      helpBox = Box(self.screen, menuBoxWidth, menuBoxHeight, BLACK)
      helpBox.drawByCenter((SCREEN_WIDTH/2, helpBoxY))
      helpLabel = TextLine(self.screen, "Game Help", color=WHITE, size=36)
      helpLabel.drawByCenter((SCREEN_WIDTH/2, helpBoxY))

      quitBox = Box(self.screen, menuBoxWidth, menuBoxHeight, BLACK)
      quitBox.drawByCenter((SCREEN_WIDTH/2, quitBoxY))
      quitLabel = TextLine(self.screen, "Quit", color=WHITE, size=36)
      quitLabel.drawByCenter((SCREEN_WIDTH/2, quitBoxY))

      # Draw a box around the currently selected menu item
      if menuSelection == Scene.levelScene:
        playBox.outline()
      elif menuSelection == Scene.difficultyScene:
        diffBox.outline()
      elif menuSelection == Scene.helpScene:
        helpBox.outline()
      elif menuSelection == Scene.quit:
        quitBox.outline()

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
    title = TextLine(self.screen, str(self.score), color=BLACK, size=76)
    title.drawByTopLeft(topLeft=SCORE_POS)

  def addPoints(self, points):
    self.score += points

  def displayLives(self):
    # Display current number of lives
    xLoc, yLoc = LIVES_POS

    for x in range(self.remainingLives):
      pygame.draw.rect(self.screen, BLACK, (xLoc - (x * 80), yLoc, 40, 40))

  def removeLife(self):
    self.remainingLives -= 1

  def livesRemaining(self):
    return self.remainingLives > 0

  def resetLives(self):
    self.remainingLives = 3

  def update(self):
    # Re draw the HUD
    pygame.draw.line(self.screen, BLACK, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT))
    self.displayScore()
    self.displayLives()

class LevelScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)

    # Start off with the first level
    self.levelNum = 1
    self.level = getLevel(self.levelNum)
    self.oldTriLoc = 0

  # Start the game
  def display(self):
    self.screen.fill(WHITE)

    # Generate all the sprite locations for the level
    self.platformParams, self.triangleLocs, self.startingLoc = self.level.generateLevel()

    # Generate the HUD
    self.HUD = HUD(self.screen)

    # Generate all the sprites for the level
    self.generateSprites()

    # Keep up with when we need to draw a new rectangle rain
    self.rectangleCounter = 0

    # Continue so long as we have lives left
    while self.HUD.livesRemaining():
      # Let the scene handle the movement
      event = pygame.event.poll()
      if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        self.handleKeyEvent(event)

      # Update the screen and check for collisions
      self.update()
      self.checkCollisions()
      self.draw()

      # Check to see if we need a new level
      if self.level.levelComplete(self.HUD.score):
        # Increment to the new level and get the new level object
        self.levelNum += 1
        self.level = getLevel(self.levelNum)

        # Regenerate all the new locations and sprites
        self.platformParams, self.triangleLocs, self.startingLoc = self.level.generateLevel()
        self.generateSprites()

      # Update the display according to the FPS
      pygame.display.flip()
      clock.tick(FRAME_RATE)

    # Go to the game over scene when we're out of lives
    return Scene.gameOverScene

  # Generate all the new sprites for a level
  def generateSprites(self):
    # Get our square character and add him to the dynamic sprite group
    self.mcSquare = Mcsquare(self.screen, self.startingLoc)
    self.dynamicSpriteGroup = pygame.sprite.Group(self.mcSquare)

    # Create a sprite group to hold the rain
    self.rectangleSpriteGroup = pygame.sprite.Group()

    # Generate all the platforms from the locations provided by the level
    self.platformSpriteGroup = pygame.sprite.Group()
    self.platforms = []
    for platformParams in self.platformParams:
      platformLoc, platformSize = platformParams
      platform = Platform(self.screen, platformLoc, platformSize)
      self.platforms.append(platform)
      self.platformSpriteGroup.add(platform)

    # Pick a random choice from all the possible triangle locations and spawn one
    self.triangleSpriteGroup = pygame.sprite.Group()
    triangleLoc = random.choice(self.triangleLocs)
    self.spawnTriangle()

  # Spawn a new triangle with the given top point
  def spawnTriangle(self):
    # Make sure we don't spawn a triangle in the same location that got removed
    newLoc = self.oldTriLoc
    while newLoc == self.oldTriLoc:
      newLoc = random.choice(self.triangleLocs)

    self.triangleSpriteGroup.add(Triangle(self.screen, newLoc, TRIANGLE_HEIGHT))

  # Remove a captured triangle
  def removeTriangle(self, triangle):
    # Keep up with where this triangle just was
    self.oldTriLoc = triangle.topPoint
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

    # Remove any dead rectangles
    for rectangle in self.rectangleSpriteGroup:
      if rectangle.alive == False:
        rectangle.update()
        self.rectangleSpriteGroup.remove(rectangle)
        rectangle = None

    # See if we need to spawn a new rectangle
    if self.rectangleCounter >= (RECTANGLE_SPAWN_RATE / self.difficulty):
      # Reset the counter and pick a random location to spawn the rectangle
      self.rectangleCounter = 0
      randomX = random.randint(0, SCREEN_WIDTH - RECTANGLE_WIDTH)

      # Get the type of rectangle we need to spawn
      rectangle = self.level.spawnNewRectangle(randomX)

      # Add the rectangle to our group
      self.rectangleSpriteGroup.add(rectangle)

    # Otherwise increment the counter
    else:
      self.rectangleCounter += 1

    # Update the rectangle rain
    self.rectangleSpriteGroup.update()

    # Update the platform sprites
    self.platformSpriteGroup.update()

    # Update the triangles
    self.triangleSpriteGroup.update()

    # Update the HUD
    self.HUD.update()

  # Checks for collisions with rectangles or triangles
  def checkCollisions(self):
    # Check for triangle collisions
    captureCount = self.mcSquare.checkCollisions(self.platforms, self.triangleSpriteGroup)

    # If one or more have been capture then increment the score and draw a new one
    if captureCount:
      # Capture the triangle and spawn a new one
      for triangle in self.triangleSpriteGroup:
        if triangle.captured:
          self.removeTriangle(triangle)
          triangle = None

      self.spawnTriangle()

      self.HUD.addPoints(captureCount)

    # Check for a hit by the rain
    for rectangle in self.rectangleSpriteGroup:
        hit = rectangle.checkCollisions(self.platforms, self.mcSquare)
        if hit:
          self.HUD.removeLife()

  # Redraws all the current sprites
  def draw(self):
    self.dynamicSpriteGroup.draw(self.screen)
    self.platformSpriteGroup.draw(self.screen)
    self.rectangleSpriteGroup.draw(self.screen)
    self.triangleSpriteGroup.draw(self.screen)

  # Sets the difficult for the level
  def setDifficulty(self, difficulty):
    self.difficulty = difficulty

class DifficultyMenu(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)

  def display(self):
    # Constants for the boxes
    menuBoxWidth = SCREEN_WIDTH/3
    menuBoxHeight = 80
    easyBoxY = SCREEN_HEIGHT/4
    medBoxY = (SCREEN_HEIGHT/2) - (menuBoxHeight/2)
    hardBoxY = medBoxY + (medBoxY - easyBoxY)

    # Keep track of the current selection
    menuSelection = 1

    # Loop until we've made a selection
    selectionMade = False
    while selectionMade == False:
      self.screen.fill(WHITE)
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
          return Scene.mainMenuScene

      font = pygame.font.SysFont('monospace', 36)

      # Draw all the difficulty options
      easyBox = Box(self.screen, menuBoxWidth, menuBoxHeight, BLACK)
      easyBox.drawByCenter((SCREEN_WIDTH/2, easyBoxY))
      easyLabel = TextLine(self.screen, "Easy", color=WHITE, size=36)
      easyLabel.drawByCenter((SCREEN_WIDTH/2, easyBoxY))

      medBox = Box(self.screen, menuBoxWidth, menuBoxHeight, BLACK)
      medBox.drawByCenter((SCREEN_WIDTH/2, medBoxY))
      medLabel = TextLine(self.screen, "Medium", color=WHITE, size=36)
      medLabel.drawByCenter((SCREEN_WIDTH/2, medBoxY))

      hardBox = Box(self.screen, menuBoxWidth, menuBoxHeight, BLACK)
      hardBox.drawByCenter((SCREEN_WIDTH/2, hardBoxY))
      hardLabel = TextLine(self.screen, "Hard", color=WHITE, size=36)
      hardLabel.drawByCenter((SCREEN_WIDTH/2, hardBoxY))

      # Draw a box around the currently selected menu item
      if menuSelection == 1:
        easyBox.outline()
      elif menuSelection == 2:
        medBox.outline()
      elif menuSelection == 3:
        hardBox.outline()

      pygame.display.flip()

  def getDifficulty(self):
    return self.difficulty

class HelpScene(Scene):
  def __init(self):
    Scene.__init__(self, screen)

  def display(self):
    self.screen.fill(WHITE)

    # Constants for the help box
    helpBoxWidth = SCREEN_WIDTH * 0.75
    helpBoxHeight = SCREEN_HEIGHT * 0.5
    helpLoc = SCREEN_WIDTH/2, SCREEN_HEIGHT*0.33

    # Constants for the back button
    backButtonWidth = SCREEN_WIDTH/3
    backButtonHeight = 80
    backButtonLoc = SCREEN_WIDTH/2, SCREEN_HEIGHT*0.75

    # Draw the help box and label
    helpBox = Box(self.screen, helpBoxWidth, helpBoxHeight, WHITE)
    helpBox.drawByCenter(helpLoc)
    helpBox.outline(color=BLACK)

    helpLabel = TextLine(self.screen, "Help Shtuff", color=BLACK, size=36)
    helpLabel.drawByCenter(helpLoc)

    # Draw the back button
    backBox = Box(self.screen, backButtonWidth, backButtonHeight, BLACK)
    backBox.drawByCenter(backButtonLoc)
    backBox.outline()

    backButtonLabel = TextLine(self.screen, "Back", color=WHITE, size=36)
    backButtonLabel.drawByCenter(backButtonLoc)

    # Wait until we want to go back
    goBack = False
    while goBack == False:
      event = pygame.event.poll()
      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          goBack = True
          return Scene.mainMenuScene

      pygame.display.flip()

class GameOverScene(Scene):
  def __init(self):
    Scene.__init__(self, screen)

  # Show game over screen
  def display(self):
    self.screen.fill(WHITE)

    # Constants to hold the main menu button
    mainMenuButtonWidth = SCREEN_WIDTH/3
    mainMenuButtonHeight = 80

    mainMenuButtonX = SCREEN_WIDTH/2
    mainMenuButtonY = SCREEN_HEIGHT * 0.66

    # Draw the game over text
    endLabel = TextLine(self.screen, "Game Over", color=BLACK, size=SCORE_FONT_SIZE)
    endLabel.drawByCenter(((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.25))

    # Draw the back box
    backBox = Box(self.screen, mainMenuButtonWidth, mainMenuButtonHeight, BLACK)
    backBox.drawByCenter((mainMenuButtonX, mainMenuButtonY))
    backButtonLabel = TextLine(self.screen, "Main Menu", color=WHITE, size=36)
    backButtonLabel.drawByCenter((mainMenuButtonX, mainMenuButtonY))
    backBox.outline()

    # Wait until we want to go back
    goBack = False
    while goBack == False:
      event = pygame.event.poll()
      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          goBack = True
          return Scene.mainMenuScene

      pygame.display.flip()
