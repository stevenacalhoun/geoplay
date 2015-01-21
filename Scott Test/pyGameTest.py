#! /usr/bin/env/python

import pygame 
 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

SCOTT_WIDTH = 100
SCOTT_HEIGHT = 125

SCOTT_RIGHT_START = 0
SCOTT_LEFT_START = 145

MOVE_DISTANCE = 35

SPACER = 110

GRAVITY = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    pygame.init()
    screen.fill((0, 0, 0))

    running = True

    scott = Scott([0, SCREEN_HEIGHT - SCOTT_HEIGHT])
    sprite_group = pygame.sprite.Group(scott)

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scott.runLeft(MOVE_DISTANCE)
            elif event.key == pygame.K_RIGHT:
                scott.runRight(MOVE_DISTANCE)
            elif event.key == pygame.K_SPACE:
                scott.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scott.stopRunning()
            if event.key == pygame.K_RIGHT:
                scott.stopRunning()


        time = pygame.time.get_ticks()

        sprite_group.update(time)
        sprite_group.draw(screen)

        pygame.display.flip()


class Scott(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load("scott.png").convert()

        self.runRightImages = []
        self.runLeftImages = []

        runRightLocations = [
                        SPACER * 0,   # frame 0
                        SPACER * 1,   # frame 1
                        SPACER * 2,   # frame 2
                        SPACER * 3,   # frame 3
                        SPACER * 4,   # frame 4
                        SPACER * 5,   # frame 5
                        SPACER * 6,   # frame 6
                        SPACER * 7    # frame 7
        ]

        runLeftLocations = [
                        SPACER * 7, # frame 0
                        SPACER * 6, # frame 1
                        SPACER * 5, # frame 2
                        SPACER * 4, # frame 3
                        SPACER * 3, # frame 4
                        SPACER * 2, # frame 5
                        SPACER * 1, # frame 6
                        SPACER * 0  # frame 7
        ]

        for location in runRightLocations:
            self.sheet.set_clip(pygame.Rect(location, SCOTT_RIGHT_START, SCOTT_WIDTH, SCOTT_HEIGHT))
            image = self.sheet.subsurface(self.sheet.get_clip())
            self.runRightImages.append(image)

        for location in runLeftLocations:
            self.sheet.set_clip(pygame.Rect(location, SCOTT_LEFT_START, SCOTT_WIDTH, SCOTT_HEIGHT))
            image = self.sheet.subsurface(self.sheet.get_clip())
            self.runLeftImages.append(image)

        standingImage = pygame.image.load("scottStanding.gif")
        self.image = standingImage

        self.rect = self.sheet.get_rect()
        self.rect.x = 90
        self.rect.y = 115
        self.rect.topleft = initial_position

        self.runningLeft = False
        self.runningRight = False

        self.finishedLeft = True
        self.finishedRight = True

        self.next_update_time = 0
        self.frameCount = 0

        self.falling = False
        self.jumping = False

        self.speed = [0, GRAVITY]

    def update(self, current_time):
        if self.next_update_time < current_time:
            self.animate()
            self.move()

            self.next_update_time = current_time + 100


    def animate(self):
        self.old = self.rect
        screen.blit(pygame.Surface((SCOTT_WIDTH, SCOTT_HEIGHT)), self.old)

        if self.runningLeft or self.runningRight or (self.finishedLeft == False) or (self.finishedRight == False):
            if self.runningLeft or (self.finishedLeft == False):
                imageSet = self.runLeftImages
            elif self.runningRight or (self.finishedRight == False):
                imageSet = self.runRightImages

            self.image = imageSet[self.frameCount]

            self.frameCount += 1
            if self.frameCount == 8:
                self.frameCount = 0
            
            if (self.frameCount == 0):
                self.finishedRight = True
            if (self.frameCount == 7):
                self.finishedLeft = True

            if self.runningRight:
                self.finishedRight = False
            elif self.runningLeft:
                self.finishedLeft = False


    def move(self):
        # Move horizontally
        if (self.rect.x >= 0) and (self.rect.x <= (SCREEN_WIDTH - SCOTT_WIDTH)):
            self.rect.x += self.speed[0]

        # Move vertically
        if self.speed[1] > 0:
            # Moving down
            if self.rect.y <= SCREEN_HEIGHT - SCOTT_HEIGHT:
                self.rect.y += self.speed[1]
        else:
            # Moving up
            if self.rect.y >= 0:
                self.rect.y += self.speed[1]
                if self.jumping:
                    # Slow down the jump
                    self.speed[1] += 10
                    if self.speed[1] >= 0:
                        # Peak of the jump
                        self.jumping = False
                        self.falling = True
                        self.speed[1] = GRAVITY * .1
                if self.falling:
                    if self.speed[1] < GRAVITY:
                        self.speed[1] += 10
                    else:
                        self.speed[1] = GRAVITY
                        self.falling = False


    def run(self, speed):
        self.speed[0] = speed

    def jump(self):
        self.speed[1] = -30
        self.jumping = True

    def stopRunning(self):
        self.runningRight = False
        self.runningLeft = False
        self.speed[0] = 0

    def runLeft(self, speed):
        self.runningLeft = True
        self.run(-speed)

    def runRight(self, speed):
        self.runningRight = True
        self.run(speed)


if __name__ == "__main__":
    main()
