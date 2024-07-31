import random
import pygame
import sys
from pygame.locals import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

BIRD_WIDTH = 60
BIRD_HEIGHT = 45
G = 0.5
SPEED_FLY = -8
BIRD_IMG = pygame.image.load("img/bird.png")

COLUMN_WIDTH = 60
COLUMN_HEIGHT = 500
BLANK = 160
DISTANCE = 200
COLUMN_SPEED = 2
COLUMN_IMG = pygame.image.load("img/column.png")

pygame.init()

BACKGROUND = pygame.image.load("img/background.png")

FPS = 60
fpsClock = pygame.time.Clock()

DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")


class Bird:
    def __init__(self):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.x = (WINDOW_WIDTH - BIRD_WIDTH) / 2
        self.y = (WINDOW_HEIGHT - BIRD_HEIGHT) / 2
        self.speed = 0
        self.surface = BIRD_IMG

    def draw(self):
        DISPLAY_SURFACE.blit(self.surface, (self.x, self.y))

    def update(self, mouse_click):
        self.y += self.speed + 0.5 * G
        self.speed += G
        if mouse_click:
            self.speed = SPEED_FLY


class Columns:
    def __init__(self):
        self.width = COLUMN_WIDTH
        self.height = COLUMN_HEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        self.speed = COLUMN_SPEED
        self.surface = COLUMN_IMG
        self.ls = []
        for i in range(3):
            x = i * self.distance + WINDOW_WIDTH
            y = random.randrange(60, WINDOW_HEIGHT - BLANK - 60, 20)
            self.ls.append([x, y])

    def draw(self):
        for i in range(3):
            DISPLAY_SURFACE.blit(self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
            DISPLAY_SURFACE.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))

    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.speed
        if self.ls[0][0] + self.width < 0:
            self.ls.pop(0)
            x = self.ls[1][0] + self.distance
            y = random.randrange(60, WINDOW_HEIGHT - BLANK - 60, 20)
            self.ls.append([x, y])


def rect_collision(rect1, rect2):
    if rect1[0] <= rect2[0] + rect2[2] and rect1[1] <= rect2[1] + rect2[3] and rect2[0] <= rect1[0] + rect1[2] and \
            rect2[1] <= rect1[1] + rect1[3]:
        return True
    return False


def is_game_over(bird, columns):
    for i in range(3):
        rect_bird = [bird.x, bird.y, bird.width, bird.height]
        rect_column1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
        rect_column2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
        if rect_collision(rect_bird, rect_column1) or rect_collision(rect_bird, rect_column2):
            return True
    if bird.y + bird.height < 0 or bird.y + bird.height > WINDOW_HEIGHT:
        return True
    return False


class Score:
    def __init__(self):
        self.score = 0
        self.addScore = False

    def draw(self):
        font = pygame.font.SysFont('consolas', 40)
        score_surface = font.render(str(self.score), True, (0, 0, 0))
        text_size = score_surface.get_size()
        DISPLAY_SURFACE.blit(score_surface, (int((WINDOW_WIDTH - text_size[0]) / 2), 100))

    def update(self, bird, columns):
        collision = False
        for i in range(3):
            rect_column = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
            rect_bird = [bird.x, bird.y, bird.width, bird.height]
            if rect_collision(rect_bird, rect_column):
                collision = True
                break
        if collision:
            if self.addScore:
                self.score += 1
            self.addScore = False
        else:
            self.addScore = True


def game_play(bird, columns, score):
    bird.__init__()
    bird.speed = SPEED_FLY
    columns.__init__()
    score.__init__()
    while True:
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
        DISPLAY_SURFACE.blit(BACKGROUND, (0, 0))
        columns.draw()
        columns.update()
        bird.draw()
        bird.update(mouse_click)
        score.draw()
        score.update(bird, columns)

        if is_game_over(bird, columns):
            return

        pygame.display.update()
        fpsClock.tick(FPS)


def game_start(bird):
    bird.__init__()

    font = pygame.font.SysFont('arial', 60)
    heading_surface = font.render('FLAPPYBIRD', True, (255, 0, 0))
    heading_size = heading_surface.get_size()

    font = pygame.font.SysFont('arial', 20)
    comment_surface = font.render('Click to start the game', True, (0, 0, 0))
    comment_size = comment_surface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        DISPLAY_SURFACE.blit(BACKGROUND, (0, 0))
        bird.draw()
        DISPLAY_SURFACE.blit(heading_surface, (int(WINDOW_WIDTH - heading_size[0]) / 2, 100))
        DISPLAY_SURFACE.blit(comment_surface, (int(WINDOW_WIDTH - comment_size[0]) / 2, 50))

        pygame.display.update()
        fpsClock.tick(FPS)


def game_over(bird, columns, score):
    font = pygame.font.SysFont('arial', 60)
    heading_surface = font.render('GAME OVER', True, (255, 0, 0))
    heading_size = heading_surface.get_size()

    font = pygame.font.SysFont('arial', 20)
    comment_surface = font.render('Press "space" to replay', True, (0, 0, 0))
    comment_size = comment_surface.get_size()

    font = pygame.font.SysFont('arial', 30)
    score_surface = font.render('Score: ' + str(score.score), True, (255, 0, 0))
    score_size = score_surface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    return
        DISPLAY_SURFACE.blit(BACKGROUND, (0, 0))
        columns.draw()
        bird.draw()
        DISPLAY_SURFACE.blit(heading_surface, (int(WINDOW_WIDTH - heading_size[0]) / 2, 100))
        DISPLAY_SURFACE.blit(comment_surface, (int(WINDOW_WIDTH - comment_size[0]) / 2, 500))
        DISPLAY_SURFACE.blit(score_surface, (int(WINDOW_WIDTH - score_size[0]) / 2, 160))

        pygame.display.update()
        fpsClock.tick(FPS)


def main():
    bird = Bird()
    columns = Columns()
    score = Score()
    while True:
        game_start(bird)
        game_play(bird, columns, score)
        game_over(bird, columns, score)


if __name__ == '__main__':
    main()
