# --- EnhancedSolver.py con mejoras y CSP Global ---

import math
import itertools
from collections import defaultdict

class EnhancedSolver:
    def __init__(self, field, height, width, stats=None):
        self.field = field
        self.height = height
        self.width = width
        self.prob_dict = dict()
        self.stats = stats  # ← Añadido
        

    def Run(self):
        self.MakeProbDict()
        self.CorrectProbDict()
        self.CorrectTotalProb()
        self.ApplyCSP()
        prev = [self.prob_dict[key][0] for key in self.prob_dict]
        eps = 0.01
        while True:
            self.CorrectTotalProb()
            cur = [self.prob_dict[key][0] for key in self.prob_dict]
            if self.AccuracyCheck(prev, cur, eps):
                break
            prev = cur

        # Aplicar CSP global si no hay jugadas seguras claras
        if not self.MakeSafeMoves():
            self.ApplyGlobalCSP()

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
                if self.field[x][y] not in ('-', 'F', '*'):
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
                if self.field[x][y] not in ('-', 'F', '*'):
                    if int(self.field[x][y]) > 0:
                        s = 0
                        for element in self.NearCellList(x, y):
                            s += self.prob_dict[element][0]
                        if s != 0:
                            s = int(self.field[x][y]) / s
                        for element in self.NearCellList(x, y):
                            r = self.prob_dict[element][0]
                            self.prob_dict[element] = [r * s]

    def ApplyCSP(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.field[x][y] not in ('-', 'F', '*') and int(self.field[x][y]) > 0:
                    neighbors = self.NearCellList(x, y)
                    clue = int(self.field[x][y])
                    if len(neighbors) > 8 or clue > len(neighbors):
                        continue
                    configs = list(itertools.combinations(neighbors, clue))
                    count = {cell: 0 for cell in neighbors}
                    for config in configs:
                        for cell in config:
                            count[cell] += 1
                    for cell in neighbors:
                        if len(configs) > 0:
                            self.prob_dict[cell] = [count[cell] / len(configs)]

    def ApplyGlobalCSP(self):
        all_hidden = [(x, y) for x in range(self.height) for y in range(self.width) if self.field[x][y] == '-']
        if len(all_hidden) > 15:
            return  # demasiado costoso

        total_mines = self.estimate_remaining_mines()
        configs = list(itertools.combinations(all_hidden, total_mines))
        valid_configs = []

        for config in configs:
            field_copy = [[c for c in row] for row in self.field]
            for (x, y) in all_hidden:
                field_copy[x][y] = 'F' if (x, y) in config else '-'
            if self.is_valid_configuration(field_copy):
                valid_configs.append(set(config))

        if not valid_configs:
            return

        count = defaultdict(int)
        for config in valid_configs:
            for cell in config:
                count[cell] += 1

        for cell in all_hidden:
            prob = count[cell] / len(valid_configs) if cell in count else 0.0
            self.prob_dict[cell] = [prob]

    def estimate_remaining_mines(self):
        total = sum(1 for x in range(self.height) for y in range(self.width) if self.field[x][y] == 'F')
        return max(1, 40 - total)  # asumimos 40 minas por defecto

    def is_valid_configuration(self, test_field):
        for x in range(self.height):
            for y in range(self.width):
                if test_field[x][y] not in ('-', 'F', '*'):
                    clue = int(test_field[x][y])
                    neighbors = self.NearCellListFrom(test_field, x, y)
                    flags = sum(1 for (nx, ny) in neighbors if test_field[nx][ny] == 'F')
                    if flags != clue:
                        return False
        return True

    def NearCellListFrom(self, field, x, y):
        ans = []
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if not self.OutBorder(x + offset_x, y + offset_y):
                    if field[x + offset_x][y + offset_y] in ('-', 'F'):
                        ans.append((x + offset_x, y + offset_y))
        return ans

    @staticmethod
    def AccuracyCheck(l1, l2, eps):
        for i in range(len(l1)):
            if abs(l2[i] - l1[i]) > eps:
                return False
        return True

    def neighbor_risk(self, x, y):
        neighbors = self.NearCellList(x, y)
        risks = [self.prob_dict.get(nb, [1.0])[0] for nb in neighbors]
        return sum(risks) / len(risks) if risks else 1.0

    def entropy_score(self, x, y):
        neighbors = self.NearCellList(x, y)
        entropies = [
            -p * math.log2(p) - (1 - p) * math.log2(1 - p) if 0 < p < 1 else 0
            for (nx, ny) in neighbors
            for p in [self.prob_dict.get((nx, ny), [1.0])[0]]
        ]
        return sum(entropies) / len(entropies) if entropies else float('inf')

    def MakePrediction(self):
        candidates = [
            (key, self.prob_dict[key][0], self.neighbor_risk(*key), self.entropy_score(*key))
            for key in self.prob_dict
        ]
        candidates.sort(key=lambda x: (x[1], x[2], x[3]))
        if candidates:
            cell, prob, _, _ = candidates[0]
            if self.stats:  # ← Añadido
                self.stats.register_move(prob)
            return cell
        return (0, 0)

    def MakeSafeMoves(self):
        if not self.prob_dict:
            return []
        min_prob = min([p[0] for p in self.prob_dict.values()])
        tolerance = 0.02
        safe_candidates = [cell for cell, prob in self.prob_dict.items() if prob[0] <= min_prob + tolerance]
        safe_candidates.sort(key=lambda c: (self.prob_dict[c][0], self.entropy_score(*c)))
        if self.stats and safe_candidates:
            for cell in safe_candidates:
             self.stats.register_move(self.prob_dict[cell][0])  # ← Añadido
        return safe_candidates
