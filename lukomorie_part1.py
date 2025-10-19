import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1030
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лукоморье 1")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
PURPLE = (100, 0, 200)

# Шрифты
font_small = pygame.font.SysFont('Arial', 24)
font_medium = pygame.font.SysFont('Arial', 36)
font_large = pygame.font.SysFont('Arial', 48)
font_huge = pygame.font.SysFont('Arial', 72)

# --- Загрузка фона ---
try:
    # Замените 'lukomorie_board.jpg' на имя вашего файла
    board_image = pygame.image.load("lukomorie_board.jpg")
    board_image = pygame.transform.scale(board_image, (SCREEN_WIDTH - 300, SCREEN_HEIGHT))
except FileNotFoundError:
    print("⚠️ Файл 'lukomorie_board.jpg' не найден. Используется заглушка.")
    board_image = pygame.Surface((SCREEN_WIDTH - 300, SCREEN_HEIGHT))
    board_image.fill(GREEN)
    pygame.draw.rect(board_image, BLACK, (0, 0, SCREEN_WIDTH - 300, SCREEN_HEIGHT), 2)
    text = font_medium.render("Фоновая доска Лукоморья", True, WHITE)
    board_image.blit(text, (10, 10))

# --- Координаты клеток (приблизительно) ---
CELL_POSITIONS = {
    1: (100, 150),
    2: (250, 300),
    3: (400, 400),
    4: (150, 500),
    5: (300, 600),
    6: (450, 500),
    7: (550, 300),
    8: (600, 400),
    9: (700, 500),
    10: (800, 300),
    11: (900, 400),
    12: (1000, 300),
    13: (1100, 500),
}

# --- Граф переходов ---
TRANSITIONS = {
    1: [2],
    2: [3, 4, 5],
    3: [6],
    4: [7],
    5: [8],
    6: [9],
    7: [10],
    8: [11],
    9: [12],
    10: [11, 12, 13],
    11: [12],
    12: [13],
    13: []
}

# Класс игрока
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 1
        self.bon = 0
        self.inventory = [None, None, None]
        self.skip_turn = False
        self.in_mini_game = False

    def roll_dice(self):
        return random.randint(1, 6)

    def move_to_cell(self, target_cell):
        if target_cell in TRANSITIONS[self.position]:
            self.position = target_cell
            print(f"Игрок переместился на клетку {target_cell}")
            return True
        else:
            print(f"Нельзя перейти с {self.position} на {target_cell}")
            return False

    def handle_cell(self, cell_number):
        if cell_number == 2:
            self.handle_waystone()
        elif cell_number == 3:
            self.start_mini_game("Кот Учёный")
        elif cell_number == 4:
            self.get_treasure()
        elif cell_number == 5:
            self.start_mini_game("Царевна Лягушка")
            self.skip_turn = False
        elif cell_number in [6]:
            self.skip_turn = True
            print("Леший и Шишига защекотали вас! Пропуск хода.")
        elif cell_number == 7:
            self.get_big_treasure()
        elif cell_number == 8:
            self.skip_turn = True
            print("Леший пригласил выпить чаю. Пропуск хода.")
        elif cell_number == 9:
            loss = self.roll_dice()
            self.bon -= loss
            if self.bon < 0:
                self.bon = 0
            self.skip_turn = True
            print(f"Разбойники отняли {loss} бон. Пропуск хода.")
        elif cell_number == 10:
            self.handle_crossroad()
        elif cell_number == 11:
            self.handle_goose()
        elif cell_number == 12:
            self.handle_repkа_question()
        elif cell_number == 13:
            self.handle_baba_yaga()

    def handle_waystone(self):
        dice = self.roll_dice()
        print(f"Вы бросили кубик: {dice}")
        if dice in [1, 2]:
            self.move_to_cell(3)
            print("Вы идёте налево -> к Коту Учёному (клетка 3)")
        elif dice in [3, 4]:
            self.move_to_cell(4)
            print("Вы идёте прямо -> к Кладу (клетка 4)")
        else:
            self.move_to_cell(5)
            print("Вы идёте направо -> к Болоту (клетка 5)")

    def get_treasure(self):
        dice1 = self.roll_dice()
        dice2 = self.roll_dice()
        bon = dice1 + dice2
        self.bon += bon
        print(f"Вы получили {bon} бон из клада!")

    def get_big_treasure(self):
        dice1 = self.roll_dice()
        dice2 = self.roll_dice()
        dice3 = self.roll_dice()
        bon = dice1 + dice2 + dice3
        self.bon += bon
        print(f"Вы получили {bon} бон из огромного клада!")

    def handle_crossroad(self):
        dice = self.roll_dice()
        print(f"Вы бросили кубик: {dice}")
        if dice in [1, 2]:
            self.move_to_cell(11)
            print("Вы идёте прямо -> к Гусю (клетка 11)")
        elif dice in [3, 4]:
            self.move_to_cell(12)
            print("Вы идёте вверх -> к Репке (клетка 12)")
        else:
            self.move_to_cell(13)
            print("Вы идёте вниз -> к Избушке Бабы Яги (клетка 13)")

    def handle_goose(self):
        new_pos = random.randint(1, 13)
        self.position = new_pos
        print(f"Гусь перенес вас на клетку {new_pos}")

    def handle_repkа_question(self):
        answer = input("Сколько действующих лиц в сказке о репке? (Введите число): ")
        try:
            num = int(answer)
            if num == 7:
                self.move_to_cell(7)
                print("Правильно! Вы перешли на клетку 7 (Огромный клад).")
            else:
                print("Неверно! Остаётесь на месте.")
        except ValueError:
            print("Неверный ввод. Остаётесь на месте.")

    def handle_baba_yaga(self):
        if self.bon >= 20:
            print("У вас есть 20 бон! Баба Яга радостно продала вам Волшебный клубок!")
            self.inventory[0] = "Волшебный клубок"
            print("🎉 Поздравляем! Вы завершили Лукоморье 1!")
        else:
            print("У вас недостаточно бон! Баба Яга отправляет вас обратно к Коту Учёному (клетка 3).")
            self.position = 3

    def start_mini_game(self, title):
        self.in_mini_game = True
        mini_game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        mini_game_screen.fill(BLACK)
        text = font_large.render(f"Мини-игра: {title}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        mini_game_screen.blit(text, text_rect)
        pygame.display.flip()
        print(f"Запущена мини-игра: {title}")

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    self.in_mini_game = False
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Создание игрока
player = Player("Игрок 1", RED)

# --- Класс для визуального барабана ---
class DiceWheel:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = 0
        self.spinning = False
        self.speed = 0
        self.target_angle = 0
        self.result = 0
        self.colors = [
            (255, 0, 0),      # 1 - красный
            (255, 127, 0),    # 2 - оранжевый
            (255, 255, 0),    # 3 - желтый
            (0, 255, 0),      # 4 - зеленый
            (0, 0, 255),      # 5 - синий
            (127, 0, 255),    # 6 - фиолетовый
        ]
        self.font = font_large

    def spin(self):
        """Запустить вращение"""
        self.spinning = True
        self.speed = random.uniform(10, 20)  # Начальная скорость
        self.result = random.randint(1, 6)   # Какое число выпадет
        # Вычисляем целевой угол (чтобы стрелка указывала на нужное число)
        self.target_angle = (self.result - 1) * (2 * math.pi / 6) + math.pi / 6

    def update(self):
        """Обновить состояние барабана"""
        if not self.spinning:
            return

        # Замедление
        self.speed *= 0.98
        if self.speed < 0.1:
            self.speed = 0
            self.spinning = False
            # Округляем угол к ближайшему числу
            self.angle = self.target_angle

        # Обновляем угол
        self.angle += self.speed

    def draw(self, screen):
        """Нарисовать барабан"""
        # Фон колеса
        pygame.draw.circle(screen, PURPLE, (self.center_x, self.center_y), self.radius + 10)
        pygame.draw.circle(screen, WHITE, (self.center_x, self.center_y), self.radius, 5)

        # Сектора
        for i in range(6):
            start_angle = self.angle + i * (2 * math.pi / 6)
            end_angle = start_angle + (2 * math.pi / 6)
            # Рисуем сектор
            points = [(self.center_x, self.center_y)]
            for j in range(100):
                angle = start_angle + (end_angle - start_angle) * j / 100
                x = self.center_x + self.radius * math.cos(angle)
                y = self.center_y + self.radius * math.sin(angle)
                points.append((x, y))
            points.append((self.center_x, self.center_y))
            pygame.draw.polygon(screen, self.colors[i], points)

            # Число в секторе
            text_angle = start_angle + (2 * math.pi / 12)
            text_x = self.center_x + (self.radius - 50) * math.cos(text_angle)
            text_y = self.center_y + (self.radius - 50) * math.sin(text_angle)
            text_surface = self.font.render(str(i + 1), True, WHITE)
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            screen.blit(text_surface, text_rect)

        # Центральная кнопка
        button_radius = 80
        button_color = GREEN
        if self.spinning:
            button_color = (0, 150, 0)
        pygame.draw.circle(screen, button_color, (self.center_x, self.center_y), button_radius)
        if not self.spinning:
            arrow = font_huge.render("↻", True, WHITE)
            arrow_rect = arrow.get_rect(center=(self.center_x, self.center_y))
            screen.blit(arrow, arrow_rect)
        else:
            # Показываем результат в центре
            result_text = font_huge.render(str(self.result), True, WHITE)
            result_rect = result_text.get_rect(center=(self.center_x, self.center_y))
            screen.blit(result_text, result_rect)

        # Стрелка сверху
        triangle_points = [
            (self.center_x - 15, self.center_y - self.radius - 10),
            (self.center_x + 15, self.center_y - self.radius - 10),
            (self.center_x, self.center_y - self.radius - 30)
        ]
        pygame.draw.polygon(screen, BLUE, triangle_points)

    def is_spinning(self):
        return self.spinning

    def get_result(self):
        return self.result

# Создание барабана
wheel = DiceWheel(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2, 150)

# UI элементы
INVENTORY_RECT = pygame.Rect(SCREEN_WIDTH - 300, 100, 280, 100)
BON_DISPLAY_RECT = pygame.Rect(SCREEN_WIDTH - 300, 250, 280, 50)

# Основной цикл игры
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if wheel.is_spinning() is False and not player.skip_turn:
                # Запускаем вращение
                wheel.spin()
            elif not player.skip_turn:
                # Если не крутится — обрабатываем результат
                if wheel.is_spinning() is False:
                    dice_roll = wheel.get_result()
                    print(f"Вы бросили: {dice_roll}")
                    player.handle_cell(player.position)
                    if player.skip_turn:
                        print("Пропуск хода активирован.")
                    else:
                        print(f"Вы на клетке {player.position}")

    # Очистка экрана
    screen.fill(WHITE)

    # --- Отрисовка фоновой доски ---
    screen.blit(board_image, (0, 0))

    # --- Отрисовка фишки игрока ---
    if player.position in CELL_POSITIONS:
        token_x, token_y = CELL_POSITIONS[player.position]
        pygame.draw.circle(screen, player.color, (token_x, token_y), 15)
        token_label = font_small.render(str(player.position), True, WHITE)
        screen.blit(token_label, (token_x - 5, token_y - 10))

    # --- Отрисовка барабана ---
    wheel.update()
    wheel.draw(screen)

    # --- UI: Инвентарь ---
    pygame.draw.rect(screen, GRAY, INVENTORY_RECT)
    inv_text = font_small.render("Инвентарь:", True, BLACK)
    screen.blit(inv_text, (INVENTORY_RECT.x + 5, INVENTORY_RECT.y + 5))
    for i, item in enumerate(player.inventory):
        item_text = font_small.render(item or "Пусто", True, BLACK)
        screen.blit(item_text, (INVENTORY_RECT.x + 5, INVENTORY_RECT.y + 30 + i*20))

    # --- UI: Счётчик бон ---
    pygame.draw.rect(screen, YELLOW, BON_DISPLAY_RECT)
    bon_text = font_medium.render(f"Боны: {player.bon}", True, BLACK)
    screen.blit(bon_text, (BON_DISPLAY_RECT.x + 10, BON_DISPLAY_RECT.y + 10))

    # --- Если в мини-игре — не обновляем основной экран ---
    if player.in_mini_game:
        continue

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()