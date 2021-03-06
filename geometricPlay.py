#! /usr/bin/env/python

import sys
sys.path.insert(0, 'lib')

import pygame
import math
from random import randint
from constants import *
import scenes
import sprites
import musicManager

# Global variable to draw on the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geo-Play")
image = pygame.image.load("images/sprites-individ/stand-right1.png").convert()
transColor = (255, 0, 0)
image.set_colorkey(transColor)
pygame.display.set_icon(image)

screen.fill(WHITE)
clock = pygame.time.Clock()

pygame.mixer.pre_init(44100, -16, 16, 4096) # setup mixer to avoid sound lag

def main():
  # Initialize the screen
  pygame.init()
  pygame.font.init()

  # Start music manager
  music = musicManager.musicManager()
  channel_m = music.play()

  # Show the splash screen
  intro = scenes.IntroScene(screen)
  intro.display()

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

  pygame.quit()

# Run our program
if __name__ == "__main__":
  main()
