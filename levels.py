import pygame
import math
import random
from constants import *
import scenes
from sprites import *

def getLevel(level):
  if level == 1:
    return Level_01()
  elif level == 2:
    return Level_02()
  elif level == 3:
    return Level_03()
  elif level == 4:
    return Level_04()
  elif level == 5:
    return Level_05()
  elif level == 6:
    return Level_06()
  elif level == 7:
    return Level_07()
  elif level == 8:
    return Level_08()
  elif level == 9:
    return Level_09()
  elif level == 10:
    return Level_10()


class Level(object):
  def __init__(self, requiredScore=10, rectangleSpawnNumber=100, normalRainChance=1, bounceRainChance=0, explodingRainChance=0, puddleRainChance=0):
    # An array to help generate a random rectangle type
    self.rectangleChoices = []

    # Recquire score to complete the level
    self.requiredScore = requiredScore

    # Keep up with how often to spawn rectangles
    self.rectangleSpawnNumber = rectangleSpawnNumber

    # Hold all the different chances to spawn each type of rectangle rain
    self.normalRainChance = normalRainChance
    self.bounceRainChance = bounceRainChance
    self.explodingRainChance = explodingRainChance
    self.puddleRainChance = puddleRainChance

    # Create the rectangle choice array
    self.createRectangleChoiceHolder()

  def generateLevel(self):
    # Keep track of our platforms and triangles
    platformLocs = []
    triangleLocs = []

    # Get our total number of rows and columns
    numRows = len(self.levelTiles)
    numColumns = self.countColumns()

    # Scale the triangle and powerup sprites based on the size of the level
    prepareTriangleSprites(int(30/numRows))
    preparePowerUpSprites(int(30/numRows))

    # Tile width and height based on the number of columns and rows
    self.tileWidth = SCREEN_WIDTH/numColumns
    self.tileHeight = (SCREEN_HEIGHT-HUD_HEIGHT)/numRows

    # Since the tileHeight is a rounded down integer then it leaves this weird gap at the bottom
    self.bottomGap = SCREEN_HEIGHT - (HUD_HEIGHT + (numRows*self.tileHeight))

    # Adjust the jumpspeed for McSquare based on the size of the level
    self.jumpSpeed = MCSQUARE_BASE_JUMP_SPEED * (15.0/numRows)

    # Current x,y coordinate for the current tile
    currentXLoc = 0
    currentYLoc = HUD_HEIGHT

    # Stuff to keep track of building platforms
    buildingPlatform = False
    platformWidth = 0
    platformLoc = 0

    # Walk over every row in the level
    for rowNum, row in enumerate(self.levelTiles):
      # Walk over every tile in the row
      for tileNum, tile in enumerate(row):
        # T stands for a triangle spawn location
        if tile == "T":
          # Search for either a 't' or a '_'
          currentSearch = 1
          stillSearching = True
          while stillSearching:
            # If there is a t that means position it between the two tiles
            if row[tileNum+currentSearch] == "t":
              triangleLoc = ((currentXLoc + self.tileWidth), currentYLoc)
              triangleLocs.append(triangleLoc)
              stillSearching = False

            # Otherwise just position it in the middle of the tile
            elif row[tileNum+currentSearch] == "_":
              triangleLoc = ((currentXLoc + (self.tileWidth/2)), (currentYLoc))
              triangleLocs.append(triangleLoc)
              stillSearching = False

            # Still looking for it
            else:
              currentSearch += 1

        # P stands for platform
        if tile == "P":
          # If we are currently building a platform, create it
          if buildingPlatform:
            platformLocs.append([platformLoc, (platformWidth, tileHeight)])

          # Start a new platform
          buildingPlatform = True
          platformLoc = currentXLoc, currentYLoc
          platformWidth = self.tileWidth

        # p stands for a growing platform
        elif tile == "p":
          platformWidth += self.tileWidth

        # S stands for the starting point for McSquare
        elif tile == "S":
          startingLoc = currentXLoc, currentYLoc

        # There is nothing on this tile
        elif tile == "_":
          # If we are building a platform, this means we've finished it, so build it
          if buildingPlatform:
            platformLocs.append([platformLoc, (platformWidth, self.tileHeight)])
            buildingPlatform = False
            platformWidth = 0

        # Change our x location for each tile
        if tile != " ":
          currentXLoc += self.tileWidth

      # Change our y location for each row, and reset back to the first tile
      currentYLoc += self.tileHeight
      currentXLoc = 0

    # Create any platform we were still building at the end, which will be the ground so add the weird gap at the bottom
    platformLocs.append([platformLoc, (platformWidth+self.tileWidth, self.tileHeight+self.bottomGap)])

    # Return the platform locations and starting location
    return platformLocs, triangleLocs, startingLoc

  def countColumns(self):
    columnCount = 0
    for column in self.levelTiles[0]:
      if column != " ":
        columnCount += 1

    return columnCount

  def createRectangleChoiceHolder(self):
    # N spawns a normal rain rectangle
    for chance in range(self.normalRainChance):
      self.rectangleChoices.append("N")

    # B spawns a bounce rain rectangle
    for chance in range(self.bounceRainChance):
      self.rectangleChoices.append("B")

    # E spawns an exploding rain rectangle
    for chance in range(self.explodingRainChance):
      self.rectangleChoices.append("E")

    # P spawns a puddle rain rectangle
    for chance in range(self.puddleRainChance):
      self.rectangleChoices.append("P")

  def spawnNewRectangle(self, xLoc, yLoc=HUD_HEIGHT):
    # Get a random rectangle choice from our list
    rectangleChoice = random.choice(self.rectangleChoices)

    # Normal rain
    if rectangleChoice == "N":
      return NormalRectangleRain((xLoc, yLoc - RECTANGLE_HEIGHT))

    # Bouncing rain
    elif rectangleChoice == "B":
      return BounceRectangleRain((xLoc, yLoc - RECTANGLE_HEIGHT))

    # Exploding rain
    elif rectangleChoice == "E":
      return ExplodingRectangleRain((xLoc, yLoc - RECTANGLE_HEIGHT))

    # Puddle rain
    elif rectangleChoice == "P":
      return PuddleRectangleRain((xLoc, yLoc - RECTANGLE_HEIGHT))

  def levelComplete(self, currentScore):
    return currentScore >= self.requiredScore

class Level_01(Level):
   def __init__(self):
    Level.__init__(self, requiredScore=2, normalRainChance=1, bounceRainChance=1, explodingRainChance=1, puddleRainChance=1)

    self.levelTiles = [
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ T _ _ _ _ _",
    "_ _ _ _ _ _ P _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ T t _ _ _ _ T t _ _",
    "_ _ P p _ _ _ _ P p _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ S _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _",
    "_ T _ _ _ T _ _ _ T _ _",
    "P p p p p p p p p p p p"]

    self.caption = "Just warming up"

class Level_02(Level):
  def __init__(self):
    Level.__init__(self, requiredScore=9999, rectangleSpawnNumber=75)

    self.levelTiles = [
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ P _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ P _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ P _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ T t _ _ _ _ T t _ _ T t _ _ _ _ _ _ _ _ _ _ T t _ _ T t _ _ T t _ _",
    "_ _ P p _ _ _ _ P p _ _ P p _ _ _ _ _ _ _ _ _ _ P p _ _ P p _ _ P p _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ S _ _",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "_ T _ _ _ T _ _ _ T _ _ _ T _ _ _ T _ _ _ T _ _ _ T _ _ _ T _ _ _ T _ _",
    "P p p p p p p p p p p p p p p p p p p p p p p p p p p p p p p p p p p p"]

    self.caption = "Try this"

class Level_03(Level):
  def __init__(self):
    pass

class Level_04(Level):
  def __init__(self):
    pass

class Level_05(Level):
  def __init__(self):
    pass

class Level_06(Level):
  def __init__(self):
    pass

class Level_07(Level):
  def __init__(self):
    pass

class Level_08(Level):
  def __init__(self):
    pass

class Level_09(Level):
  def __init__(self):
    pass

class Level_10(Level):
  def __init__(self):
    pass
