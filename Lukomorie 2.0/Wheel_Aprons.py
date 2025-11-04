import pygame
import random
import math

class DiceWheel:
    def __init__(self, center_x, center_y, radius, font_large, font_huge):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = 0  # текущий угол поворота колеса
        self.spinning = False
        self.speed = 0
        self.dice = 0
        self.colors = [
            (203, 65, 84),      # 1
            (255, 127, 0),      # 2
            (255, 207, 64),     # 3
            (140, 203, 94),     # 4
            (66, 133, 180),     # 5
            (123, 104, 238),    # 6
        ]
        self.font = font_large
        self.font_huge = font_huge
        self.light_blue = (0, 153, 125)
        self.PURPLE = (100, 0, 200)
        self.arrow_angle = math.pi  # стрелка слева - 180 = радиан

    def spin(self):
        """Запустить вращение"""
        self.spinning = True
        self.speed = random.uniform(10, 20)
        self.dice = 0  # сброс результата

    def update(self):
        """Обновить состояние барабана"""
        if not self.spinning:
            return

        self.speed *= 0.98
        if self.speed < 0.1:
            self.speed = 0
            self.spinning = False
            # После остановки определяем, какой сектор под стрелкой
            self._calculate_dice_from_angle()
        self.angle += self.speed

    def _calculate_dice_from_angle(self):
        '''Определяет, какой сектор находится под стрелкой (угол = π)
        Общий угол колеса: self.angle
        Стрелка неподвижна и смотрит на угол π (влево)
        Нам нужно найти, какой сектор колеса сейчас в точке угла π

        Приведём текущий угол колеса к диапазону [0, 2π)'''
        normalized_angle = self.angle % (2 * math.pi)

        # Угол сектора под стрелкой = (π - normalized_angle) mod 2π
        # Потому что колесо вращается, а стрелка — фиксирована
        sector_angle = (self.arrow_angle - normalized_angle) % (2 * math.pi)

        # Каждый сектор занимает 2π/6 радиан
        sector_index = int(sector_angle / (2 * math.pi / 6)) % 6  # 0..5

        '''Секторы идут по часовой стрелке? В вашем draw — да, т.к. angle растёт → поворот против часовой?
        Но визуально: при angle=0, сектор 1 (красный) начинается с угла 0 → вправо.
        А стрелка слева → угол π → должен соответствовать сектору 4 (если 1 — справа).
        Однако в вашем коде секторы рисуются в порядке 1,2,3,4,5,6 против часовой стрелки.
        Чтобы совпало с визуалом, инвертируем порядок:
        На самом деле проще: проверим, что при angle = 0, сектор 1 — справа → стрелка слева = сектор 4.
        Но вы хотите, чтобы выпадало число, которое **остановилось у стрелки**.
        Поскольку вы не используете геометрию для генерации результата, а только для отображения,
        и чтобы не ломать логику — сделаем так:
        Мы просто пронумеруем сектора от стрелки против часовой стрелки: 1,2,3,4,5,6.

        Но в вашем текущем коде сектор 1 рисуется от угла `self.angle + 0`
        при angle=0, сектор 1 — справа (угол 0), сектор 2 — вверху-справа и т.д.
        Стрелка слева = угол π → это середина сектора с индексом 3 (если 0=справа).
        Поэтому: чтобы сектор под стрелкой был "1", когда он там — нужно сдвинуть.

        Однако вы просите: **число на секторе, который остановился напротив стрелки**.
        В текущей отрисовке: сектор i имеет число (i+1), и расположен от угла `self.angle + i * step`.
        Значит, чтобы найти, какое число напротив стрелки (угол π), решаем:
        self.angle + i * step ≈ π - step/2 (середина сектора)
        => i ≈ (π - step/2 - self.angle) / step'''

        step = 2 * math.pi / 6
        # Найдём индекс сектора, чья середина ближе всего к стрелке (π)
        best_i = 0
        min_diff = float('inf')
        for i in range(6):
            sector_center = (self.angle + i * step + step / 2) % (2 * math.pi)
            diff = abs((sector_center - self.arrow_angle + math.pi) % (2 * math.pi) - math.pi)
            if diff < min_diff:
                min_diff = diff
                best_i = i

        # Число на этом секторе — (best_i + 1)
        self.dice = best_i + 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.PURPLE, (self.center_x, self.center_y), self.radius + 10)
        pygame.draw.circle(screen, (255, 255, 255), (self.center_x, self.center_y), self.radius, 5)

        for i in range(6):
            start_angle = self.angle + i * (2 * math.pi / 6)
            end_angle = start_angle + (2 * math.pi / 6)
            points = [(self.center_x, self.center_y)]
            for j in range(100):
                angle = start_angle + (end_angle - start_angle) * j / 100
                x = self.center_x + self.radius * math.cos(angle)
                y = self.center_y + self.radius * math.sin(angle)
                points.append((x, y))
            points.append((self.center_x, self.center_y))
            pygame.draw.polygon(screen, self.colors[i], points)

            text_angle = start_angle + (2 * math.pi / 12)
            text_x = self.center_x + (self.radius - 50) * math.cos(text_angle)
            text_y = self.center_y + (self.radius - 50) * math.sin(text_angle)
            text_surface = self.font.render(str(i + 1), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            screen.blit(text_surface, text_rect)

        button_radius = 80
        button_color = self.light_blue
        if self.spinning:
            button_color = (2, 139, 87)
        pygame.draw.circle(screen, button_color, (self.center_x, self.center_y), button_radius)

        if not self.spinning:
            arrow = self.font_huge.render("start", True, (255, 255, 255))
            arrow_rect = arrow.get_rect(center=(self.center_x, self.center_y))
            screen.blit(arrow, arrow_rect)

        triangle_points = [
            (self.center_x - self.radius, self.center_y - 15),
            (self.center_x - self.radius, self.center_y + 15),
            (self.center_x - self.radius + 30, self.center_y)
        ]
        pygame.draw.polygon(screen, (0, 0, 0), triangle_points)

    def is_spinning(self):
        return self.spinning

    def get_dice_result(self):
        #Возвращает число на секторе, остановившемся напротив стрелки
        return self.dice