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
  nextScene = scenes.Scene.mainMenuScene

  # Loop until it's time to quit
  running = True
  while running:

    # Show the level scene
    if nextScene == scenes.Scene.levelScene:
      scene = scenes.LevelScene(screen)
      scene.setDifficulty(difficulty)
      nextScene = scene.display()
      totalScore, level = scene.getFinalProgress()

    # Show the Difficulty menu
    elif nextScene == scenes.Scene.difficultyScene:
      scene = scenes.DifficultyMenu(screen)
      nextScene = scene.display()
      difficulty = scene.getDifficulty()

    # Show the help screen
    elif nextScene == scenes.Scene.helpScene:
      scene = scenes.HelpScene(screen)
      nextScene = scene.display()

    # Show the main menu
    elif nextScene == scenes.Scene.mainMenuScene:
      scene = scenes.MainMenu(screen)
      nextScene = scene.display()

    # Show the game over scene
    elif nextScene == scenes.Scene.gameOverScene:
      scene = scenes.GameOverScene(screen)
      scene.setFinalProgress(totalScore, level)
      nextScene = scene.display()

    # Time to quit
    elif nextScene == scenes.Scene.quit:
      running = False

# Run our program
if __name__ == "__main__":
  main()
