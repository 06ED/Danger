import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self,  *group):
        super().__init__(*group)

    def set_parameters(self, image_url, hover_image_url, x, y):  # Установка параметров вне иницилизации
        self.smart_image = pygame.image.load(image_url)
        self.hover_image = pygame.image.load(hover_image_url)
        self.image = self.smart_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, events):
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # Смена цвета при наведении на кнопку
            self.image = self.hover_image
        else:
            self.image = self.smart_image
