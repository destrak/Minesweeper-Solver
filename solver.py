class Solver:

    # Конструктор помощника
    def __init__(self, field, h, w):
        self.field = field
        self.height = h
        self.width = w
        self.prob_dict = dict()

    # Запуск помощника
    def Run(self) -> bool:
        self.MakeProbDict()
        self.CorrectProbDict()
        self.CorrectTotalProb()
        prev = [element[0] for element in self.prob_dict]
        eps = 0.01
        while True:
            self.CorrectTotalProb()
            cur = [element[0] for element in self.prob_dict]
            if self.AccuracyCheck(prev, cur, eps):
                break
            prev = cur
        return len(self.prob_dict) > 0

    # Проверка на выход за границы поля
    def OutBorder(self, x, y) -> bool:
        return x < 0 or y < 0 or x >= self.height or y >= self.width

    # Список координат лежащих рядом клеток
    def NearCellList(self, x, y):
        ans = []
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.OutBorder(x + offset_x, y + offset_y):
                    if self.field[x + offset_x][y + offset_y] == '-':
                        ans.append((x + offset_x, y + offset_y))
        return ans

    # Создание словаря вероятностей: {координаты клетки: вероятность бомбы в этой клетке}
    def MakeProbDict(self):
        for x in range(self.height):
            for y in range(self.width):
                if (self.field[x][y] != '-' and
                        self.field[x][y] != 'F' and
                        self.field[x][y] != '*'):
                    if int(self.field[x][y]) > 0:
                        g = self.NearProb(x, y)
                        for element in g:
                            if element[0] not in self.prob_dict:
                                self.prob_dict[element[0]] = []
                            self.prob_dict[element[0]].append(element[1])

    # Вероятность бомбы в лежащих рядом клетках
    def NearProb(self, x, y) -> list:
        s = []
        n = len(self.NearCellList(x, y))
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.OutBorder(x + offset_x, y + offset_y):
                    if self.field[x + offset_x][y + offset_y] == '-':
                        prob = int(self.field[x][y]) / n
                        s.append([(x + offset_x, y + offset_y), prob])
        return s

    # Корректировка вероятности клеток, которые лежат в пересечении
    def CorrectProbDict(self):
        for element in self.prob_dict:
            p = 1
            for i in self.prob_dict[element]:
                p *= (1 - i)
            p = 1 - p
            self.prob_dict[element] = [p]

    # Корректировка вероятностей, пока разница не станет меньше eps
    def CorrectTotalProb(self):
        for x in range(self.height):
            for y in range(self.width):
                if (self.field[x][y] != '-' and
                        self.field[x][y] != 'F' and
                        self.field[x][y] != '*'):
                    if int(self.field[x][y]) > 0:
                        s = 0
                        for element in self.NearCellList(x, y):
                            s += self.prob_dict[element][0]
                        if s != 0:
                            s = int(self.field[x][y]) / s
                        for element in self.NearCellList(x, y):
                            r = self.prob_dict[element][0]
                            self.prob_dict[element] = [r * s]

    # Проверка на точность
    def AccuracyCheck(self, l1, l2, eps):
        for i in range(len(l1)):
            if l2[i] - l1[i] > eps:
                return False
        return True

    # Выбор наилучшего хода
    def MakePrediction(self):
        minimum = 1.0
        cords = (0, 0)
        for key in self.prob_dict:
            if self.prob_dict[key][0] <= minimum:
                minimum = self.prob_dict[key][0]
                cords = key
        return cords
