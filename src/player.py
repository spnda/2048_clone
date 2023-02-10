import numpy
import numpy.typing
import typing

from game import Game, ActionType, TileType

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

class Player(object):
    def __init__(self, game: Game, alpha=0.15, randomFactor=0.2):
        self.stateHistory = {}
        self.alpha = alpha
        self.randomFactor = randomFactor

        self.game = game


    def chooseAction(self) -> ActionType:
        nextMove = ACTIONS['U']

        notDecided = True
        while notDecided:
            move = ACTIONS[numpy.random.choice(list(ACTIONS.keys()))]
            for x in range(self.game.boardSize):
                for y in range(self.game.boardSize):
                    if self.game.canMoveInDirection((x, y), move):
                        nextMove = move
                        notDecided = False
                        break
            if not notDecided:
                break

        return nextMove
