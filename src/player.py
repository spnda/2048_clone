import copy
import random
import numpy
import numpy.typing
import typing

from game import Game, ActionType, TileType, ACTIONS

class Player(object):
    def __init__(self, game: Game, alpha=0.15, randomFactor=0.2):
        self.stateHistory = {}
        self.alpha = alpha
        self.randomFactor = randomFactor

        self.game = game


    def chooseRandomAction(self) -> ActionType:
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

    def simulateAction(self, game: Game, action: ActionType, prevHighestScore: int, depth: int) -> int:
        if depth == 0:
            return game.getScore()
        
        # Create a copy of the game we'll use to simulate moves.
        simulatedGame = copy.deepcopy(game)
        simulatedGame.move(action)
        if simulatedGame.isGameOver():
            return simulatedGame.getScore()

        highestScore = simulatedGame.getScore()
        for action in ACTIONS.values():
            score = self.simulateAction(simulatedGame, action, highestScore, depth - 1)
            if score > highestScore:
                highestScore = score
        return highestScore


    def chooseEducatedGuess(self, depth) -> ActionType:
        highestScore = self.game.getScore()
        bestMove = (0,0)
        
        for action in ACTIONS.values():
            score = self.simulateAction(self.game, action, highestScore, depth)
            if score > highestScore:
                bestMove = action
                highestScore = score

        return bestMove if bestMove != (0,0) else self.chooseRandomAction()


    def chooseAction(self) -> ActionType:
        # Too high depth values cause massive slowdowns.
        return self.chooseEducatedGuess(4)
