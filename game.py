import pickle
from field import Field
from solver import Solver


class Game:

    def __init__(
            self,
            height,
            width,
            bomb_number,
            saved_field=None
    ):

        self.width = width
        self.height = height
        self.bomb_number = bomb_number
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

    def NextSolved(self):
        r = self.field.Render()
        height, width = self.field.GetSize()
        solver = Solver(r, height, width)
        solver.Run()
        prediction = solver.MakePrediction()
        x, y = prediction[0], prediction[1]
        passed = self.field.RevealCell(x, y)
        if not passed:
            self.game_is_over_ = True
            return False
        return True

    def GameIsOver(self):
        height, width = self.field.GetSize()
        revealed = self.field.GetRevealedCells()
        if len(revealed) >= height * width - self.bomb_number:
            self.game_is_over_ = True
            return True
        else:
            return False

    def MakeSave(self, filename, game_is_over=False):
        if game_is_over:
            f = open(filename, 'wb')
            f.close()
        else:
            field = self.field
            f = open(filename, 'wb')
            pickle.dump(field, f)
            f.close()
