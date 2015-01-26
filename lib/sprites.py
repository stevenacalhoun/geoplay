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

# Platform size
PLATFORM_WIDTH = 240
PLATFORM_HEIGHT = 40

# Rectangle size
RECTANGLE_WIDTH = 40
RECTANGLE_HEIGHT = 100
RECTANGLE_SPAWN_RATE = 100

# McSquare class
class Mcsquare(pygame.sprite.Sprite):
  # Arrays to hold all the animations for the left and right running
  runningRightImages = []
  runningLeftImages = []

  # Initializer
  def __init__(self, screen, startingLoc):
    pygame.sprite.Sprite.__init__(self)

    spriteSheet = SpriteSheet("images/braid_man.png")

    # Location for the next image in the sprite sheet
    xVal = 0
    yVal = 0

    # There are 26 images in the sprite sheet, load them all
    for imageCount in range(0, 26):
      # Load each image and add it to the running right images
      image = spriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      self.runningRightImages.append(image)
      imageCount += 1

      # At the end of a row of sprites, go to the next row by adding some arbitrary amound of pixels
      if imageCount % 7 == 0:
        xVal = 0
        yVal += MCSQUARE_HEIGHT + 13
      else:
        xVal += MCSQUARE_WIDTH

    # For the running left images just flipe the right ones
    for image in self.runningRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.runningLeftImages.append(leftImage)


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
    self.falling = True

    self.height = MCSQUARE_HEIGHT

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
          self.yMove = GRAVITY * .1
      # As he's falling increase the amount of gravity until we reach full gravity
      else:
        if self.yMove < GRAVITY:
          self.yMove += GRAVITY * .1
        else:
          self.yMove = GRAVITY

  # Check to see if we've collided with anything
  def checkCollisions(self, platforms, triangles):
    # Check to see if we landed on any platforms
    # self.falling = True
    for platform in platforms:
      if self.rect.colliderect(platform.rect):
        # Moving up
        if self.yMove < 0:
          self.rect.y = platform.rect.y + platform.height
        # Moving down
        if self.yMove > 0:
          self.jumpRecharged = True
          self.rect.y = platform.rect.y - MCSQUARE_HEIGHT
          str(self.rect.y + MCSQUARE_HEIGHT) + "==" + str(platform.rect.y)

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

  def moveLeft(self):
    self.runningLeft = True
    self.xMove = -MCSQUARE_SPEED

  def moveRight(self):
    self.runningRight = True
    self.xMove = MCSQUARE_SPEED

  def stopMoving(self):
    self.runningLeft = False
    self.runningRight = False
    self.xMove = 0

  def jump(self):
    # No double jumping allowed
    if self.jumpRecharged:
      self.jumping = True
      self.yMove = -MCSQUARE_JUMP_SPEED
      self.jumpRecharged = False

  def animate(self):
    # Check if it's time for a new fram and if we are currently running
    if self.frameCount >= 1 and (self.runningRight or self.runningLeft):
      # Select the correct set of images, and display the new frame
      if self.runningLeft:
        self.image = self.runningLeftImages[self.frame]
      elif self.runningRight:
        self.image = self.runningRightImages[self.frame]
      self.frame += 1

      # Final fram reached
      if self.frame == len(self.runningRightImages):
        self.frame = 0
      self.frameCount = 0

    # Increment the frame count if it's not time to change frames
    else:
      self.frameCount += 1

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
  def __init__(self, screen, topPoint, height):
    pygame.sprite.Sprite.__init__(self)

    # Store the triangle's top point
    self.topPoint = topPoint

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

    # Load the triangle and size it based on the input parameters
    self.height = height
    self.width = 2*xOffset
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(WHITE)
    self.image = pygame.image.load("images/triangle.png")
    self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))

    self.rect = pygame.Rect(bX, cY, self.width, self.height)

    self.screen = screen

    self.captured = False

  def update(self):
    # Triangles are currently stationary
    pass
