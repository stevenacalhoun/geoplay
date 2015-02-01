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

PAUSE_DURATION = 100

class Scene(object):
  mainMenuScene = 0
  levelScene = 1
  difficultyScene = 2
  helpScene = 3
  quit = 4
  gameOverScene = 5

  def __init__(self, screen):
    self.screen = screen

class IntroScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)

  def display(self):
    waitCounter = 0
    waitCounterEnd = 75
    moveUp = False

    moveCounter = 0
    doneAnimating = False
    startHeight = SCREEN_HEIGHT/2
    endHeight = 100
    moveCountEnd = 87
    step = (startHeight - endHeight)/moveCountEnd
    title = TextLine(self.screen, "Geo-Play", color=BLACK, size=76)

    while not doneAnimating:
      # Leave the splash screen if a key is hit
      event = pygame.event.poll()
      if event.type == pygame.KEYDOWN:
        return

      # Fill the screen
      self.screen.fill(LIGHT_BLUE)
      overlay = Box(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, alpha=128)
      overlay.drawByTopLeft((0,0))

      # Show the title before moving up
      if not moveUp:
        # Draw the title
        title.drawByCenter((SCREEN_WIDTH/2, startHeight))

        waitCounter += 1
        if waitCounter >= waitCounterEnd:
          moveUp = True

      # Start moving up
      else:
        # Draw the title
        title.drawByCenter((SCREEN_WIDTH/2, startHeight - (step*moveCounter)))

        moveCounter += 1
        if moveCounter > moveCountEnd:
          doneAnimating = True

      pygame.display.flip()

class MainMenu(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
    
    # Set sounds
    self.changeSelection_sound = pygame.mixer.Sound("sounds/Bump.ogg")
    self.confirm_sound = pygame.mixer.Sound("sounds/Bump.ogg")
    
    # Show some rectangles falling down in the background
    self.rectangleCounter = 75
    self.rectangleSpriteGroup = pygame.sprite.Group()
    self.level = Level(normalRainChance=1, bounceRainChance=1, explodingRainChance=1, puddleRainChance=1)

  # Show the main menu where you can select play, difficulty, or help
  def display(self):
    # Keep up with what's selected
    self.menuSelection = Scene.levelScene

    # Keep looping unitl somehting has been selected
    selectionMade = False
    while selectionMade == False:
      self.screen.fill(LIGHT_BLUE)
      event = pygame.event.poll()

      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        # Go down one option
        if event.key == pygame.K_DOWN:
          self.menuSelection += 1
          self.changeSelection_sound.play()
          if self.menuSelection >= 5:
            self.menuSelection = Scene.levelScene
        # Go up one option
        if event.key == pygame.K_UP:
          self.menuSelection -= 1
          self.changeSelection_sound.play()
          if self.menuSelection < Scene.levelScene:
            self.menuSelection = Scene.quit
        # Select the current option
        if event.key == pygame.K_RETURN:
          self.confirm_sound.play()
          selectionMade = True
          return self.menuSelection

      # Draw the background, then blur it out, then draw the menu
      self.drawBackground()
      overlay = Box(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, alpha=128)
      overlay.drawByTopLeft((0,0))
      self.drawMenu()

      # Remove any dead rectangles
      for rectangle in self.rectangleSpriteGroup:
        if rectangle.alive == False:
          rectangle.update()
          self.rectangleSpriteGroup.remove(rectangle)
          rectangle = None

      pygame.display.flip()

  # Draw the falling rectangles
  def drawBackground(self):
    # Control the spawn rate of the rectangles
    self.rectangleCounter += 1
    if self.rectangleCounter >= 65:
      self.rectangleCounter = 0
      randomX = random.randint(0, SCREEN_WIDTH - RECTANGLE_WIDTH)

      # Get the type of rectangle we need to spawn
      rectangle = self.level.spawnNewRectangle(randomX)

      # Add the rectangle to our group
      self.rectangleSpriteGroup.add(rectangle)

    # Redraw all the rain
    self.rectangleSpriteGroup.update()
    self.rectangleSpriteGroup.draw(self.screen)

  # Draw the entire main menu
  def drawMenu(self):
    # Constants for the boxes
    menuBoxWidth = SCREEN_WIDTH/3
    menuBoxHeight = 80

    # Locations for the menu items
    playBoxY = SCREEN_HEIGHT/4 + 40
    diffBoxY = playBoxY + 150
    helpBoxY = diffBoxY + 150
    quitBoxY = helpBoxY + 150

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
    if self.menuSelection == Scene.levelScene:
      playBox.outline()
    elif self.menuSelection == Scene.difficultyScene:
      diffBox.outline()
    elif self.menuSelection == Scene.helpScene:
      helpBox.outline()
    elif self.menuSelection == Scene.quit:
      quitBox.outline()

class HUD():
  def __init__(self, screen):
    # Draw a line to section off the hud
    pygame.draw.line(screen, BLACK, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT))

    self.screen = screen

    # Display the score
    self.score = 0

    # Display lives
    self.remainingLives = 3

    # Image to display for remaining lives
    rawImage = pygame.image.load("images/sprites-individ/stand-left1.png").convert()
    rawImageWidth, rawImageHeight = rawImage.get_rect().size
    transColor = rawImage.get_at((0,0))
    rawImage.set_colorkey(transColor)

    self.lifeImage = pygame.transform.scale(rawImage, (rawImageWidth, rawImageHeight))

  def displayScore(self):
    # Draw new score
    title = TextLine(self.screen, str(self.score), color=BLACK, size=76)
    title.drawByTopLeft(topLeft=SCORE_POS)

  def addPoints(self, points):
    self.score += points

  def displayLives(self):
    # Display current number of lives
    xLoc, yLoc = LIVES_POS

    if self.remainingLives <= 5:
      for x in range(self.remainingLives):
        self.screen.blit(self.lifeImage, (xLoc - (x * 80), yLoc, 40, 40))
        # pygame.draw.rect(self.screen, BLACK, (xLoc - (x * 80), yLoc, 40, 40))
    else:
      lifeCount = TextLine(self.screen, "x " + str(self.remainingLives), color=BLACK, size=38)
      lifeCount.drawByTopLeft((xLoc - 20, yLoc))
      self.screen.blit(self.lifeImage, (xLoc - 85, yLoc, 40, 40))

  def addLife(self):
    self.remainingLives += 1

  def removeLife(self):
    self.remainingLives -= 1

  def livesRemaining(self):
    return self.remainingLives > 0

  def resetLives(self):
    self.remainingLives = 3

  def displayPauseButton(self):
    pauseBox = Box(self.screen, 200, 25, WHITE)
    pauseBox.drawByCenter((SCREEN_WIDTH/2, 50))
    pauseBox.outline()

    pauseLabel = TextLine(self.screen, str("Esc - ||"), color=BLACK, size=36)
    pauseLabel.drawByCenter(center=(SCREEN_WIDTH/2, 50))

  def update(self):
    # Re draw the HUD
    hudRect = pygame.Rect((0, 0), (SCREEN_WIDTH, HUD_HEIGHT))
    pygame.draw.rect(self.screen, WHITE, hudRect)
    pygame.draw.line(self.screen, BLACK, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT))
    self.displayScore()
    self.displayLives()
    self.displayPauseButton()

class LevelScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
    
    # Sounds
    self.triangle_sound = pygame.mixer.Sound("sounds/Bump.ogg")
    self.hurt_sound = pygame.mixer.Sound("sounds/Bump.ogg")
    self.victory_sound = pygame.mixer.Sound("sounds/Bump.ogg")

    # Start off with the first level
    self.levelNum = 1
    self.level = getLevel(self.levelNum)
    self.oldTriLoc = 0

    self.pausePowerUpCount = 0
    self.pausePowerUp = False

    # Keep up with paused state
    self.paused = False
    self.selectResume = True
    self.selectQuit = False
    self.returnToMain = False

  # Start the game
  def display(self):
    self.screen.fill(LIGHT_BLUE)

    # Generate all the sprite locations for the level
    self.platformParams, self.triangleLocs, self.powerUpLocs, self.startingLoc = self.level.generateLevel()

    # Generate the HUD
    self.HUD = HUD(self.screen)

    # Show a transition screen
    self.showLevelTransitionScreen()

    # Generate all the sprites for the level
    self.generateSprites()
    self.generateGround()

    # Keep up with when we need to draw a new rectangle rain
    self.rectangleCounter = 0

    # Keep up with when to spawn a power up
    self.powerUpCounter = 0

    # Continue so long as we have lives left
    while self.HUD.livesRemaining() and self.returnToMain == False:
      # Let the scene handle the movement
      event = pygame.event.poll()
      if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        self.handleKeyEvent(event)

      # So long as we're not paused continue showing the game
      if self.paused == False:
        # Update the screen and check for collisions
        self.update()
        self.checkCollisions()
        self.draw()
        self.HUD.update()

        # Check to see if we need a new level
        if self.level.levelComplete(self.HUD.score):
          # Increment to the new level and get the new level object
          self.levelNum += 1
          self.level = getLevel(self.levelNum)

          # Show a transition screen
          self.showLevelTransitionScreen()
          self.victory_sound.play()

          # Regenerate all the new locations and sprites
          self.platformParams, self.triangleLocs, self.powerUpLocs, self.startingLoc = self.level.generateLevel()
          self.generateSprites()
          self.generateGround()

      else:
        self.displayPauseInfo()

      # Update the display according to the FPS
      pygame.display.flip()
      clock.tick(FRAME_RATE)

    # Go to the game over scene when we're out of lives or to main menu if wev'e quit
    if self.returnToMain:
      return Scene.mainMenuScene
    else:
      return Scene.gameOverScene

  def showLevelTransitionScreen(self):
    self.screen.fill(LIGHT_BLUE)

    # Constants to hold the main menu button
    nextLevelButtonWidth = SCREEN_WIDTH/3
    nextLevelButtonHeight = 80

    nextLevelButtonX = SCREEN_WIDTH/2
    nextLevelButtonY = SCREEN_HEIGHT * 0.66

    # Draw the game over text
    levelLabel = TextLine(self.screen, "Level " + str(self.levelNum), color=BLACK, size=SCORE_FONT_SIZE)
    levelLabel.drawByCenter(((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.25))

    # Show the final level and score
    captionLabel = TextLine(self.screen, self.level.caption, color=BLACK, size=int((SCORE_FONT_SIZE*.66)))
    captionLabel.drawByCenter(((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.4))

    # Draw the back box
    nextLevelBox = Box(self.screen, nextLevelButtonWidth, nextLevelButtonHeight, BLACK)
    nextLevelBox.drawByCenter((nextLevelButtonX, nextLevelButtonY))
    nextLevelButtonLabel = TextLine(self.screen, "Start Level", color=WHITE, size=36)
    nextLevelButtonLabel.drawByCenter((nextLevelButtonX, nextLevelButtonY))
    nextLevelBox.outline()

    # Wait until we want to go back
    proceed = False
    while proceed == False:
      event = pygame.event.poll()
      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          proceed = True
          return Scene.mainMenuScene

      pygame.display.flip()

  # Generate all the new sprites for a level
  def generateSprites(self):
    # Get our square character and add him to the dynamic sprite group
    self.mcSquare = Mcsquare(self.screen, self.startingLoc, self.level.tileHeight, self.level.jumpSpeed)
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

    # Sprite group to hold the power ups
    self.powerUpSpriteGroup = pygame.sprite.Group()

  # Spawn a new triangle with the given top point
  def spawnTriangle(self):
    # Make sure we don't spawn a triangle in the same location that got removed
    newLoc = self.oldTriLoc
    while newLoc == self.oldTriLoc:
      newLoc = random.choice(self.triangleLocs)

    # Spawn the new triangle
    self.triangleSpriteGroup.add(Triangle(newLoc, self.level.tileHeight))

  # Remove a captured triangle
  def removeTriangle(self, triangle):
    # Keep up with where this triangle just was
    self.oldTriLoc = triangle.topPoint
    self.triangleSpriteGroup.remove(triangle)
    self.triangle_sound.play()

  # Hand key input
  def handleKeyEvent(self, event):
    # Key pushed down
    if event.type == pygame.KEYDOWN:
      # If we're not paused let McSquare handle the key
      if event.key == pygame.K_LEFT:
        if self.paused:
          self.togglePauseSelection()
        else:
          self.mcSquare.moveLeft()

      # If we're not paused let McSquare handle the key
      elif event.key == pygame.K_RIGHT:
        if self.paused:
          self.togglePauseSelection()
        else:
          self.mcSquare.moveRight()

      # Only McSquare uses the space
      elif event.key == pygame.K_SPACE:
        self.mcSquare.jump()

      # Pause when escape is hit
      elif event.key == pygame.K_ESCAPE:
        self.paused = not self.paused
        self.displayPauseOverlay()

      # Let return handle button pusing in the pause menu
      elif event.key == pygame.K_RETURN:
        if self.paused:
          if self.selectResume:
            self.paused = not self.paused
          elif self.selectQuit:
            self.returnToMain = True

    # Movement keys let go
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        self.mcSquare.stopMoving()

  # Update all the sprites on screen
  def update(self):
    # Update our dynamic sprite and refresh the screen
    self.screen.fill(LIGHT_BLUE)
    self.dynamicSpriteGroup.update()

    # Remove any dead rectangles
    for rectangle in self.rectangleSpriteGroup:
      if rectangle.alive == False:
        rectangle.update()
        self.rectangleSpriteGroup.remove(rectangle)
        rectangle = None

    # See if we need to spawn a new rectangle
    if self.rectangleCounter >= (self.level.rectangleSpawnNumber / self.difficulty):
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

    # Remove any expired powerups
    for powerUp in self.powerUpSpriteGroup:
      if powerUp.expired or powerUp.captured:
        powerUp.update()
        self.powerUpSpriteGroup.remove(powerUp)
        powerUp = None

    # See if we need to spawn a power up
    if self.powerUpCounter >= self.level.powerUpRate:
      # Reset the counter and pick a location to spawn the power up
      self.powerUpCounter = 0
      randomLoc = random.choice(self.powerUpLocs)

      # Spawn a new power up
      powerUp = self.level.spawnNewPowerUp(randomLoc)

      # Add the new power up
      self.powerUpSpriteGroup.add(powerUp)
    else:
      self.powerUpCounter += 1

    # Update the rectangle rain
    if self.pausePowerUp:
      self.pausePowerUpCount += 1
      if self.pausePowerUpCount >= PAUSE_DURATION:
        self.pausePowerUpCount = 0
        self.pausePowerUp = False
    else:
      self.rectangleSpriteGroup.update()

    # Update the platform sprites
    self.platformSpriteGroup.update()

    # Update the triangles
    self.triangleSpriteGroup.update()

    # Update the powerUps
    self.powerUpSpriteGroup.update()

    # Update the HUD
    self.HUD.update()

  # Checks for collisions with rectangles or triangles
  def checkCollisions(self):
    # Check for triangle collisions
    captureCount, powerUpType = self.mcSquare.checkCollisions(self.platforms, self.triangleSpriteGroup, self.powerUpSpriteGroup)

    # If one or more have been capture then increment the score and draw a new one
    if captureCount:
      # Capture the triangle and spawn a new one
      for triangle in self.triangleSpriteGroup:
        if triangle.captured:
          self.removeTriangle(triangle)
          triangle = None

      self.spawnTriangle()

      self.HUD.addPoints(captureCount)

    if powerUpType == 1:
      self.pausePowerUp = True
    elif powerUpType == 2:
      self.HUD.addLife()

    # Check for a hit by the rain
    for rectangle in self.rectangleSpriteGroup:
        hit = rectangle.checkCollisions(self.platforms, self.mcSquare)
        if hit:
          self.hurt_sound.play()
          self.HUD.removeLife()

  def generateGround(self):
    numTiles = SCREEN_WIDTH/GROUND_TILE_WIDTH

    for tileNum in range(0, numTiles):
      groundPiece = Ground(self.screen, (GROUND_TILE_WIDTH*tileNum, (SCREEN_HEIGHT - GROUND_HEIGHT)), (GROUND_TILE_WIDTH, GROUND_HEIGHT))
      self.platformSpriteGroup.add(groundPiece)
      self.platforms.append(groundPiece)

  # Redraws all the current sprites
  def draw(self):
    self.dynamicSpriteGroup.draw(self.screen)
    self.platformSpriteGroup.draw(self.screen)
    self.rectangleSpriteGroup.draw(self.screen)
    self.triangleSpriteGroup.draw(self.screen)
    self.powerUpSpriteGroup.draw(self.screen)

  # Overlay to blur out the game when it is paused
  def displayPauseOverlay(self):
    overlay = Box(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, alpha=128)
    overlay.drawByTopLeft((0,0))

  # Box that shows a bit of help and the option to resume or quit
  def displayPauseInfo(self):
    # Nice sized box centered on the screen
    pauseBoxWidth = SCREEN_WIDTH/2
    pauseBoxHeight = SCREEN_HEIGHT/2
    pauseBoxX = SCREEN_WIDTH/2
    pauseBoxY = SCREEN_HEIGHT/2

    # Box for all the pause menu stuff
    pauseBox = Box(self.screen, pauseBoxWidth, pauseBoxHeight, WHITE)
    pauseBox.drawByCenter((pauseBoxX, pauseBoxY))
    pauseBox.outline(padding=(0,0))

    # Key for all the rectangle types...not proud of the following math

    # Normal
    normalX = pauseBoxX + 20 - (RECTANGLE_WIDTH*2)
    normalY = pauseBoxY - 175
    normalRectangle = NormalRectangleRain((normalX, normalY))
    normalRectangle.draw(self.screen)
    normalLabel = TextLine(self.screen, "Normal", color=BLACK, size=28)
    normalLabel._render()
    normalLabel.drawByTopLeft((normalX - 50 - normalLabel.width, normalY + (RECTANGLE_HEIGHT/2) - 12))

    # Exploding
    explodingX = pauseBoxX + 20
    explodingY = pauseBoxY - 175
    explodingRectangle = ExplodingRectangleRain((explodingX, explodingY))
    explodingRectangle.draw(self.screen)
    explodingLabel = TextLine(self.screen, "Exploding", color=BLACK, size=28)
    explodingLabel.drawByTopLeft((explodingX + 50 + RECTANGLE_WIDTH, explodingY + (RECTANGLE_HEIGHT/2) - 12))

    # Bouncing
    bouncingX = pauseBoxX + 20 - (RECTANGLE_WIDTH*2)
    bouncingY = pauseBoxY - 25
    bouncingRectangle = BounceRectangleRain((bouncingX, bouncingY))
    bouncingRectangle.draw(self.screen)
    bouncingLabel = TextLine(self.screen, "Bouncing", color=BLACK, size=28)
    bouncingLabel._render()
    bouncingLabel.drawByTopLeft((bouncingX - 50 - bouncingLabel.width, bouncingY + (RECTANGLE_HEIGHT/2) - 12))

    # Puddle
    puddleX = pauseBoxX + 20
    puddleY = pauseBoxY - 25
    puddleRectangle = PuddleRectangleRain((puddleX, puddleY))
    puddleRectangle.draw(self.screen)
    puddleLabel = TextLine(self.screen, "Puddle", color=BLACK, size=28)
    puddleLabel.drawByTopLeft((puddleX + 50 + RECTANGLE_WIDTH, puddleY + (RECTANGLE_HEIGHT/2) - 12))

    # Button info
    buttonWidth = pauseBoxWidth/4
    buttonHeight = pauseBoxHeight/8

    # Button to resume play
    resumeButton = Box(self.screen, buttonWidth, buttonHeight, BLACK)
    resumeButton.drawByCenter((pauseBoxX - (pauseBoxWidth/4), pauseBoxY + 150))
    resumeLabel = TextLine(self.screen, "Resume", color=WHITE, size=28)
    resumeLabel.drawByCenter((pauseBoxX - (pauseBoxWidth/4), pauseBoxY + 150))

    # Button to quit back to the main menu
    quitButton = Box(self.screen, buttonWidth, buttonHeight, BLACK)
    quitButton.drawByCenter((pauseBoxX + (pauseBoxWidth/4), pauseBoxY + 150))
    quitLabel = TextLine(self.screen, "Quit", color=WHITE, size=28)
    quitLabel.drawByCenter((pauseBoxX ++ (pauseBoxWidth/4), pauseBoxY + 150))

    # Outline the one that is currently selected
    if self.selectResume == True:
      resumeButton.outline()
    elif self.selectQuit == True:
      quitButton.outline()

  # Toggle which pause button is selected
  def togglePauseSelection(self):
    self.selectResume = not self.selectResume
    self.selectQuit = not self.selectQuit

  # Sets the difficult for the level
  def setDifficulty(self, difficulty):
    self.difficulty = difficulty

  # Get the final score to display at the end of the game
  def getFinalProgress(self):
    return self.HUD.score, self.levelNum

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
      self.screen.fill(LIGHT_BLUE)
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
    self.screen.fill(LIGHT_BLUE)
    currentHelpScreen = 1
    numberOfHelpScreens = 7

    # Constants for the help box
    helpBoxWidth = (SCREEN_WIDTH * 0.75)
    helpBoxHeight = (SCREEN_HEIGHT * 0.60)
    helpBoxLocX = SCREEN_WIDTH/2
    helpBoxLocY = SCREEN_HEIGHT*0.4
    self.helpBoxLoc = helpBoxLocX, helpBoxLocY

    helpLabelLocX = SCREEN_WIDTH/2
    helpLabelLocY = SCREEN_HEIGHT * 0.25
    self.helpLabelLoc = helpLabelLocX, helpLabelLocY

    # Location for page number
    pageNumberLoc = (helpBoxLocX + (helpBoxWidth/2)) - 36, (helpBoxLocY + (helpBoxHeight/2)) - 22

    # Constants for the back button
    backButtonWidth = SCREEN_WIDTH/3
    backButtonHeight = 80
    backButtonLoc = SCREEN_WIDTH/2, SCREEN_HEIGHT*0.85

    prepareTriangleSprites(5)
    preparePowerUpSprites(3)

    # Sprites for various help sheets
    self.mcSquare = Mcsquare(self.screen, self.helpBoxLoc, 150, MCSQUARE_BASE_JUMP_SPEED)
    self.triangle = Triangle((helpBoxLocX - 25, helpBoxLocY), 100)
    self.normalRectangle = NormalRectangleRain((helpBoxLocX - (RECTANGLE_WIDTH/2), helpBoxLocY - 60))
    self.explodingRectangle = ExplodingRectangleRain((helpBoxLocX - (RECTANGLE_WIDTH/2), helpBoxLocY - 60))
    self.bounceRectangle = BounceRectangleRain((helpBoxLocX - (RECTANGLE_WIDTH/2), helpBoxLocY - 60))
    self.puddleRectangle = PuddleRectangleRain((helpBoxLocX - (RECTANGLE_WIDTH/2), helpBoxLocY - 60))
    self.powerUpTime = PowerUp((helpBoxLocX - 170, helpBoxLocY - 150), 100, 1)
    self.powerUpLife = PowerUp((helpBoxLocX - 170, helpBoxLocY), 100, 2)
    self.powerUpShield = PowerUp((helpBoxLocX - 170, helpBoxLocY + 150), 100, 3)

    # Wait until we want to go back
    goBack = False
    while goBack == False:
      self.screen.fill(LIGHT_BLUE)

      # Show the current help screen
      self.showHelpScreen(currentHelpScreen)

      # Draw the help box and label
      helpBox = Box(self.screen, helpBoxWidth, helpBoxHeight, WHITE)
      helpBox.drawByCenter(self.helpBoxLoc)
      helpBox.outline(color=BLACK, padding=(0, 0))

      # Draw the back button
      backBox = Box(self.screen, backButtonWidth, backButtonHeight, BLACK)
      backBox.drawByCenter(backButtonLoc)
      backBox.outline()

      backButtonLabel = TextLine(self.screen, "Back", color=WHITE, size=36)
      backButtonLabel.drawByCenter(backButtonLoc)

      # Show help page number
      pageLabel = TextLine(self.screen, str(currentHelpScreen) + "/" + str(numberOfHelpScreens), color=BLACK, size=18)
      pageLabel = pageLabel.drawByTopLeft(pageNumberLoc)

      # Show the current help content
      self.showHelpScreen(currentHelpScreen)

      event = pygame.event.poll()
      # Key up and down the menu
      if event.type == pygame.KEYDOWN:
        # Enter means we've hit the go back button
        if event.key == pygame.K_RETURN:
          goBack = True
          return Scene.mainMenuScene

        # Go to the next help screen
        elif event.key == pygame.K_RIGHT:
          currentHelpScreen += 1

          if currentHelpScreen > numberOfHelpScreens:
            currentHelpScreen = numberOfHelpScreens

        # Go to the previous help screen
        elif event.key == pygame.K_LEFT:
          currentHelpScreen -= 1

          if currentHelpScreen < 1:
            currentHelpScreen = 1

      pygame.display.flip()
      clock.tick(FRAME_RATE)

  def showHelpScreen(self, currentHelpScreen):
    if currentHelpScreen == 1:
      self.showMcSquareHelp()
    elif currentHelpScreen == 2:
      self.showTriangleHelp()
    elif currentHelpScreen == 3:
      self.showNormalRectangleHelp()
    elif currentHelpScreen == 4:
      self.showExplodingRectangleHelp()
    elif currentHelpScreen == 5:
      self.showBounceRectangleHelp()
    elif currentHelpScreen == 6:
      self.showPuddleRectangleHelp()
    elif currentHelpScreen == 7:
      self.showPowerUpHelp()

  def showMcSquareHelp(self):
    helpBoxX, helpBoxY = self.helpLabelLoc

    # Help text for McSquare
    helpLabel = TextLine(self.screen, "This is Scotty McSquare", color=BLACK, size=36)
    helpLabel.drawByCenter((helpBoxX, helpBoxY - 80))

    # Show McSquare running around
    self.mcSquare.reposition((helpBoxX - (self.mcSquare.width/2), helpBoxY + 60))
    self.mcSquare.animateRunningRight(override=True)
    self.mcSquare.draw(self.screen)


  def showTriangleHelp(self):
    helpBoxX, helpBoxY = self.helpLabelLoc

    # Help text for Triangle
    helpLabel = TextMultiLine(self.screen, "All he wants in life\nare these triangles", color=BLACK, size=36, lineSpacing=45)
    helpLabel.drawByCenter((helpBoxX, helpBoxY - 80))

    # Show triangle hovering (waiting on the sprites)
    self.triangle.animate()
    self.triangle.draw(self.screen)

  def showNormalRectangleHelp(self):
    helpBoxX, helpBoxY = self.helpLabelLoc

    # Help text for normal rectangle
    helpLabel = TextMultiLine(self.screen, "Look out for the evil\nrectangle rain though", color=BLACK, size=36, lineSpacing=45)
    helpLabel.drawByCenter((helpBoxX, helpBoxY - 80))

    # Show rectangle falling (waiting on the sprites)
    self.normalRectangle.helpAnimation()
    self.normalRectangle.draw(self.screen)

  def showExplodingRectangleHelp(self):
    helpBoxX, helpBoxY = self.helpLabelLoc

    # Help text for exploding rectangle
    helpLabel = TextLine(self.screen, "Some rain is a bit explosive", color=BLACK, size=36)
    helpLabel.drawByCenter((helpBoxX, helpBoxY - 80))

    # Show rectangle exploding (waiting on the sprites)
    self.explodingRectangle.helpAnimation()
    self.explodingRectangle.draw(self.screen)

  def showBounceRectangleHelp(self):
    helpBoxX, helpBoxY = self.helpLabelLoc

    # Help text for bouncing rectangle
    helpLabel = TextMultiLine(self.screen, "Some rain likes to go\nboth up and down", color=BLACK, size=36, lineSpacing=45)
    helpLabel.drawByCenter((helpBoxX, helpBoxY - 80))

    # Show rectangle bouncing (waiting on the sprites)
    self.bounceRectangle.helpAnimation()
    self.bounceRectangle.draw(self.screen)

  def showPuddleRectangleHelp(self):
    helpBoxX, helpBoxY = self.helpLabelLoc

    # Help text for puddle rectangle
    helpLabel = TextLine(self.screen, "Some rain leaves a puddle", color=BLACK, size=36)
    helpLabel.drawByCenter((helpBoxX, helpBoxY - 80))

    # Show rectangle puddling (waiting on the sprites)
    self.puddleRectangle.helpAnimation()
    self.puddleRectangle.draw(self.screen)

  def showPowerUpHelp(self):
    helpLabelX, helpLabelY = self.helpLabelLoc
    helpBoxX, helpBoxY = self.helpBoxLoc

    # Help text for puddle rectangle
    helpLabel = TextLine(self.screen, "Collect these to help you power up", color=BLACK, size=36)
    helpLabel.drawByCenter((helpLabelX, helpLabelY - 80))

    helpTimeLabel = TextLine(self.screen, "Pauses the rain", color=BLACK, size=24)
    helpTimeLabel.drawByTopLeft((helpBoxX - 20, helpBoxY - 115))

    helpLifeLabel = TextLine(self.screen, "Gain an extra life", color=BLACK, size=24)
    helpLifeLabel.drawByTopLeft((helpBoxX - 20, helpBoxY + 35))

    helpShieldLabel = TextLine(self.screen, "Invincibility", color=BLACK, size=24)
    helpShieldLabel.drawByTopLeft((helpBoxX - 20, helpBoxY + 185))


    self.powerUpTime.draw(self.screen)
    self.powerUpLife.draw(self.screen)
    self.powerUpShield.draw(self.screen)

class GameOverScene(Scene):
  def __init(self):
    Scene.__init__(self, screen)

  # Show game over screen
  def display(self):
    self.screen.fill(LIGHT_BLUE)

    # Constants to hold the main menu button
    mainMenuButtonWidth = SCREEN_WIDTH/3
    mainMenuButtonHeight = 80

    mainMenuButtonX = SCREEN_WIDTH/2
    mainMenuButtonY = SCREEN_HEIGHT * 0.66

    # Draw the game over text
    endLabel = TextLine(self.screen, "Game Over", color=BLACK, size=SCORE_FONT_SIZE)
    endLabel.drawByCenter(((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.25))

    # Show the final level and score
    levelLabel = TextLine(self.screen, "You made it to level " + str(self.finalLevel), color=BLACK, size=int((SCORE_FONT_SIZE*.75)))
    levelLabel.drawByCenter(((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.4))
    scoreLabel = TextLine(self.screen, "You recieved a score of " + str(self.finalScore), color=BLACK, size=int((SCORE_FONT_SIZE*.75)))
    scoreLabel.drawByCenter(((SCREEN_WIDTH/2), SCREEN_HEIGHT*0.5))

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

  def setFinalProgress(self, score, levelNum):
    self.finalScore = score
    self.finalLevel = levelNum
