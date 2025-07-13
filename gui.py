import sys

import pygame
import time
import os
import pickle
from game import Game
import time

class GUI:

    def __init__(
            self,
            height=800,
            width=800,
            cell_size=50,
            bomb_number=40,
            fps=60
    ):

        self.clock = None
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.res = width, height
        self.surface = pygame.display.set_mode(self.res)

        self.cell_height = self.height // self.cell_size
        self.cell_width = self.width // self.cell_size

        self.bomb_number = bomb_number

        self.fps = fps

        self.colors = [
            'lightcyan', 'lightcoral', 'yellow1',
            'mediumpurple1', 'midnightblue', 'mistyrose4',
            'salmon4', 'sienna1', 'thistle4'
        ]

        pygame.font.init()
        self.button_width, self.button_height = cell_size * 3, cell_size
        self.font_size = cell_size // 3
        self.font = pygame.font.SysFont('courier', self.font_size)
        self.game = Game(self.cell_height, self.cell_width, self.bomb_number)

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

    def DrawText(self, text, color, x, y, width=0, height=0):
        label = self.font.render(
            text,
            True,
            color
        )
        self.surface.blit(
            label,
            (
                x + (width / 2 - label.get_width() / 2),
                y + (height / 2 - label.get_height() / 2)
            )
        )

    def DrawButton(self, x, y, width, height, color):
        button = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.surface, color, button)
        return button

    def FillCell(self, bias, x, y, color):
        pygame.draw.rect(
            self.surface,
            pygame.Color(color),
            (y * bias + 1, x * bias + 1, bias - 1, bias - 1)
        )

    def DrawCells(self, player_field):
        margin = self.cell_size
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                self.FillCell(margin, i, j, 'gray')
                sign = str(player_field[i][j])
                if player_field[i][j] == '-':
                    color = 'gray'
                elif player_field[i][j] == 'F':
                    color = 'black'
                    self.FillCell(margin, i, j, 'white')
                elif player_field[i][j] == '*':
                    color = 'black'
                    self.FillCell(margin, i, j, 'red')
                else:
                    color = self.colors[int(player_field[i][j])]
                    self.FillCell(margin, i, j, 'dimgray')

                if sign == ' ':
                    continue

                self.DrawText(
                    sign,
                    color,
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

    def Run(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        condition = True
        while condition:
            pygame.display.set_caption('Main Menu')
            self.game = Game(self.cell_height, self.cell_width, self.bomb_number)
            self.surface.fill(pygame.Color('dimgray'))
            self.DrawText('Main Menu', 'white', 100, 50)

            button_1 = self.DrawButton(
                50, 100,
                self.button_width,
                self.button_height,
                'lightcyan'
            )
            button_2 = self.DrawButton(
                50, 200,
                self.button_width,
                self.button_height,
                'lightcoral'
            )
            self.DrawText(
                'Regular Game',
                'black',
                50,
                100,
                self.button_width,
                self.button_height
            )
            self.DrawText(
                'Solver',
                'black',
                50,
                200,
                self.button_width,
                self.button_height
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    condition = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        condition = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        mx, my = pygame.mouse.get_pos()
                        if button_1.collidepoint((mx, my)):
                            if self.GameInProgress():
                                self.AskForCheckpoint()
                            self.RegularGame()
                            time.sleep(0.5)
                        if button_2.collidepoint((mx, my)):
                            self.SolvedGame()
                            time.sleep(0.5)
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()

    def RegularGame(self):
        condition = True
        pygame.display.set_caption('Regular Game')
        self.surface.fill(pygame.Color('dimgray'))
        while condition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.MakeSave('data.pickle')
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.MakeSave('data.pickle')
                        condition = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = [
                        pos[1] // self.cell_size,
                        pos[0] // self.cell_size,
                    ]
                    if pygame.mouse.get_pressed(3)[0]:
                        passed = self.game.Next('reveal', x, y)
                        if not passed:
                            self.game.MakeSave('data.pickle', game_is_over=True)
                            condition = False
                    if pygame.mouse.get_pressed(3)[2]:
                        self.game.Next('flag', x, y)
            self.DrawGrid()
            self.DrawCells(self.game.GetPlayerField())
            pygame.display.update()
            self.clock.tick(self.fps)
            if self.game.GameIsOver():
                self.game.MakeSave('data.pickle', game_is_over=True)
                condition = False

    def AskForCheckpoint(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("There's a game in progress...")
        condition = True
        while condition:
            self.surface.fill(pygame.Color('dimgray'))
            self.DrawText('Continue?', 'white', 100, 50)

            button_1 = self.DrawButton(
                50, 100,
                self.button_width,
                self.button_height,
                'green'
            )
            button_2 = self.DrawButton(
                50, 200,
                self.button_width,
                self.button_height,
                'red'
            )
            self.DrawText(
                'Yes',
                'black',
                50,
                100,
                self.button_width,
                self.button_height
            )
            self.DrawText(
                'No',
                'black',
                50,
                200,
                self.button_width,
                self.button_height
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        condition = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        mx, my = pygame.mouse.get_pos()
                        if button_1.collidepoint((mx, my)):
                            with open('data.pickle', 'rb') as file:
                                save = pickle.load(file)
                            self.game = Game(self.cell_height, self.cell_width,
                                             self.bomb_number, saved_field=save)
                            condition = False
                        if button_2.collidepoint((mx, my)):
                            condition = False
            pygame.display.update()
            self.clock.tick(self.fps)

    def SolvedGame(self):
        pygame.display.set_caption('Solver')

        # Menú de selección de tipo de solver
        condition = True
        selected_solver = False  # Por defecto: Solver clásico

        while condition:
            self.surface.fill(pygame.Color('dimgray'))
            self.DrawText('Selecciona el Solver', 'white', 100, 50)

            button_classic = self.DrawButton(
                50, 100, self.button_width, self.button_height, 'lightblue'
            )
            button_enhanced = self.DrawButton(
                50, 200, self.button_width, self.button_height, 'lightgreen'
            )

            self.DrawText('Solver clásico', 'black', 50, 100, self.button_width, self.button_height)
            self.DrawText('EnhancedSolver', 'black', 50, 200, self.button_width, self.button_height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    condition = False
                    return  # Salir del método limpio
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if button_classic.collidepoint((mx, my)):
                        selected_solver = False
                        condition = False
                    if button_enhanced.collidepoint((mx, my)):
                        selected_solver = True
                        condition = False

            pygame.display.update()
            self.clock.tick(self.fps)

        # Inicializa el juego con el solver elegido
        self.game = Game(self.cell_height, self.cell_width, self.bomb_number, use_enhanced_solver=selected_solver)
        self.surface.fill(pygame.Color('dimgray'))
        self.game.RevealFirstCell()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return  # Salida segura

            passed = self.game.NextSolved()

            if not passed:
                running = False
                continue  # No seguir actualizando si perdió

            time.sleep(0.3)
            self.clock.tick(1)

            self.DrawGrid()
            self.DrawCells(self.game.GetPlayerField())
            pygame.display.update()

            if self.game.GameIsOver():
                running = False


@staticmethod
def GameInProgress():
        try:
            if os.stat('data.pickle').st_size > 0:
                return True
            else:
                return False

        except FileNotFoundError:
            f = open('data.pickle', 'wb')
            f.close()
            return False


if __name__ == '__main__':
    a = GUI()
    a.Run()
