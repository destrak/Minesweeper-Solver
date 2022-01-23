import pickle
import pygame
from field import Field
from solver import Solver


class Game:

    # Конструктор
    def __init__(self,
                 height=900,
                 width=900,
                 cell_size=90,
                 bomb_number=20,
                 fps=60,
                 saved_field=None
                 ):

        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.res = width, height
        self.surface = pygame.display.set_mode(self.res)

        self.cell_height = self.height // self.cell_size
        self.cell_width = self.width // self.cell_size

        self.bomb_number = bomb_number

        if saved_field is None:
            self.field = Field(self.cell_height, self.cell_width, self.bomb_number)
        else:
            self.field = saved_field

        self.fps = fps

        self.game_is_over_ = False

        self.colors = ['lightcyan', 'lightcoral', 'yellow1',
                       'mediumpurple1', 'midnightblue', 'mistyrose4',
                       'salmon4', 'sienna1', 'thistle4']

        self.font_size = cell_size // 3

    # Отрисовка сетки
    def DrawGrid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.surface,
                pygame.Color('black'),
                (x, 0),
                (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.surface,
                pygame.Color('black'),
                (0, y),
                (self.width, y)
            )

    # Заливка клеток
    def DrawRect(self, bias, x, y, color):
        pygame.draw.rect(
            self.surface,
            pygame.Color(color),
            (y * bias + 1, x * bias + 1, bias - 1, bias - 1)
        )

    # Отрисовка клеток
    def DrawCells(self):
        bias = self.cell_size
        player_field = self.field.Render()
        pygame.font.init()
        font_renderer = pygame.font.SysFont('courier', self.font_size)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                self.DrawRect(bias, i, j, 'gray')
                number = str(player_field[i][j])
                if player_field[i][j] == '-':
                    color = 'gray'
                elif player_field[i][j] == 'F':
                    color = 'black'
                    self.DrawRect(bias, i, j, 'white')
                elif player_field[i][j] == '*':
                    color = 'black'
                    self.DrawRect(bias, i, j, 'red')
                else:
                    color = self.colors[int(player_field[i][j])]
                    self.DrawRect(bias, i, j, 'dimgray')

                if number == ' ':
                    continue

                label = font_renderer.render(
                    number,
                    True,
                    color
                )

                self.surface.blit(
                    label,
                    (j * bias + bias // 2 - self.font_size // 4,
                     i * bias + bias // 2 - self.font_size // 2)
                )

    # Закончилась ли игра
    def GameIsOver(self) -> bool:
        height, width = self.field.GetSize()
        revealed = self.field.GetRevealed()
        if len(revealed) >= height * width - self.bomb_number:
            self.game_is_over_ = True
            return True
        else:
            return False

    # Запуск без решения
    def Run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Minesweeper')
        self.surface.fill(pygame.Color('dimgray'))
        condition = True
        while condition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    condition = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        pos = pygame.mouse.get_pos()
                        x, y = [
                            pos[1] // self.cell_size,
                            pos[0] // self.cell_size,
                        ]
                        passed = self.field.Reveal(x, y)
                        if not passed:
                            condition = False
                            self.game_is_over_ = True
                    if pygame.mouse.get_pressed(3)[2]:
                        pos = pygame.mouse.get_pos()
                        x, y = [
                            pos[1] // self.cell_size,
                            pos[0] // self.cell_size,
                        ]
                        self.field.Flag(x, y)
            self.DrawGrid()
            self.DrawCells()
            pygame.display.update()
            clock.tick(self.fps)
            if self.GameIsOver():
                condition = False
        pygame.quit()

    # Запуск с решением
    def RunSolved(self):
        self.field.Reveal(0, 0)
        condition = True
        clock = pygame.time.Clock()
        pygame.display.set_caption('Minesweeper')
        self.surface.fill(pygame.Color('dimgray'))
        while condition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    condition = False

            r = self.field.Render()
            height, width = self.field.GetSize()
            solver = Solver(r, height, width)
            solver.Run()
            prediction = solver.MakePrediction()
            x, y = prediction[0], prediction[1]
            passed = self.field.Reveal(x, y)
            if not passed:
                condition = False
                self.game_is_over_ = True
            self.DrawGrid()
            self.DrawCells()
            pygame.display.update()
            clock.tick(self.fps)
            if self.GameIsOver():
                condition = False

    # Сохранение поля
    def MakeSave(self):
        if self.game_is_over_:
            f = open('data.pickle', 'rb')
            f.close()
        else:
            field = self.field
            f = open('data.pickle', 'wb')
            pickle.dump(field, f)
            f.close()
