import pygame
import config

class Button:
    def __init__(self, text, pos, callback, font = None, font_size = 36):
        self.text = text
        self.pos = pos
        self.callback = callback
        self.font = pygame.font.Font(font, font_size)
        self.rendered_text = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.rendered_text.get_rect(center=self.pos)

    def draw(self, screen):
        screen.blit(self.rendered_text, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class HealthStatusBar:
    def __init__(self, font = None, font_size = 36):
        self.pos = (700,900)
        self.font = pygame.font.Font(font, font_size)
        self.rendered_text = self.font.render("Health:", True, (255, 0, 0))
        self.rect = self.rendered_text.get_rect(center=self.pos)

    def draw(self, screen, health):
        self.rendered_text = self.font.render("Health: " + str(health), True, (255, 0, 0))
        screen.blit(self.rendered_text, self.rect)

class EnemyHealthStatusBar:
    def __init__(self, font = None, font_size = 36):
        self.pos = (700,600)
        self.font = pygame.font.Font(font, font_size)
        self.rendered_text = self.font.render("Enemy Health:", True, (255, 0, 0))
        self.rect = self.rendered_text.get_rect(center=self.pos)

    def draw(self, screen, health):
        self.rendered_text = self.font.render("Enemy Health: " + str(health), True, (255, 0, 0))
        screen.blit(self.rendered_text, self.rect)

class GestureStatusBar:
    def __init__(self, font = None, font_size = 36):
        self.pos = (700,950)
        self.font = pygame.font.Font(font, font_size)
        self.rendered_text = self.font.render("Gesture:", True, (255, 0, 0))
        self.rect = self.rendered_text.get_rect(center=self.pos)

    def draw(self, screen, gesture):
        self.rendered_text = self.font.render("Gesture: " + gesture, True, (255, 0, 0))
        screen.blit(self.rendered_text, self.rect)

class TuneBoard:
    # draw tune.jpg
    def __init__(self):
        self.pos = (0,0)
        self.image = pygame.image.load("./img/tune.jpg")
    def draw(self, screen):
        screen.blit(self.image, self.pos)

class Fist:
    def __init__(self, pos):
        self.image = pygame.image.load("./img/fist.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dy):
        self.rect.y += dy

class Sword:
    def __init__(self, pos):
        self.image = pygame.image.load("./img/sword.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dy):
        self.rect.y += dy

class Shield:
    def __init__(self, pos):
        self.image = pygame.image.load("./img/shield.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dy):
        self.rect.y += dy

class ok:
    def __init__(self, pos):
        self.image = pygame.image.load("./img/ok.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dy):
        self.rect.y += dy

class Enemy:
    def __init__(self, position=(550,100)):
        self.image = pygame.image.load('./img/enemy.png')
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

background_image = pygame.image.load("./img/OpenMenuBg.jpg")
background_image = pygame.transform.scale(background_image, (config.screen_width, config.screen_height))
# preparation_image = pygame.image.load("./img/PreparationSceneBG.png")
# preparation_image = pygame.transform.scale(preparation_image, (config.screen_width, config.screen_height))
level1_image = pygame.image.load("./img/Level1BG.jpg")
level1_image = pygame.transform.scale(level1_image, (350, config.screen_height))

def load_preparation_image():
    image = pygame.image.load("./img/PreparationSceneBG.png")
    return pygame.transform.scale(image, (config.screen_width, config.screen_height))