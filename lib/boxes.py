import pygame
from pygame import Surface
from pygame.locals import *
from constants import *

class Box():
  def __init__(self, screen, width, height, color, alpha=255):
    self.screen = screen
    self._width = width
    self._height = height
    self._color = color
    self.alpha = alpha

  def _draw(self, location=(0,0)):
    self.location = location
    self.image = pygame.Surface((self._width, self._height))
    self.image.fill(self._color)

    self.rect = self.image.get_rect()
    self.topLeft = location
    self.image.set_alpha(self.alpha)

    self.screen.blit(self.image, location)

  def drawByCenter(self, center=(0,0)):
    centerX, centerY = center

    self.locX = centerX - (self._width/2)
    self.locY = centerY - (self._height/2)

    self._draw((self.locX, self.locY))

  def drawByTopLeft(self, topLeft=(0,0)):
    self.locX, self.locY = topLeft
    self._draw((self.locX, self.locY))

  def outline(self, padding=(10, 10), color=BLACK):
    padX, padY = padding
    pygame.draw.rect(self.screen, color, (self.locX - (padX), self.locY - (padY), self._width + (padX*2), self._height + (padY*2)), 2)

  def changeTransparency(self, alpha=0):
    self.image.set_alpha(alpha)
    self.screen.blit(self.image, self.location)
