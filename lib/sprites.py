import pygame
import math
from pygame.locals import *
from pygame import Surface
from pygame.locals import *
from constants import *
from spriteSheets import *
import time

# McSquare size
MCSQUARE_HEIGHT = 140
MCSQUARE_WIDTH = 130
MCSQUARE_SPEED = 15
MCSQUARE_JUMP_SPEED = 30

# Rectangle size
RECTANGLE_WIDTH = 40
RECTANGLE_HEIGHT = 100



# McSquare class
class Mcsquare(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, screen, startingLoc, height):
    pygame.sprite.Sprite.__init__(self)

    # Sprite sheet for McSquare
    spriteSheet = SpriteSheet("images/braid_man.png")
    
    # McSquare sounds
    self.jump_sound = pygame.mixer.Sound("sounds/Bump.ogg")
    self.hurt_sound = pygame.mixer.Sound("sounds/Bump.ogg")
    self.land_sound = pygame.mixer.Sound("sounds/Bump.ogg")

    # Keep up with our height for collision detection
    self.height = height
    self.width = height

    # Arrays to hold all the animations
    self.runningRightImages = []
    self.runningLeftImages = []

    self.standingRightImages = []
    self.standingLeftImages = []

    self.jumpingRightImages = []
    self.jumpingLeftImages = []

    self.fallingRightImages = []
    self.fallingLeftImages = []

    # Location for the next image in the sprite sheet
    xVal = 0
    yVal = 0

    # There are 26 images in the sprite sheet, load them all
    for imageCount in range(0, 26):
      # Load each image, scale them, and add it to the running right images
      rawImage = spriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height), int(self.height)))
      self.runningRightImages.append(image)
      imageCount += 1

      # At the end of a row of sprites, go to the next row by adding some arbitrary amound of pixels
      if imageCount % 7 == 0:
        xVal = 0
        yVal += MCSQUARE_HEIGHT + 13
      else:
        xVal += MCSQUARE_WIDTH

    # For the running left images just flip the right ones
    for image in self.runningRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.runningLeftImages.append(leftImage)

    otherSpriteSheet = SpriteSheet("images/tim_animations.png")

    # Standing left images
    xVal = 615
    yVal = 1205
    for imageCount in range(0, 9):
      rawImage = otherSpriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH - 30, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height - 30), int(self.height)))
      self.standingRightImages.append(image)
      imageCount += 1

      xVal += MCSQUARE_WIDTH - 30

    # Standing left images
    for image in self.standingRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.standingLeftImages.append(leftImage)

    # Jumping right images
    xVal = 42
    yVal = 870
    for imageCount in range(0, 3):
      rawImage = otherSpriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height - 30), int(self.height)))
      self.jumpingRightImages.append(image)
      imageCount += 1

    # Jumping left images
    for image in self.jumpingRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.jumpingLeftImages.append(leftImage)

    # Falling right images
    xVal = 1655
    yVal = 875
    for imageCount in range(0, 3):
      rawImage = otherSpriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height - 30), int(self.height)))
      self.fallingRightImages.append(image)
      imageCount += 1

    # Falling left images
    for image in self.fallingRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.fallingLeftImages.append(leftImage)

    self.image = image
    self.screen = screen

    # Start him on the ground in the center of the screen
    self.rect = self.image.get_rect()
    self.rect.topleft = startingLoc

    # Start of not moving, jumping, or falling
    self.xMove = 0
    self.yMove = GRAVITY
    self.runningRight = False
    self.runningLeft = False
    self.jumping = False
    self.jumpRecharged = True
    self.falling = False

    self.facingRight = False
    self.facingLeft = True

    # Count frames to make the animation look smooth
    self.frame = 0
    self.frameCount = 0

  # Update based on the current number of ticks
  def update(self):
    # Move the sprite, check bounds, and animate
    self.move()
    self.checkBounds()
    self.animate()

  # Moves McSquare on the screen
  def move(self):
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
          self.jumping = False
          self.falling = True
          self.yMove = GRAVITY * .1
      # As he's falling increase the amount of gravity until we reach full gravity
      else:
        if self.yMove < GRAVITY:
          self.yMove += GRAVITY * .1
        else:
          self.yMove = GRAVITY

  def draw(self, screen):
    screen.blit(self.image, self.rect.topleft)

  # Check to see if we've collided with anything
  def checkCollisions(self, platforms, triangles):
    # Check to see if we landed on any platforms
    # self.falling = True
    for platform in platforms:
      if self.rect.colliderect(platform.rect):
        # Moving up
        if self.yMove < 0:
          self.rect.y = platform.rect.y + platform.height

          # We've bumped our head, so immediately start moving downwards
          self.yMove = 1

        # Moving down
        elif self.yMove > 0:
          self.jumpRecharged = True
          self.falling = False
          self.rect.y = platform.rect.y - self.height


        ###########################################################################
        # Bunch of failed attempts to make collisions work better
        ###########################################################################

        # feetY = self.rect.y + self.height
        # headY = self.rect.y
        #
        # leftSide = self.rect.x
        # rightSide = self.rect.x + self.width
        #
        # platformTop = platform.rect.y
        # platformBottom = platform.rect.y + platform.height
        #
        # platformRight = platform.rect.x
        # platformLeft = platform.rect.x + platform.width
        #
        # bumpedHead = False
        #
        # # This means we are not above the platform, so we might be hitting the sides
        # if (feetY-15 > platformTop) and (headY < platformBottom) and bumpedHead == False:
        #   # self.rect.y = oldY
        #   # Moving left
        #   if self.xMove < 0:
        #     self.rect.x = platform.rect.x + platform.width
        #
        #   # Moving right
        #   elif self.xMove > 0:
        #     self.rect.x = platform.rect.x - self.width
        #
        # # Moving up
        # elif self.yMove < 0:
        #   oldY = self.rect.y
        #   self.rect.y = platform.rect.y + platform.height
        #
        #   # We've bumped our head, so immediately start moving downwards
        #   self.yMove = 1
        #   bumpedHead = True
        #
        # # Moving down
        # elif self.yMove > 0:
        #   self.jumpRecharged = True
        #   oldY = self.rect.y
        #   self.rect.y = platform.rect.y - self.height
        #
        ###########################################################################
        # Keeping them here in case I want to revisit this issue
        ###########################################################################


    # Check to see if we've gotten to the triangle
    captureCount = 0
    for triangle in triangles:
      if self.rect.colliderect(triangle.rect):
        captureCount += 1
        triangle.captured = True
    return captureCount

  # Just to make sure we haven't crossed any bounds
  def checkBounds(self):
    # Left side
    if (self.rect.x < 0):
      self.rect.x = 0
    # Right side
    if (self.rect.x > SCREEN_WIDTH - MCSQUARE_WIDTH):
      self.rect.x = SCREEN_WIDTH - MCSQUARE_WIDTH
    # Ceiling
    if (self.rect.y < HUD_HEIGHT):
      self.rect.y = HUD_HEIGHT + 1

      # We've bumped our head, so immediately start moving downwards
      self.yMove = 1

  def moveLeft(self):
    self.runningLeft = True
    self.xMove = -MCSQUARE_SPEED
    self.facingRight = False
    self.facingLeft = True

  def moveRight(self):
    self.runningRight = True
    self.xMove = MCSQUARE_SPEED
    self.facingRight = True
    self.facingLeft = False

  def stopMoving(self):
    self.runningLeft = False
    self.runningRight = False
    self.xMove = 0

  def jump(self):
    # No double jumping allowed
    if self.jumpRecharged:
      self.jumping = True
      self.jump_sound.play() # Test sound code
      self.yMove = -MCSQUARE_JUMP_SPEED
      self.jumpRecharged = False

  def animate(self):
    # Select the correct set of images, and display the new frame
    if self.jumping:
      self.animateJumping()
    elif self.falling:
      self.animateFalling()
    elif self.runningLeft:
      self.animateRunningLeft()
    elif self.runningRight:
      self.animateRunningRight()
    else:
      self.animateStanding()

    # Increment the frame count if it's not time to change frames
    self.frameCount += 1

  def animateRunningRight(self):
    if self.frameCount >= 1:
      # Final fram reached
      if self.frame >= len(self.runningRightImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      self.image = self.runningRightImages[self.frame]
      self.frame += 1
      self.frameCount = 0

  def animateRunningLeft(self):
    if self.frameCount >= 1:
      # Final fram reached
      if self.frame >= len(self.runningLeftImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      self.image = self.runningLeftImages[self.frame]
      self.frame += 1
      self.frameCount = 0

  def animateStanding(self):
    if self.frameCount >= 5:
      # Final fram reached
      if self.frame >= len(self.standingRightImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      if self.facingLeft == True:
        self.image = self.standingLeftImages[self.frame]
      else:
        self.image = self.standingRightImages[self.frame]

      self.frame += 1
      self.frameCount = 0

  def animateJumping(self):
    if self.frameCount >= 5:
      # Final fram reached
      if self.frame >= len(self.jumpingRightImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      if self.facingLeft == True:
        self.image = self.jumpingLeftImages[self.frame]
      else:
        self.image = self.jumpingRightImages[self.frame]
      self.frame += 1
      self.frameCount = 0

  def animateFalling(self):
    if self.frameCount >= 5:
      # Final fram reached
      if self.frame >= len(self.fallingRightImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      if self.facingLeft == True:
        self.image = self.fallingLeftImages[self.frame]
      else:
        self.image = self.fallingRightImages[self.frame]
      self.frame += 1
      self.frameCount = 0


  def reposition(self, newLoc):
    self.rect.topleft = newLoc


# Platform class
class Platform(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, screen, position, size):
    pygame.sprite.Sprite.__init__(self)

    self.width, self.height = size

    # Simple rectangular image
    self.image = pygame.Surface(size)
    self.image.fill(BLACK)

    self.screen = screen

    # Position the platform by the passed in value
    self.rect = self.image.get_rect()
    self.rect.topleft = position

  def update(self):
    # Platforms are currently stationary
    pass

# Rectangle rain class
class RectangleRain(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, initialPosition):
    pygame.sprite.Sprite.__init__(self)

    # Draw a simple black rectangle
    self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
    self.image.fill(BLACK)

    self.rect = self.image.get_rect()
    self.rect.topleft = initialPosition

    # Set it to fall and make it alive
    self.fallingSpeed = GRAVITY * .3
    self.alive = True

  def draw(self, screen):
    screen.blit(self.image, self.rect.topleft)

  def despawn(self):
    # Stop the rectangle and set it to being dead
    self.fallingSpeed = 0
    self.alive = False

    # Blank out last location
    blank = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
    blank.fill(WHITE)
    self.image = blank

  def checkCollisions(self, platforms, mcSquare):
    # Check collisions with platforms
    for platform in platforms:
      if self.rect.colliderect(platform.rect):
        self.despawn()

    # Check collisions with McSquare
    if self.rect.colliderect(mcSquare.rect):
      self.despawn()
      return True
    return False

  def reposition(self, newLoc):
    self.rect.topleft = newLoc

class NormalRectangleRain(RectangleRain):
  def update(self):
    # Move the sprite and plan the next update
    self.move()

  def move(self):
    self.rect.y += self.fallingSpeed

    if self.alive == False:
      # Blank out last location
      self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
      self.image.fill(WHITE)

  def animate():
    # No animation for this type of rain currently
    pass

class BounceRectangleRain(RectangleRain):
  ## TO DO ##
  def update(self):
    pass

  def move(self):
    pass

  def animate():
    pass

class ExplodingRectangleRain(RectangleRain):
  ## TO DO ##
  def update(self):
    pass

  def move(self):
    pass

  def animate():
    pass

class PuddleRectangleRain(RectangleRain):
  ## TO DO ##
  def update(self):
    pass

  def move(self):
    pass

  def animate():
    pass

# Triangle class
class Triangle(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, topPoint, height):
    pygame.sprite.Sprite.__init__(self)

    # Store the triangle's top point
    self.topPoint = topPoint
    self.height = height

    self.findTriangleInfo()

    # Load the triangle image and transform it to the desired size
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(WHITE)
    self.image = pygame.image.load("images/triangle.png")
    self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))

    # The rectangle is for collision detection, really should be a triangle
    self.rect = pygame.Rect(self.points[1][0], self.points[2][1], self.width, self.height)

    # Currently not captured
    self.captured = False

  def update(self):
    # Triangles are currently stationary
    pass

  def draw(self, screen):
    screen.blit(self.image, self.rect.topleft)

  def findTriangleInfo(self):
    # C point is simply the passed in topPoint
    cX, cY = self.topPoint

    # Find the x offset for the other two points
    xOffset = self.height * math.tan(math.radians(30))

    # bY is simply cY minus the height, and bX is cX minus the offset
    bX = cX - xOffset
    bY = cY + self.height

    # aY is simply cY minus the height, and aX is cX plus the offset
    aX = cX + xOffset
    aY = cY + self.height

    self.points = [[aX, aY], [bX, bY], [cX, cY]]

    # Load the triangle and size it based on the input parameters
    self.width = 2*xOffset

  def animateHover(self):
    pass

  def reposition(self, newTopPoint):
    self.topPoint = newTopPoint
    self.findTriangleInfo()
    self.rect.topleft = (self.points[1][0], self.points[2][1])
