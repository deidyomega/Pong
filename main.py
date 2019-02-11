import pygame
import random
import time
from pygame.locals import *
from functools import partial

class Player:
    speed = 5
    color = (255, 0, 0)
    rec1 = pygame.Rect(50, 100, 5, 75)
    rec2 = pygame.Rect(725, 100, 5, 75)
    game_height = 0

    def __init__(self, win):
        self.win = win
        self.game_height = win.get_rect().height

    def level_up(self):
        self.speed += 1

    def move(self, direction):
        if direction == "up":
            self.rec1 = self.rec1.move(0, self.speed * -1)
            self.rec2 = self.rec2.move(0, self.speed * -1)
            if self.rec1.y < 0:
                self.rec1.y = 0
                self.rec2.y = 0

        if direction == "down":
            self.rec1 = self.rec1.move(0, self.speed)
            self.rec2 = self.rec2.move(0, self.speed)
            if self.rec1.y > self.game_height - self.rec1.height:
                self.rec1.y = self.game_height - self.rec1.height
                self.rec2.y = self.game_height - self.rec2.height

    def draw(self):
        pygame.draw.rect(self.win, self.color, self.rec1)
        pygame.draw.rect(self.win, self.color, self.rec2)

class Ball:
    """ Ball is calculated as a square, but drawn as a circle """
    radius = 15
    hor_speed = 5
    vert_speed = 0
    color = (0, 255, 0)
    rec = pygame.Rect(0, 0, radius*2, radius*2)
    game_height = 0
    
    def __init__(self, win):
        win_rect = win.get_rect()
        self.win = win
        self.rec.x = win_rect.centerx - self.radius
        self.rec.y = win_rect.centery - self.radius
        self.game_height = win_rect.height
        self.game_width = win_rect.width
        self.vert_speed = random.randint(-5, 5)
        if random.choice([True, False]):
            self.hor_speed *= -1

    def level_up(self):
        if self.hor_speed < 0:
            self.hor_speed -= 2
        else:
            self.hor_speed += 2

    def detect_win(self):
        if self.rec.x < 0 or self.rec.x > self.game_width:
            return True
        else:
            return False

    def respond_to_collide(self):
        self.rec = self.rec.move(-1 * (self.hor_speed), -1 * (self.vert_speed))
        self.hor_speed *= -1
        self.vert_speed = random.randint(-5, 5)

    def move(self):
        self.rec = self.rec.move(self.hor_speed, self.vert_speed)
        if self.rec.y < 0 or self.rec.y > self.game_height - self.rec.height:
            self.vert_speed *= -1
            self.rec = self.rec.move(0, self.vert_speed * 2)

    def draw(self):
        pygame.draw.circle(
            self.win,
            self.color,
            (self.rec.x+self.radius, self.rec.y+self.radius),
            self.radius
        )
        
    def detect_collide(self, player):
        collide = self.rec.colliderect(player.rec1) or self.rec.colliderect(player.rec2)
        if collide:
            self.respond_to_collide()
        return collide

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
    level = 1
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
        print_c(level, 0, -25, (20,20,20))
        print_c(score, 0, 25, (20,20,20))
        ball.draw()

        if ball.detect_collide(player):
            score += 1
            if score % 3 == 0:
                level += 1
                ball.level_up()
                player.level_up()

        if ball.detect_win():
            run = False

        pygame.display.update()
        clock.tick(60)

    return score

if __name__ == "__main__":
    main_menu()
