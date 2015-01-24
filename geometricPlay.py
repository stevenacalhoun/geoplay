#! /usr/bin/env/python

import sys
sys.path.insert(0, 'lib')

import pygame
import math
from random import randint
from constants import *
import scenes

# Global variable to draw on the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
screen.fill(WHITE)
clock = pygame.time.Clock()

def main():
  # Initialize the screen
  pygame.init()
  pygame.font.init()

  # Default difficulty is two, start on the main menu
  difficulty = 2
  scene = scenes.MainMenu(screen)
  newScene = scene.display()

  # Loop infinitely
  running = True
  while True:

    # This is a weird way of switch screens, I'm trying to thingk of better mehtods of accomplishing it
    if newScene == 0:
      scene = scenes.LevelScene(screen, difficulty)
      newScene = scene.display()
    elif newScene == 1:
      scene = scenes.DifficultyMenu(screen)
      newScene, difficulty = scene.display()
    elif newScene == 2:
      scene = scenes.HelpScene(screen)
      newScene = scene.display()
    elif newScene == 3:
      scene = scenes.MainMenu(screen)
      newScene = scene.display()
    elif newScene == 4:
      scene = scenes.GameOverScene(screen)
      newScene = scene.display()


# Run our program
if __name__ == "__main__":
  main()
