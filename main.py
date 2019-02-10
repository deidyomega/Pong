import pygame
import random
import time
from pygame.locals import *
from functools import partial

class Player:
    x1 = 50
    x2 = 725
    y = 100
    width = 5
    height = 75
    speed = 5
    color = (255, 0, 0)

    def __init__(self, win):
        self.win = win

    def move(self, direction):
        if direction == "up":
            self.y -= self.speed
            if self.y < 0:
                self.y = 0
        if direction == "down":
            self.y += self.speed
            if self.y > 500-self.height:
                self.y = 500-self.height

    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.x1, self.y, self.width, self.height))
        pygame.draw.rect(self.win, self.color, (self.x2, self.y, self.width, self.height))

class Ball:
    x = 250
    y = 110
    radius = 15
    hor_speed = 5
    vert_speed = 2
    color = (0, 255, 0)
    
    def __init__(self, win):
        self.win = win

    def detect_win(self):
        if self.x < 0 or self.x > 800:
            return True
        else:
            return False

    def respond_to_collide(self):
        self.hor_speed *= -1
        self.vert_speed = random.randint(-5, 5)

    def move(self):
        self.x += self.hor_speed
        self.y += self.vert_speed
        if self.y < self.radius or self.y > 500-self.radius:
            self.vert_speed *= -1

    def draw(self):
        pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

    def detect_collide(self, player):
        rez = False
        if not (self.y > player.y + player.height or self.y + (self.radius*2) < player.y):
            if self.x + self.radius == player.x2:
                rez = True
            if self.x - self.radius == player.x1+5:
                rez = True
        if rez:
            self.respond_to_collide()
        return rez

def print_to_screen(win, msg, xoff=0, yoff=0, color=(255,0,0)):
    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render(str(msg), True, color, (0, 0, 0))
    textrect = text.get_rect()
    textrect.centerx = win.get_rect().centerx + xoff
    textrect.centery = win.get_rect().centery + yoff
    win.blit(text, textrect)

def main_menu():
    pygame.init()
    win = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Loner Pong")
    print_c = partial(print_to_screen, win)

    basicfont = pygame.font.SysFont(None, 48)
    win.fill((0, 0, 0))

    for x in range(3, 0, -1):
        print_c("Loner Pong", 0, -25)
        print_c(x, 0, 25)
        pygame.display.update()
        time.sleep(1)

    score = main_game(win)

    win.fill((0,0,0))
    print_c("Game Over", 0, -25)
    print_c("Final Score: " + str(score), 0, 25)
    pygame.display.update()
    time.sleep(3)

    pygame.quit()

def main_game(win):
    score = 0
    clock = pygame.time.Clock()
    print_c = partial(print_to_screen, win)

    player = Player(win)
    ball = Ball(win)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_DOWN]:
            player.move("down")
        
        if keys[pygame.K_UP]:
            player.move("up")

        win.fill((0,0,0))

        player.draw()
        ball.move()
        print_c(score, 0, 0, (20,20,20))
        ball.draw()

        if ball.detect_collide(player):
            score += 1

        if ball.detect_win():
            run = False

        pygame.display.update()
        clock.tick(60)

    return score

if __name__ == "__main__":
    main_menu()
