import pygame
from pygame import Surface
from pygame.locals import *

class Box():
  def __init__(self, width, height, color):
    self._width = width
    self._height = height
    self._color = color

  def _draw(self, screen, location=(0,0,0)):
    pygame.draw.rect(screen, self._color, (location, (self._width, self._height)))

  def drawByCenter(self, screen, center=(0,0,0)):
    centerX, centerY = center

    # pygame.draw.line(screen, (0,0,0), (0, self.locY), (1200, self.locY))
    # pygame.draw.line(screen, (0,0,0), (self.locX, 0), (self.locX, 900))

    self.locX = centerX - (self._width/2)
    self.locY = centerY - (self._height/2)

    self._draw(screen, (self.locX, self.locY))

  def drawByTopLeft(self, screen, topLeft=(0,0,0)):
    self.locX, self.locY = topLeft
    self._draw(screen, (drawX, drawY))

  def outline(self, screen, padding=(10, 10)):
    padX, padY = padding
    pygame.draw.rect(screen, self._color, (self.locX - (padX), self.locY - (padY), self._width + (padX*2), self._height + (padY*2)), 2)
