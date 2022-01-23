import os
import pickle
from game import Game


# Проверка сохранения
def SaveCheck() -> bool:
    try:
        f = open('data.pickle', 'rb')
        if os.stat('data.pickle').st_size > 0:
            print('\n', end="")
            print("There's a game in progress, would you like to continue?", '\n')
            print("[Input] Yes | No >> ", end="")
            ans = input()
            if ans == 'Yes':
                return True
            else:
                f = open('data.pickle', 'wb')
                f.close()
        f.close()
    except FileNotFoundError:
        f = open('data.pickle', 'wb')
        f.close()
        return False


# Запуск
print('\n', end="")
print('Choose game type:')
print("[Input] Regular | Solver >> ", end="")
answer = input()
if answer == 'Regular':
    if SaveCheck():
        with open('data.pickle', 'rb') as file:
            save = pickle.load(file)
            minesweeper = Game(saved_field=save)
    else:
        minesweeper = Game()
    minesweeper.Run()
    minesweeper.MakeSave()
else:
    minesweeper = Game(fps=5)
    minesweeper.RunSolved()

