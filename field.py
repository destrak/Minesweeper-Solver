from cell import Cell
import random
import sys

sys.setrecursionlimit(10000)


class Field:

    def __init__(self, h=10, w=10, n=10):
        self.height = h
        self.width = w
        self.bombs = n
        self.field = self.MakeNewField()
        self.AssignValues()

        self.unrevealed_sign = '-'
        self.bomb_sign = '*'
        self.flag_sign = 'F'

    def MakeNewField(self):
        field = [
            [Cell() for _ in range(self.width)] for _ in range(self.height)
        ]
        counter = 0
        while counter < self.bombs:
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if field[x][y].IsBomb():
                continue
            field[x][y].MakeBomb()
            counter += 1
        return field

    def GetSize(self):
        return self.height, self.width

    def IsOutBorder(self, x, y):
        return x < 0 or y < 0 or x >= self.height or y >= self.width

    def NeighborCounter(self, x, y):
        counter = 0
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.IsOutBorder(x + offset_x, y + offset_y):
                    if self.field[x + offset_x][y + offset_y].IsBomb():
                        counter += 1
        return counter

    def AssignValues(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.field[x][y].IsBomb():
                    continue
                n = self.NeighborCounter(x, y)
                self.field[x][y].ChangeValue(n)

    def RevealCell(self, x, y) -> bool:
        self.field[x][y].Reveal()
        if self.field[x][y].IsBomb():
            return False
        elif self.field[x][y].GetValue() > 0:
            return True
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.IsOutBorder(x + offset_x, y + offset_y):
                    if self.field[x + offset_x][y + offset_y].IsRevealed():
                        continue
                    self.RevealCell(x + offset_x, y + offset_y)
        return True

    def GetRevealedCells(self) -> set:
        revealed = set()
        for x in range(self.height):
            for y in range(self.width):
                if self.field[x][y].IsRevealed():
                    revealed.add((x, y))
        return revealed

    def FlagCell(self, x, y):
        self.field[x][y].Flag()

    def Render(self) -> list:
        visible_field = [
            [self.unrevealed_sign for _ in range(self.width)] for _ in range(self.height)
        ]
        for x in range(self.height):
            for y in range(self.width):
                if self.field[x][y].IsRevealed():
                    visible_field[x][y] = self.field[x][y].GetValue()
                    if self.field[x][y].IsBomb():
                        visible_field[x][y] = self.bomb_sign
                elif self.field[x][y].IsFlagged():
                    visible_field[x][y] = self.flag_sign
        return visible_field
