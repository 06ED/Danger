import pygame
import random
import ctypes

monster_xp = 100
KILLED_MONSTER_COUNT = 0
KILLERS = []


class Monster(pygame.sprite.Sprite):
    group = pygame.sprite.Group()

    def __init__(self, *group):
        super(Monster, self).__init__(*group)
        self.image = pygame.image.load("data//images//enemy//right.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, ctypes.windll.user32.GetSystemMetrics(0) - self.image.get_rect()[2])
        self.rect.y = ctypes.windll.user32.GetSystemMetrics(1) - self.image.get_rect()[3]
        self.uron = False
        self.n = 0
        self.is_right = True
        pygame.sprite.Sprite.__init__(Monster.group)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def isuron(self):
        return self.uron

    def set_xp(self):
        global monster_xp
        monster_xp -= 10

    def update(self, x, y):
        global monster_xp, KILLED_MONSTER_COUNT
        if monster_xp % 100 == 0 and monster_xp != 100:
            KILLERS.remove(self)
            self.kill()
            monster_xp = 100
            print("died")
            KILLED_MONSTER_COUNT += 1

        else:
            if x == self.rect.x:
                if self.is_right:
                    self.image = pygame.image.load('data/images/enemy/right.png')
                else:
                    self.image = pygame.image.load('data/images/enemy/left.png')
                self.n = 0
                self.uron = True
            else:
                if self.n == 60:
                    self.n = 0
                if x > self.rect.x:
                    self.rect.x += 2
                    self.is_right = True
                    if self.n % 6 == 0:
                        self.image = pygame.image.load(f'data/images/enemy/moving/right_go_{self.n // 6}.png')
                else:
                    self.rect.x -= 2
                    self.is_right = False
                    if self.n % 6 == 0:
                        self.image = pygame.image.load(f'data/images/enemy/moving/left_go_{self.n // 6}.png')
                self.uron = False
                self.n += 1


def return_monster_count():
    global KILLED_MONSTER_COUNT
    return KILLED_MONSTER_COUNT


def set_monster_count():
    global KILLED_MONSTER_COUNT
    KILLED_MONSTER_COUNT = 0
