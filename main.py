import pygame
import ctypes
import time
import random
from data.objects.hero import Hero, HealthBar, Bullet  # Класс с главным героем
from data.objects.button import Button  # Класс с кнопками
from data.objects.dialog import DialogWindow, DialogButtonExit, show_flag  # Классы с элементами для диалогового окна
from data.objects.monster import Monster, return_monster_count, set_monster_count, KILLERS

pygame.init()
pygame.mixer.init()
size = width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.image.load("data//images//enemy//blood.png").convert_alpha()]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(blood_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 5

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(0, 0,
                                     ctypes.windll.user32.GetSystemMetrics(0),
                                     ctypes.windll.user32.GetSystemMetrics(1)):
            self.kill()


if __name__ == "__main__":
    """Инициализация групп спрайтов"""
    sprites = pygame.sprite.Group()  # Группа спрайтов
    buttons = pygame.sprite.Group()  # Группа кнопок
    dialog_parts = pygame.sprite.Group()  # Диалоговое окно
    monsters = pygame.sprite.Group()  # Враги
    blood_group = pygame.sprite.Group()
    shoots = pygame.sprite.Group()  # Пули
    game_over_group = pygame.sprite.Group()
    game_over_animation_flag = False
    LIVING_TIME = time.time()
    monsters_count = 0
    bit_time = time.time()
    my_font = pygame.font.SysFont("Comic Sans MS", 40)
    game_over_animation_img = pygame.image.load("data//images//buttons and windows//game_over.png")
    game_over_animation_img = pygame.transform.scale(game_over_animation_img,
                                                     (ctypes.windll.user32.GetSystemMetrics(0),
                                                      ctypes.windll.user32.GetSystemMetrics(1)))
    score_img = pygame.image.load("data//images//buttons and windows//score.png")
    score_img = pygame.transform.scale(score_img, ((ctypes.windll.user32.GetSystemMetrics(0),
                                                    512)))
    score_count = 0
    game_over_animation_count = 0
    """Спрайты"""
    hero = Hero(sprites)  # Спрайт главного героя
    bar = HealthBar(sprites)
    start_button = Button(buttons)
    start_button.set_parameters(image_url="data//images//buttons and windows//start.png",  # Кнопка старта
                                hover_image_url="data//images//buttons and windows//start_hover.png",
                                x=ctypes.windll.user32.GetSystemMetrics(0) // 2 - 300,
                                y=ctypes.windll.user32.GetSystemMetrics(1) // 2 - 100)
    continue_btn = Button(game_over_group)
    continue_btn.set_parameters(image_url="data//images//buttons and windows//continue.png",
                                hover_image_url="data//images//buttons and windows//continue_hover.png",
                                x=700, y=500)

    background_image = pygame.image.load("data/images/buttons and windows/background.gif")  # Картинка на фоне игры
    background_image = pygame.transform.scale(background_image, (ctypes.windll.user32.GetSystemMetrics(0),
                                                                 ctypes.windll.user32.GetSystemMetrics(1)))

    # Настройка и создание диалогового окна из частей
    dialog_window = DialogWindow(dialog_parts)  # Диалоговое окно
    dialog_window.set_parameters(x=ctypes.windll.user32.GetSystemMetrics(0) // 2 - 100,
                                 y=ctypes.windll.user32.GetSystemMetrics(1) // 2 - 200,
                                 width=200, height=200,
                                 background_color=(100, 102, 100))

    dialog_btn = DialogButtonExit(dialog_parts)  # Кнопка выхода из диалогового окна
    dialog_btn.set_pos(x=ctypes.windll.user32.GetSystemMetrics(0) // 2 + 70,
                       y=ctypes.windll.user32.GetSystemMetrics(1) // 2 - 200)

    """Инициализация музыки"""
    main_music = pygame.mixer.Sound("data//music//main_window.wav")  # Музыка диалоговых окон и главного меню
    shoot_music = pygame.mixer.Sound("data//music//shoot.wav")  # Звук выстрела
    game_music = pygame.mixer.Sound("data//music//game_music.wav")  # Музыка игры на фоне
    main_music.play(-1)  # Запуск главной музыки

    """Игра"""
    fps = 60
    clock = pygame.time.Clock()
    running = True
    start_window = True
    start_time = time.time()
    while running:  # Цикл игры
        if pygame.key.get_pressed()[pygame.K_a]:  # Бег влево
            hero.left_()
        if pygame.key.get_pressed()[pygame.K_d]:  # Бег вправо
            hero.right_()
        if pygame.key.get_pressed()[pygame.K_w]:  # Прыжок
            hero.jump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:  # Если игрок esc нажал, то заходит в меню
            dialog_btn.set_flag()
        if pygame.key.get_pressed()[pygame.K_SPACE]:  # Если игрок esc нажал, то заходит в меню
            game_over_animation_flag = False
            bar.set_hp()
            score_count = 0
            game_over_animation_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not start_window:
                    shoot_music.play()
                    if hero.is_right:
                        h = Bullet(shoots)
                        h.set_pos(hero.rect.x + 165, hero.rect.y + 115, False)
                    else:
                        h = Bullet(shoots)
                        h.set_pos(hero.rect.x + 4, hero.rect.y + 115, True)
                    for monster in KILLERS:
                        if pygame.sprite.spritecollide(monster, shoots, False):
                            monster.set_xp()
                    dialog_btn.check_click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                else:
                    if start_button.image == start_button.hover_image:
                        monsters.empty()
                        KILLERS.clear()
                        main_music.stop()
                        game_music.play()
                        buttons.empty()
                        start_window = False
                        LIVING_TIME = time.time()
                        start_time = time.time()

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        if start_window:  # Обновление всего
            buttons.draw(screen)
            buttons.update(pygame.event.get())
        else:
            dialog_parts.draw(screen)
            monsters.draw(screen)
            monsters.update(hero.rect.x, hero.rect.y)
            dialog_parts.update()
            sprites.draw(screen)
            sprites.update()
            shoots.draw(screen)
            shoots.update()
            if bar.is_died():
                buttons.add(start_button)
                start_window = True
                singleplayer = False
                bar.set_hp()
                LIVING_TIME = round(time.time() - LIVING_TIME)
                print(LIVING_TIME)
                print(return_monster_count())
                monsters_count = return_monster_count()
                set_monster_count()
                game_over_animation_flag = True
                game_music.stop()
                main_music.play()
                dialog_btn.set_flag()
            if pygame.sprite.spritecollide(hero, monsters, False):
                hero.set_xp()
                if time.time() - bit_time >= 1:
                    numbers = range(-10, 10)
                    for _ in range(20):
                        Particle((hero.rect.x + 50, hero.rect.y + 50),
                                 random.choice(numbers),
                                 random.choice(numbers))
                    bit_time = time.time()
            dialog_parts.draw(screen)
            dialog_parts.update()
            sprites.draw(screen)
            sprites.update()
            if bar.return_hp() >= 0:
                pygame.draw.rect(screen, (255, 0, 0), (50 + bar.return_hp(), 50, 200 - bar.return_hp(), 20))
            if time.time() - start_time >= 10:
                KILLERS.append(Monster(monsters))
                start_time = time.time()
        if dialog_btn.return_flag and not game_over_animation_flag and not start_window:
            font = pygame.font.SysFont("Comic Sans MS", 40)
            screen.blit(font.render(f"You kill {return_monster_count()}", False, (0, 0, 225)), (
                ctypes.windll.user32.GetSystemMetrics(0) // 2 - 90,
                ctypes.windll.user32.GetSystemMetrics(1) // 2 - 140,))
            screen.blit(font.render(f"Time {round(time.time() - LIVING_TIME)}", False, (0, 0, 225)), (
                ctypes.windll.user32.GetSystemMetrics(0) // 2 - 90,
                ctypes.windll.user32.GetSystemMetrics(1) // 2 - 100,))
        if game_over_animation_flag:
            screen.blit(game_over_animation_img, (game_over_animation_count - 1000, 0))
            if game_over_animation_count < 990:
                game_over_animation_count += 15
            else:
                screen.blit(score_img, (0, ctypes.windll.user32.GetSystemMetrics(1) - score_count))
                if score_count < 500:
                    score_count += 15
                else:
                    screen.blit(my_font.render(str(monsters_count), False, (0, 0, 225)), (350, 420))
                    screen.blit(my_font.render(str(round(LIVING_TIME)), False, (0, 0, 225)), (320, 495))
                    screen.blit(my_font.render(str(return_monster_count() * 100 + LIVING_TIME * 50), False,
                                               (0, 0, 225)), (390, 575))
                    screen.blit(my_font.render("Press space to continue", False, (0, 0, 225)), (500, 700))
        blood_group.draw(screen)
        blood_group.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
