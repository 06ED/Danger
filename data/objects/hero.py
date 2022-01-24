import pygame
import ctypes

HERO_XP = 200


class Hero(pygame.sprite.Sprite):
    image = pygame.image.load("data//images//hero//right.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = ctypes.windll.user32.GetSystemMetrics(1) - self.image.get_rect()[3]
        self.right_image = pygame.image.load("data//images//hero//right.png").convert_alpha()
        self.left_image = pygame.image.load("data//images//hero//left.png").convert_alpha()
        self.is_right = True
        self.n = 0
        self.right_go = False
        self.left_go = False
        self.jump_flag = False  # Флаг и счетчик для прыжков
        self.jump_count = 200
        self.right = False  # Флаг для движения вправо
        self.left = False  # Флаг для движения влево
        self.right_animation = False
        self.left_animation = False
        self.collide_flag = False
        self.two = True
        self.flag = True

    def get_pos(self):
        return [self.rect.x, self.rect.y]

    def set_xp(self):
        global HERO_XP
        HERO_XP -= 1

    def left_(self):
        self.right = False
        self.left = True
        self.right_animation = False
        self.left_animation = True
        self.left_go = True
        self.right_go = False

    def right_(self):
        self.right = True
        self.left = False
        self.left_go = False
        self.right_go = True
        self.right_animation = True
        self.left_animation = False

    def collide(self):
        self.collide_flag = True

    def jump(self):
        self.jump_flag = True

    def update(self):
        if not self.right and not self.left:
            self.n = 0
            if self.is_right:
                self.image = self.right_image
            else:
                self.image = self.left_image
        if ((self.left_animation and not self.right_animation)
                or (self.right_animation and not self.left_animation)) and (self.left_go or self.right_go):
            if self.right_go and self.rect.x \
                    + 170 <= ctypes.windll.user32.GetSystemMetrics(0):
                self.right_go = False
                self.left_go = False
                self.is_right = True
                self.rect.x += 5
            else:
                self.right_go = False
            if self.left_go and self.rect.x >= 0:
                self.is_right = False
                self.left_go = False
                self.right_go = False
                self.rect.x -= 5
            else:
                self.left_go = False
            if self.n == 40:
                self.n = 0
            if self.n % 4 == 0:
                if self.right_animation:
                    self.image = pygame.image.load(f'data//images//hero//moving//right_go_'
                                                   f'{self.n // 4}.png').convert_alpha()
                if self.left_animation:
                    self.image = pygame.image.load(f'data//images//hero//moving//left_go_'
                                                   f'{self.n // 4}.png').convert_alpha()
            self.n += 1
        if self.jump_flag:  # Прыжок
            if self.jump_count == 0:
                self.jump_count = 200
                self.jump_flag = False
            if 0 < self.jump_count <= 100:  # Если вдруг счетчик стал меньше или равен половине, то он падает
                self.rect.y += 5
            else:
                self.rect.y -= 5
            self.jump_count -= 5


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((200, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

    def return_hp(self):
        global HERO_XP
        return HERO_XP

    def is_died(self):
        global HERO_XP
        if HERO_XP <= 0:
            return True

    def set_hp(self):
        global HERO_XP
        HERO_XP = 200


class Bullet(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Bullet, self).__init__(*group)
        self.image = pygame.Surface((20, 5))
        self.rect = self.image.get_rect()
        self.reverse = False

    def update(self):
        if self.reverse:
            self.rect.x -= 30
        else:
            self.rect.x += 30

    def set_pos(self, x, y, reverse):
        self.rect.x = x
        self.rect.y = y
        self.reverse = reverse
