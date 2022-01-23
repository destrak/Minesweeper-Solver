import random


class Field:
    # Конструктор поля
    def __init__(self, h, w, n):
        self.height = h
        self.width = w
        self.bombs = n
        self.field = self.MakeNewField()
        self.AssignValues()
        self.revealed = set()
        self.flagged = set()

    # Генерация поля
    def MakeNewField(self):
        field = [
            [0 for _ in range(self.width)]
            for _ in range(self.height)
        ]

        counter = 0

        while counter < self.bombs:
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if field[x][y] == '*':
                continue
            field[x][y] = '*'
            counter += 1

        return field

    # Проверка на выход за границы поля
    def OutBorder(self, x, y):
        return x < 0 or y < 0 or x >= self.height or y >= self.width

    # Количество бомб в окружении
    def NeighborCounter(self, x, y):
        counter = 0
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.OutBorder(x + offset_x, y + offset_y):
                    if self.field[x + offset_x][y + offset_y] == '*':
                        counter += 1
        return counter

    # Присваивание значений клеткам
    def AssignValues(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.field[x][y] == '*':
                    continue
                self.field[x][y] = self.NeighborCounter(x, y)

    # Открыть клетку
    def Reveal(self, x, y) -> bool:
        self.revealed.add((x, y))
        if self.field[x][y] == '*':
            return False
        elif int(self.field[x][y]) > 0:
            return True
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.OutBorder(x + offset_x, y + offset_y):
                    if (x + offset_x, y + offset_y) in self.revealed:
                        continue
                    self.Reveal(x + offset_x, y + offset_y)
        return True

    # Пометить клетку
    def Flag(self, x, y):
        if (x, y) not in self.flagged:
            self.flagged.add((x, y))
        else:
            self.flagged.remove((x, y))

    # Состояние клетки
    def GetState(self, x, y):
        return self.field[x][y]

    # Список открытых клеток
    def GetRevealed(self) -> set:
        return self.revealed

    # Размер поля
    def GetSize(self):
        return self.height, self.width

    # Поле
    def GetField(self) -> list:
        return self.field

    # Генерация поля для пользователя
    def Render(self) -> list:
        visible_field = [['-' for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.height):
            for y in range(self.width):
                if (x, y) in self.revealed:
                    visible_field[x][y] = self.field[x][y]
                elif (x, y) in self.flagged:
                    visible_field[x][y] = 'F'
        return visible_field
