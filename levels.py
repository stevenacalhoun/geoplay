import pygame
import math
from random import randint
from constants import *
import scenes

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
  def __init__(self):
    pass

  def generateLevel(self):
    platformLocs = []

    numRows = len(self.levelTiles)
    numColumns = len(self.levelTiles[0])

    tileWidth = SCREEN_WIDTH/numColumns
    tileHeight = SCREEN_HEIGHT/numRows

    currentXLoc = 0
    currentYLoc = 0

    buildingPlatform = False
    platformWidth = 0
    platformLoc = 0

    # Walk over every row in the level
    for row in self.levelTiles:
      # Walk over every tile in the row
      for tile in row:
        # P stands for platform
        if tile == "P":
          # If we are currently building a platform, create it
          if buildingPlatform:
            platformLocs.append([platformLoc, (platformWidth, tileHeight)])

          # Start a new platform
          buildingPlatform = True
          platformLoc = currentXLoc, currentYLoc
          platformWidth = tileWidth

        # p stands for a growing platform
        elif tile == "p":
          platformWidth += tileWidth

        # S stands for the starting point for McSquare
        elif tile == "S":
          startingLoc = currentXLoc, currentYLoc

        # There is nothing on this tile
        else:
          # If we are building a platform, this means we've finished it, so build it
          if buildingPlatform:
            platformLocs.append([platformLoc, (platformWidth, tileHeight)])
            buildingPlatform = False
            platformWidth = 0

        # Change our x location for each tile
        currentXLoc += tileWidth

      # Change our y location for each row, and reset back to the first tile
      currentYLoc += tileHeight
      currentXLoc = 0

    # Create any platform we were still building at the end
    platformLocs.append([platformLoc, (platformWidth+tileWidth, tileHeight)])

    # Return the platform locations and starting location
    return platformLocs, startingLoc

class Level_01(Level):
   def __init__(self):
    self.levelTiles = [
    "____________",
    "____________",
    "____________",
    "______P_____",
    "____________",
    "____________",
    "____________",
    "__Pp____Pp__",
    "____________",
    "____________",
    "____________",
    "_________S__",
    "____________",
    "____________",
    "PppPppPppPpp"]

class Level_02(Level):
  def __init__(self):
    pass

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
