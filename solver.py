# --- Solver.py ---

class Solver:
    def __init__(self, field, height, width, stats=None):
        self.field = field
        self.height = height
        self.width = width
        self.prob_dict = dict()
        self.stats = stats  # Agregado


    def Run(self):
        self.MakeProbDict()
        self.CorrectProbDict()
        self.CorrectTotalProb()
        prev = [self.prob_dict[key][0] for key in self.prob_dict]
        eps = 0.01
        while True:
            self.CorrectTotalProb()
            cur = [self.prob_dict[key][0] for key in self.prob_dict]
            if self.AccuracyCheck(prev, cur, eps):
                break
            prev = cur
        return len(self.prob_dict) > 0

    def OutBorder(self, x, y):
        return x < 0 or y < 0 or x >= self.height or y >= self.width

    def NearCellList(self, x, y):
        ans = []
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.OutBorder(x + offset_x, y + offset_y):
                    if self.field[x + offset_x][y + offset_y] == '-':
                        ans.append((x + offset_x, y + offset_y))
        return ans

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

    def NearProb(self, x, y):
        s = []
        n = len(self.NearCellList(x, y))
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.OutBorder(x + offset_x, y + offset_y):
                    if self.field[x + offset_x][y + offset_y] == '-':
                        prob = int(self.field[x][y]) / n
                        s.append([(x + offset_x, y + offset_y), prob])
        return s

    def CorrectProbDict(self):
        for element in self.prob_dict:
            p = 1
            for i in self.prob_dict[element]:
                p *= (1 - i)
            p = 1 - p
            self.prob_dict[element] = [p]

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

    @staticmethod
    def AccuracyCheck(l1, l2, eps):
        for i in range(len(l1)):
            if abs(l2[i] - l1[i]) > eps:
                return False
        return True

    def MakePrediction(self):
        minimum = 1.0
        cords = (0, 0)
        for key in self.prob_dict:
            if self.prob_dict[key][0] <= minimum:
                minimum = self.prob_dict[key][0]
                cords = key
        if self.stats:
            self.stats.register_move(minimum)
        return cords
    def MakeSafeMoves(self):
        if not self.prob_dict:
            return []
        min_prob = min([p[0] for p in self.prob_dict.values()])
        tolerance = 0.02  # Mismo criterio que EnhancedSolver
        safe_candidates = [cell for cell, prob in self.prob_dict.items() if prob[0] <= min_prob + tolerance]
        safe_candidates.sort(key=lambda c: self.prob_dict[c][0])  # Ordenar por menor probabilidad
        return safe_candidates



