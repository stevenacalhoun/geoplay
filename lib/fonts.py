import pygame
from pygame import Surface
from pygame.locals import *
from constants import *
import string

# Class to help render single lines of text
class TextLine():
  def __init__(self, screen, text, font=GAME_FONT, size=16, color=(0,0,0)):
    self.screen = screen
    self.text = text
    self.font = pygame.font.SysFont(font, size)
    self.color = color

  def _render(self):
    # Render the text
    self.image = self.font.render(self.text, True, self.color)
    self.rect = self.image.get_rect()
    self.width = self.rect.width
    self.height = self.rect.height

  def _draw(self, location=(0,0)):
    # Draw the text
    self.screen.blit(self.image, location)

  def drawByCenter(self, center=(0,0)):
    # Render the text
    self._render()

    # Find where we need to offset it for the center
    locX, locY = center
    drawX = locX - (self.width/2)
    drawY = locY - (self.height/2)

    # Draw the text
    self._draw((drawX, drawY))

  def drawByTopLeft(self,topLeft=(0,0)):
    # Render the text then draw it by the topleft
    self._render()
    self._draw(topLeft)

# Class to help render multi-lined text
class TextMultiLine():
  def __init__(self, screen, text, font=GAME_FONT, size=16, color=(0,0,0), lineSpacing=10):
    self.font = pygame.font.SysFont(font, size)
    self.textLineObjects = []
    self.lineSpacing = lineSpacing

    # Split up the text and create a single line object for each line
    textLines = string.split(text, "\n")

    for textLine in textLines:
      self.textLineObjects.append(TextLine(screen, textLine, font=GAME_FONT, size=size, color=color))

  # Draw all the lines be positioning the center
  def drawByCenter(self, center=(0,0)):
    xLoc, yLoc = center

    # Draw each line, increasing the yLoc for each line
    for textLineNum, textLineObject in enumerate(self.textLineObjects):
      textLineObject.drawByCenter((xLoc, yLoc + (textLineNum * self.lineSpacing)))

  # Draw all the lines be positioning the top left
  def drawByTopLeft(self,topLeft=(0,0)):
    xLoc, yLoc = center

    # Draw each line, increasing the yLoc for each line
    for textLineNum, textLineObject in enumerate(self.textLineObjects):
      textLineObject.drawByCenter((xLoc, yLoc + (textLineNum * self.lineSpacing)))
