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

    # Running right images
    self.runningRightImages = getImages("images/sprites-individ/run-right", 8, int(height/26.5))

    # Running left images
    self.runningLeftImages = getImages("images/sprites-individ/run-left", 8, int(height/26.5))

    # Standing right images
    self.standingRightImages = getImages("images/sprites-individ/stand-right", 4, int(height/26.5))

    # Standing left images
    self.standingLeftImages = getImages("images/sprites-individ/stand-left", 4, int(height/26.5))

    # Jumping right images
    fullJumpingRightImages = getImages("images/sprites-individ/jump-right", 6, int(height/26.5))
    self.jumpingRightImages= fullJumpingRightImages[0:2]
    self.fallingRightImages= fullJumpingRightImages[3:6]

    # Jumping left images
    fullJumpingLeftImages = getImages("images/sprites-individ/jump-left", 6, int(height/26.5))
    self.jumpingLeftImages= fullJumpingLeftImages[0:2]
    self.fallingLeftImages= fullJumpingLeftImages[3:6]

    self.image = self.standingLeftImages[0]

    # Keep up with our height for collision detection
    self.width, self.height = self.image.get_rect().size

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

  def animateRunningRight(self, override=False):
    # I had to do this weird override thing so that the help screen could use the animations
    if override == True:
      self.frameCount += 1

    if self.frameCount >= 5:
      # Final fram reached
      if self.frame >= len(self.runningRightImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      self.image = self.runningRightImages[self.frame]
      self.frame += 1
      self.frameCount = 0

  def animateRunningLeft(self, override=False):
    # I had to do this weird override thing so that the help screen could use the animations
    if override == True:
      self.frameCount += 1

    if self.frameCount >= 5:
      # Final fram reached
      if self.frame >= len(self.runningLeftImages):
        self.frame = 0
      self.frameCount = 0

      # Select the correct set of images, and display the new frame
      self.image = self.runningLeftImages[self.frame]
      self.frame += 1
      self.frameCount = 0

  def animateStanding(self, override=False):
    # I had to do this weird override thing so that the help screen could use the animations
    if override == True:
      self.frameCount += 1

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

  def animateJumping(self, override=False):
    # I had to do this weird override thing so that the help screen could use the animations
    if override == True:
      self.frameCount += 1

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

  def animateFalling(self, override=False):
    # I had to do this weird override thing so that the help screen could use the animations
    if override == True:
      self.frameCount += 1

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

  # Animation and movement for the help screen
  def helpAnimation(self):
    # Continuously spawn a falling rectangle
    self.rect.y += self.fallingSpeed * 0.5
    if self.rect.y >= 500:
      self.rect.y = (SCREEN_HEIGHT*0.33) - 60

class BounceRectangleRain(RectangleRain):
  def __init__(self, initialPosition):
    RectangleRain.__init__(self, initialPosition)

    self.bouncingImages = bouncingRectangleImages
    self.image = self.bouncingImages[0]

    # Keep up with the center point
    self.initialPositionX, initailPositionY = initialPosition
    sizeWidth, sizeHeight = self.rect.size
    self.centerX = self.initialPositionX + (sizeWidth/2)

    self.goingBackUp = False
    self.doneAnimating = False
    # self.animate = False

    self.frame = 0
    self.frameCount = 0

    # Flags and counter for help animation
    self.animateBounce = False
    self.waiting = False
    self.waitCount = 0

  def update(self):
    self.move()
    if self.animateBounce:
      self.animate()

  def checkCollisions(self, platforms, mcSquare):
    # Check collisions with platforms
    for platform in platforms:
      if self.rect.colliderect(platform.rect) and self.goingBackUp == False:
        self.fallingSpeed = 0
        self.goingBackUp = True
        self.animateBounce = True

    # Check collisions with McSquare
    if self.rect.colliderect(mcSquare.rect):
      self.despawn()
      return True
    return False

  # Animation and movement for the help screen
  def helpAnimation(self):
    fallingSpeed = GRAVITY * 0.3

    # If we're not waiting or bouncing then move the rectangle
    if self.animateBounce == False and self.waiting == False:
      if self.goingBackUp == False:
        self.rect.y += fallingSpeed * 0.5
      else:
        self.rect.y -= fallingSpeed * 0.5

      # If we hit the bottom then bounce back up
      if self.rect.y >= 500:
        self.goingBackUp = True
        self.animateBounce = True

      # If we hit the top then stop moving up and wait a bit
      if self.rect.y <= ((SCREEN_HEIGHT*0.4)  - 60):
        self.goingBackUp = False
        self.waiting = True

    # Start animating if we're at the bottom, flag that we're finished animating when the animation is done
    elif self.doneAnimating == False and self.waiting == False:
      self.animate()
      if self.doneAnimating == True:
        self.doneAnimating = False
        self.rect.y -= 7
        self.goingBackUp = True

    # Wait at the top for a bit before starting again
    else:
      self.waitCount += 1
      if self.waitCount >= 50:
        self.waiting = False
        self.waitCount = 0


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
    if self.frameCount >= 2:
      self.frameCount = 0

      # Final frame reached
      if self.frame >= len(self.bouncingImages):
        self.doneAnimating = True
        self.fallingSpeed = (-1 * GRAVITY * .3)
        self.frame = 0
        self.image = self.bouncingImages[self.frame]
        self.animateBounce = False

      else:
        # Keep up with how big we just were
        prevSizeWidth, prevSizeHeight = self.image.get_rect().size

        # Change to the next frame
        self.image = self.bouncingImages[self.frame]

        # Change how big the collision box is
        tempRect = self.image.get_rect()
        self.rect.size = tempRect.size

        # Reposition the rectangle to offse the new size
        newSizeWidth, newSizeHeight = tempRect.size
        heightDifference = prevSizeHeight - newSizeHeight
        self.rect.x = self.centerX - (newSizeWidth/2)
        self.rect.y = self.rect.y + heightDifference

        self.frame += 1

class ExplodingRectangleRain(RectangleRain):
  def __init__(self, initialPosition):
    RectangleRain.__init__(self, initialPosition)

    # Set the animation images
    self.explodingImages = explodingRectangleImages
    self.image = self.explodingImages[0]

    # Keep up with the center point
    self.initialPositionX, initailPositionY = initialPosition
    sizeWidth, sizeHeight = self.rect.size
    self.centerX = self.initialPositionX + (sizeWidth/2)

    # Control the animation
    self.frame = 0
    self.frameCount = 0

    # Startes of the animation
    self.exploding = False
    self.exploded = False
    self.animateExplosion = False

    # Flags and counter for help animation
    self.doneAnimating = False

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
    if self.rect.y > SCREEN_HEIGHT or self.exploded:
      self.despawn()

  def animate(self):
    self.frameCount += 1
    if self.frameCount >= 3:
      self.frameCount = 0

      # Final fram reached
      if self.frame >= len(self.explodingImages):
        self.exploded = True
        self.doneAnimating = True

      else:
        # Keep up with how big we just were
        prevSizeWidth, prevSizeHeight = self.image.get_rect().size

        # Change to the next frame
        self.image = self.explodingImages[self.frame]

        # Change how big the collision box is
        tempRect = self.image.get_rect()
        self.rect.size = tempRect.size

        # Reposition the rectangle to offse the new size
        newSizeWidth, newSizeHeight = tempRect.size
        heightDifference = prevSizeHeight - newSizeHeight
        self.rect.x = self.centerX - (newSizeWidth/2)
        self.rect.y = self.rect.y + heightDifference

        self.frame += 1

  # Animation and movement for the help screen
  def helpAnimation(self):
    fallingSpeed = GRAVITY * 0.3

    # If we're not waiting or exploding then move the rectangle
    if self.animateExplosion == False:
      self.rect.y += fallingSpeed * 0.5

      # If we hit the bottom then start exploding
      if self.rect.y >= 500:
        self.animateExplosion = True

    #Start animating at the bottom, move the rectangle to the top when it's done exploding
    elif self.doneAnimating == False:
      self.animate()
      if self.doneAnimating == True:
        self.animateExplosion = False
        self.doneAnimating = False
        self.rect.x = self.initialPositionX
        self.rect.y = (SCREEN_HEIGHT*0.33) - 60
        self.image = self.explodingImages[0]
        self.frame = 0

class PuddleRectangleRain(RectangleRain):
  def __init__(self, initialPosition):
    RectangleRain.__init__(self, initialPosition)

    self.puddleImages = puddleRectangleImages
    self.image = self.puddleImages[0]

    self.puddling = False
    self.puddled = False
    self.puddleCount = 0

    # Keep up with the center point
    self.initialPositionX, initailPositionY = initialPosition
    sizeWidth, sizeHeight = self.rect.size
    self.centerX = self.initialPositionX + (sizeWidth/2)

    self.frame = 0
    self.frameCount = 0

    # Flags and counters to help keep up with the help animation
    self.doneAnimating = False
    self.animatePuddle = False

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
    if self.frameCount >= 3:
      self.frameCount = 0

      # Final fram reached
      if self.frame >= len(self.puddleImages):
        self.puddled = True
        self.doneAnimating = True

      else:
        # Keep up with how big we just were
        prevSizeWidth, prevSizeHeight = self.image.get_rect().size

        # Change to the next frame
        self.image = self.puddleImages[self.frame]

        # Change how big the collision box is
        tempRect = self.image.get_rect()
        self.rect.size = tempRect.size

        # Reposition the rectangle to offse the new size
        newSizeWidth, newSizeHeight = tempRect.size
        heightDifference = prevSizeHeight - newSizeHeight
        self.rect.x = self.centerX - (newSizeWidth/2)
        self.rect.y = self.rect.y + heightDifference

        self.frame += 1

  def helpAnimation(self):
    fallingSpeed = GRAVITY * 0.3

    # If we're not puddling, continue falling
    if self.animatePuddle == False and self.puddled == False:
      self.rect.y += fallingSpeed * 0.5

      if self.rect.y >= 500:
        self.animatePuddle = True

    # At the bottom starting puddling
    if self.animatePuddle:
      self.animate()
      if self.doneAnimating == True:
        self.animatePuddle = False
        self.doneAnimating = False
        self.frame = 0
        self.puddled = True

    # After animating wait a bit before starting again
    if self.puddled:
      self.puddleCount += 1

      if self.puddleCount >= 100:
        self.puddleCount = 1
        self.rect.x = self.initialPositionX
        self.rect.y = (SCREEN_HEIGHT*0.33) - 60
        self.image = self.puddleImages[self.frame]
        self.puddled = False

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
    self.image = self.hoverImages[0]
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
    if self.frameCount >= 1:
      self.frameCount = 0

      # Final fram reached
      if self.frame >= len(self.hoverImages):
        self.frame = 0

      # Change to the next frame
      self.image = self.hoverImages[self.frame]
      self.frame += 1

  def reposition(self, newTopPoint):
    self.topPoint = newTopPoint
    self.findTriangleInfo()
    self.rect.topleft = (self.points[1][0], self.points[2][1])


def prepareSprites():
  global powerUpImages, normalRectangleImages, explodingRectangleImages, bouncingRectangleImages, puddleRectangleImages

  # Exploding Rectangle
  explodingRectangleImages = getImages("images/sprites-individ/rect-blue", 7, 3)

  # Bouncing Rectangle
  bouncingRectangleImages = getImages("images/sprites-individ/rect-purple", 8, 3)

  # Puddle Rectangle
  puddleRectangleImages = getImages("images/sprites-individ/rect-green", 6, 3)

  # Power up
  powerUpImages = getImages("images/sprites-individ/hexagon", 4, 2)

def prepareTriangleSprites(scale):
  global triangleImages

  # Triangle
  triangleImages = getImages("images/sprites-individ/triangle", 5, scale)


def getImages(baseName, totalImages, scaleFactor):
  images = []

  for imageNum in range (1, totalImages+1):
    rawImage = pygame.image.load(baseName + str(imageNum) + ".png").convert()
    rawImageWidth, rawImageHeight = rawImage.get_rect().size


    rawImage = pygame.transform.scale(rawImage, (rawImageWidth*scaleFactor, rawImageHeight*scaleFactor))

    image = rawImage

    transColor = image.get_at((0,0))
    image.set_colorkey(transColor)
    images.append(image)

  return images
