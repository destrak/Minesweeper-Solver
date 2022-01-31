class Cell:

    def __init__(
            self,
            bomb=False
    ):

        self.revealed = False
        self.flagged = False
        self.bomb = bomb
        self.val = 0

    def Reveal(self):
        self.revealed = True

    def Flag(self):
        self.flagged = not self.flagged

    def MakeBomb(self):
        self.bomb = not self.bomb

    def IsRevealed(self):
        return self.revealed

    def IsFlagged(self):
        return self.flagged

    def IsBomb(self):
        return self.bomb

    def ChangeValue(self, value):
        self.val = value

    def GetValue(self):
        return self.val
