import pygame

show_flag = False  # Общий флаг для всех диалоговых окон


class DialogWindow(pygame.sprite.Sprite):  # Класс самого окна
    def __init__(self, *group):
        super().__init__(*group)

    def set_parameters(self, x, y, width, height, background_color=(255, 255, 255)):
        self.field = pygame.Surface((width, height))
        self.field.fill(background_color)
        self.rect = self.field.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = self.field

    def update(self):
        global show_flag
        if not show_flag:
            self.image = pygame.Surface((0, 0))
        else:
            self.image = self.field


class DialogButtonExit(pygame.sprite.Sprite):  # Класс кнопки закрытия окна
    def __init__(self, *group):
        super().__init__(*group)
        self.image_exit = pygame.image.load("data//images//buttons and windows//button_exit.png")
        self.image = self.image_exit
        self.hidden_img = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.flag = False

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def check_click(self, x, y):
        global show_flag
        if self.rect.collidepoint(x, y):
            show_flag = False

    def set_flag(self):
        global show_flag
        show_flag = True

    def set_false_flag(self):
        global show_flag
        show_flag = True

    def return_flag(self):
        global show_flag
        return show_flag

    def update(self):
        global show_flag
        if not show_flag:
            self.image = self.hidden_img
            show_flag = False
        else:
            self.image = self.image_exit
            show_flag = True
