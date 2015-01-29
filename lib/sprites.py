import pygame
import math
from pygame.locals import *
from pygame import Surface
from pygame.locals import *
from constants import *
from spriteSheets import *
import time

# McSquare size
MCSQUARE_HEIGHT = 53
MCSQUARE_WIDTH = 50
MCSQUARE_SPEED = 15
MCSQUARE_BASE_JUMP_SPEED = 30.0

# Rectangle size
RECTANGLE_WIDTH = 40
RECTANGLE_HEIGHT = 100

triangleImages = []
powerUpImages = []
normalRectangleImages = []
explodingRectangleImages =[]
bouncingRectangleImages = []
puddleRectangleImages = []

# McSquare class
class Mcsquare(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, screen, startingLoc, height, jumpSpeed):
    pygame.sprite.Sprite.__init__(self)

    # Sprite sheet for McSquare
    spriteSheet = SpriteSheet("images/spritesheet.png")

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
    xVal = 15
    yVal = 160

    # There are 26 images in the sprite sheet, load them all
    for imageCount in range(0, 8):
      # Load each image, scale them, and add it to the running right images
      rawImage = spriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height), int(self.height)))
      self.runningRightImages.append(image)
      xVal += MCSQUARE_WIDTH + 12

    # For the running left images just flip the right ones
    for image in self.runningRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.runningLeftImages.append(leftImage)

    # Standing left images
    xVal = 986
    yVal = 190
    for imageCount in range(0, 3):
      rawImage = spriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height), int(self.height)))
      self.standingRightImages.append(image)

      xVal += MCSQUARE_WIDTH + 7

    # Standing left images
    for image in self.standingRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.standingLeftImages.append(leftImage)

    # Jumping right images
    xVal = 575
    yVal = 200
    for imageCount in range(0, 3):
      rawImage = spriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height), int(self.height)))
      self.jumpingRightImages.append(image)

      xVal += MCSQUARE_WIDTH + 7
      yVal -= 9 + imageCount*9

    # Jumping left images
    for image in self.jumpingRightImages:
      leftImage = pygame.transform.flip(image, True, False)
      self.jumpingLeftImages.append(leftImage)

    # Falling right images
    xVal = 750
    yVal = 170
    for imageCount in range(0, 3):
      rawImage = spriteSheet.get_image(xVal, yVal, MCSQUARE_WIDTH, MCSQUARE_HEIGHT)
      image = pygame.transform.scale(rawImage, (int(self.height), int(self.height)))
      self.fallingRightImages.append(image)

      xVal += MCSQUARE_WIDTH + 7
      yVal += 9 + imageCount*9

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

    # Start facing left
    self.facingRight = False
    self.facingLeft = True

    # Adjusted jump speed based on the size of the level
    self.jumpSpeed = jumpSpeed

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
        self.yMove += self.jumpSpeed * .04
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
      self.yMove = -self.jumpSpeed
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
    if self.frameCount >= 2:
      # Final fram reached
      if self.frame >= len(self.runningRightImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      self.image = self.runningRightImages[self.frame]
      self.frame += 1
      self.frameCount = 0

  def animateRunningLeft(self):
    if self.frameCount >= 2:
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

  def reposition(self, newLoc):
    self.rect.topleft = newLoc

class NormalRectangleRain(RectangleRain):
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

  def update(self):
    # Move the sprite and plan the next update
    self.move()

  def move(self):
    self.rect.y += self.fallingSpeed

    if self.alive == False:
      # Blank out last location
      self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
      self.image.fill(WHITE)

    # If it somehow gets off screen then despawn it
    if self.rect.y > SCREEN_HEIGHT:
      self.despawn()

  def animate():
    # No animation for this type of rain currently
    pass

class BounceRectangleRain(RectangleRain):
  def __init__(self, initialPosition):
    RectangleRain.__init__(self, initialPosition)

    self.bouncingImages = bouncingRectangleImages

    self.goingBackUp = False
    self.doneAnimating = False

    self.frame = 0
    self.frameCount = 0

  def update(self):
    self.move()
    if self.goingBackUp:
      self.animate()

  def checkCollisions(self, platforms, mcSquare):
    # Check collisions with platforms
    for platform in platforms:
      if self.rect.colliderect(platform.rect) and self.goingBackUp == False:
        self.fallingSpeed = 0
        self.goingBackUp = True

    # Check collisions with McSquare
    if self.rect.colliderect(mcSquare.rect):
      self.despawn()
      return True
    return False


  def move(self):
    self.rect.y += self.fallingSpeed

    if self.goingBackUp:
      if self.rect.y <= HUD_HEIGHT:
        self.despawn()

    if self.alive == False:
      # Blank out last location
      self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
      self.image.fill(WHITE)

    # If it somehow gets off screen then despawn it
    if self.rect.y > SCREEN_HEIGHT:
      self.despawn()

  def animate(self):
    self.frameCount += 1
    if self.frameCount >= 5:
      self.frameCount = 0

      # Final fram reached
      if self.frame >= len(self.bouncingImages):
        self.doneAnimating = True
        self.fallingSpeed = (-1 * GRAVITY * .3)

      # Change to the next frame
      # self.image = self.bouncingRectangleImages[self.frame]
      self.frame += 1


class ExplodingRectangleRain(RectangleRain):
  def __init__(self, initialPosition):
    RectangleRain.__init__(self, initialPosition)

    self.explodingImages = explodingRectangleImages

    self.frame = 0
    self.frameCount = 0

    self.exploding = False

  def update(self):
    self.move()
    if self.exploding:
      self.animate()

  def checkCollisions(self, platforms, mcSquare):
    # Check collisions with platforms
    for platform in platforms:
      if self.rect.colliderect(platform.rect):
        self.fallingSpeed = 0
        self.exploding = True

    # Check collisions with McSquare
    if self.rect.colliderect(mcSquare.rect):
      self.despawn()
      return True
    return False

  def move(self):
    self.rect.y += self.fallingSpeed

    if self.alive == False:
      # Blank out last location
      self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
      self.image.fill(WHITE)

    # If it somehow gets off screen then despawn it
    if self.rect.y > SCREEN_HEIGHT:
      self.despawn()

  def animate(self):
    self.frameCount += 1
    if self.frameCount >= 5:
      self.frameCount = 0

      # Final fram reached
      if self.frame >= len(self.explodingImages):
        self.despawn()

      # Change to the next frame
      # self.image = self.explodingRectangleImages[self.frame]
      self.frame += 1


class PuddleRectangleRain(RectangleRain):
  def __init__(self, initialPosition):
    RectangleRain.__init__(self, initialPosition)

    self.puddleImages = puddleRectangleImages

    self.puddling = False
    self.puddled = False
    self.puddleCount = 0

    self.frame = 0
    self.frameCount = 0

  def update(self):
    self.move()
    if self.puddling:
      self.animate()

    if self.puddled:
      self.puddleCount += 1

      if self.puddleCount >= 100:
        self.despawn()

    # If it somehow gets off screen then despawn it
    if self.rect.y > SCREEN_HEIGHT:
      self.despawn()

  def checkCollisions(self, platforms, mcSquare):
    # Check collisions with platforms
    for platform in platforms:
      if self.rect.colliderect(platform.rect):
        self.fallingSpeed = 0
        self.puddling = True

    # Check collisions with McSquare
    if self.rect.colliderect(mcSquare.rect):
      self.despawn()
      return True
    return False

  def move(self):
    self.rect.y += self.fallingSpeed

    if self.alive == False:
      # Blank out last location
      self.image = pygame.Surface((RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
      self.image.fill(WHITE)

  def animate(self):
    self.frameCount += 1
    if self.frameCount >= 5:
      self.frameCount = 0

      # Final fram reached
      if self.frame >= len(self.puddleImages):
        self.puddled = True

      # Change to the next frame
      # self.image = self.puddleRectangleImages[self.frame]
      self.frame += 1


# Triangle class
class Triangle(pygame.sprite.Sprite):
  # Initializer
  def __init__(self, topPoint, height):
    pygame.sprite.Sprite.__init__(self)

    # Store the triangle's top point
    self.topPoint = topPoint
    self.height = height

    self.findTriangleInfo()

    self.hoverImages = triangleImages
    self.frameCount = 0
    self.frame = 0

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
    self.animate()

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

  def animate(self):
    self.frameCount += 1
    if self.frameCount >= 5:
      self.frameCount = 0

      # Final fram reached
      if self.frame >= len(self.hoverImages):
        self.frame = 0

      # Change to the next frame
      # self.image = self.hoverImages[self.frame]
      self.frame += 1

  def reposition(self, newTopPoint):
    self.topPoint = newTopPoint
    self.findTriangleInfo()
    self.rect.topleft = (self.points[1][0], self.points[2][1])


def prepareSprites():
  global triangleImages, powerUpImages, normalRectangleImages, explodingRectangleImages, bouncingRectangleImages, puddleRectangleImages

  # Exploding Rectangle
  # explodingRectangleImages = getImages("explodingRectangle", 7)

  # Bouncing Rectangle
  # bouncingRectangleImages = getImages("bouncingRectangle", 9)

  # Puddle Rectangle
  # puddleRectangleImages = getImages("puddleRectangle", 6)

  # Triangle
  # triangleImages = getImages("triangle", 5)

  # Power up
  # powerUpImages = getImages("powerUp", 5)

def getImages(baseName, totalImages):
  images = []

  for imageNum in range (1, totalImages):
    image = pygame.image.load(baseName + str(totalImages)).convert()
    images.append(image)

  return images
