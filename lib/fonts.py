import pygame
from pygame import Surface
from pygame.locals import *

class TextLine():
  def __init__(self, screen, text, font='monospace', size=16, color=(0,0,0)):
    self.font = pygame.font.SysFont(font, size)
    self.color_fg = color
    self.color_bg = Color("white")

    self.screen = screen

    self._aa = True
    self._text = text
    self.dirty = True

  def _render(self):
    # render for cache
    self.dirty = False
    self.image = self.font.render(self._text, self._aa, self.color_fg)
    self.rect = self.image.get_rect()
    self.width = self.rect.width
    self.height = self.rect.height
    self.screen = pygame.display.get_surface()

  def _draw(self, location=(0,0)):
    self.screen.blit(self.image, location)

    locX, locY = location

    # pygame.draw.line(self.screen, (0,0,0), (0, locY), (1200, locY))
    # pygame.draw.line(self.screen, (0,0,0), (locX, 0), (locX, 900))

  def drawByCenter(self, center=(0,0)):
    self._render()
    locX, locY = center

    drawX = locX - (self.width/2)
    drawY = locY - (self.height/2)

    self._draw((drawX, drawY))

  def drawByTopLeft(self,topLeft=(0,0)):
    self._render()

    self._draw(topLeft)


class TextBox():
  def __init__(self, text, fontName='monospace', size=16, color=(0,0,0)):
    self.font = pygame.font.SysFont(fontName, size)
    self.color_fg = color
    self.color_bg = Color("white")

    self.text_lines = [ TextLine(line, font=fontName, size=size, color=color) for line in text ]

    self._aa = True
    self._text = text
    self.dirty = True


  def _render(self):
    # render for cache
    self.dirty = False
    self.image = self.font.render(self._text, self.aa, self.color_fg)
    self.rect = self.image.get_rect()
    self.screen = pygame.display.get_surface()

  def draw(self, screen, location=(0,0)):
    self._render()
    screen.blit(self.image, location)

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self, text):
    self.dirty = True
    self._text = text

  @property
  def aa(self): return self._aa

  @aa.setter
  def aa(self, aa):
    self.dirty = True
    self._aa = aa
