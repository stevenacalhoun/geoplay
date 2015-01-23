import pygame
import math
from pygame.locals import *
from pygame import Surface
from pygame.locals import *
from constants import *

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

# McSquare class
class Mcsquare(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, screen):
    pygame.sprite.Sprite.__init__(self)

    # Draw a simple black square
    self.image = pygame.Surface((MCSQUARE_WIDTH, MCSQUARE_HEIGHT))
    self.image.fill(BLACK)

    self.screen = screen

    # Start him on the ground in the center of the screen
    self.rect = self.image.get_rect()
    self.rect.x = (SCREEN_WIDTH / 2) - (MCSQUARE_WIDTH / 2)
    self.rect.y = GROUND_Y - MCSQUARE_HEIGHT

    # Start of not moving, jumping, or falling
    self.xMove = 0
    self.yMove = 0
    self.movingRight = False
    self.movingLeft = False
    self.jumping = False
    self.falling = False

  # Update based on the current number of ticks
  def update(self):
    # Move the sprite and plan the next update
    self.move()
    self.checkBounds()

  # Moves McSquare on the screen
  def move(self):
    # Clean up old location
    self.old = self.rect
    blank = pygame.Surface((MCSQUARE_WIDTH, MCSQUARE_HEIGHT))
    blank.fill(WHITE)
    self.screen.blit(blank, self.old)

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
  def checkCollisions(self, platforms, triangle):
    for platform in platforms:
      if self.rect.colliderect(platform.rect):
        # Moving up
        if self.yMove < 0:
          self.rect.y = platform.rect.y + PLATFORM_HEIGHT
        # Moving down
        if self.yMove > 0:
          self.falling = False
          self.rect.y = platform.rect.y - MCSQUARE_HEIGHT

    # Check to see if we've gotten to the triangle
    if self.rect.colliderect(triangle.rect):
      return True

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
  def __init__(self, screen, position):
    pygame.sprite.Sprite.__init__(self)

    # Simple rectangular image
    self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
    self.image.fill(BLACK)

    self.screen = screen

    # Position the platform by the passed in value
    self.rect = self.image.get_rect()
    self.rect.topleft = position

  def update(self):
    pass

# Rectangle rain class
class RectangleRain(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, screen, initialPosition):
    pygame.sprite.Sprite.__init__(self)

    # Draw a simple black rectangle
    self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
    self.image.fill(BLACK)

    self.screen = screen

    self.rect = self.image.get_rect()
    self.rect.topleft = initialPosition

    self.fallingSpeed = GRAVITY * .3

    self.alive = True

  def despawn(self):
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

    # Check collisions with ground
    if self.rect.y + RECTANGLE_HEIGHT >= GROUND_Y:
      self.despawn()

    # Check collisions with McSquare
    if self.rect.colliderect(mcSquare.rect):
      self.despawn()
      return True
    return False


class NormalRectangleRain(RectangleRain):
  ## TO DO ##
  def update(self):
    # Move the sprite and plan the next update
    self.move()

  def move(self):
    # Clean up old location
    self.old = self.rect
    blank = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
    blank.fill(WHITE)
    self.screen.blit(blank, self.old)

    self.rect.y += self.fallingSpeed

    if self.alive == False:
      # Blank out last location
      self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
      self.image.fill(WHITE)

  def animate():
    pass

class BounceUpRectangleRain(RectangleRain):
  ## TO DO ##
  def animate():
    pass

class ExplodingRectangleRain(RectangleRain):
  ## TO DO ##
  def animate():
    pass
class PuddleRectangleRain(RectangleRain):
  ## TO DO ##
  def animate():
    pass

# Triangle class
class Triangle(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, screen, topPoint, height):
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

    self.screen = screen

  # Remove the triangle when it is captured
  def capture(self):
    blank = pygame.Surface((self.width, self.height + 1))
    blank.fill(WHITE)
    self.screen.blit(blank, self.rect)

  def update(self):
    pass
