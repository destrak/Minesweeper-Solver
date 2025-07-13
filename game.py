import pickle
from field import Field
from solver import Solver
from EnhancedSolver import EnhancedSolver

class Game:
    def __init__(self, height, width, bomb_number, saved_field=None, use_enhanced_solver=False):
        self.width = width
        self.height = height
        self.bomb_number = bomb_number
        self.use_enhanced_solver = use_enhanced_solver
        self.game_is_over_ = False

        if saved_field is None:
            self.field = Field(self.height, self.width, self.bomb_number)
        else:
            self.field = saved_field

    def RevealFirstCell(self):
        self.field.RevealCell(0, 0)

    def GetPlayerField(self):
        return self.field.Render()

    def Next(self, action, x, y):
        if action == 'reveal':
            passed = self.field.RevealCell(x, y)
            if not passed:
                self.game_is_over_ = True
                return False
        elif action == 'flag':
            self.field.FlagCell(x, y)
        return True

    def NextSolved(self, stats=None):
        r = self.field.Render()
        height, width = self.field.GetSize()

        # ✔ Aquí corregimos: pasamos el objeto stats solo si Enhanced lo admite
        if self.use_enhanced_solver:
            solver = EnhancedSolver(r, height, width)
        else:
            solver = Solver(r, height, width)

        solver.Run()

        # Elegimos la jugada
        if hasattr(solver, "MakeSafeMoves"):
            safe_moves = solver.MakeSafeMoves()
            if safe_moves:
                x, y = safe_moves[0]
                prob = solver.prob_dict.get((x, y), [0.0])[0]  # ✔ Si es safe, usamos 0.0
            else:
                x, y = solver.MakePrediction()
                prob = solver.prob_dict.get((x, y), [1.0])[0]  # ❗ Esto puede ser alto
        else:
            x, y = solver.MakePrediction()
            prob = solver.prob_dict.get((x, y), [1.0])[0]

        # ✔ Registramos la probabilidad real usada en el movimiento
        if stats:
            stats.register_move(prob)

        passed = self.field.RevealCell(x, y)
        if not passed:
            self.game_is_over_ = True
            return False
        return True

    def GameIsOver(self):
        if self.game_is_over_:
            return False
        height, width = self.field.GetSize()
        revealed = self.field.GetRevealedCells()
        if len(revealed) >= height * width - self.bomb_number:
            self.game_is_over_ = True
            return True
        return False

    def MakeSave(self, filename, game_is_over=False):
        if game_is_over:
            with open(filename, 'wb') as f:
                pass
        else:
            with open(filename, 'wb') as f:
                pickle.dump(self.field, f)
