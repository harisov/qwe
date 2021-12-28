import os
import sys
import pygame
import random

pygame.init()
size = width, height = 600, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Дудл джамп")
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Dudu(pygame.sprite.Sprite):
    image = load_image("dudu.png")
    image = pygame.transform.scale(image, (75, 75))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Dudu.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, Platform()):
            self.rect = self.rect.move(0, 1)


class Platform(pygame.sprite.Sprite):
    image = load_image("plata.png")
    image = pygame.transform.scale(image, (75, 15))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)


back = load_image("background.png")
back = pygame.transform.scale(back, (600, 800))

if __name__ == '__main__':
    for _ in range(30):
        Platform(all_sprites)
    x, y = 250, 725
    clock = pygame.time.Clock()
    running = True
    screen.blit(back, (0, 0))
    while running:
        Dudu(x, y)
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
                x -= 5
        if pressed_keys[pygame.K_RIGHT]:
                x += 5
        all_sprites.draw(screen)
        clock.tick(100)
        pygame.display.flip()
    pygame.quit()