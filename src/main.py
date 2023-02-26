import sys
import time

import matplotlib.pyplot as plt

from game import Game, ACTIONS
from player import Player

def printBoard(game: Game):
    # The tiles array is a column major array.
    for y in range(game.boardSize):
        for x in range(game.boardSize):
            print(game.tiles[x, y], end=' ')
        print()


def clearTerminal():
    print("\033[H\033[J", end="")


def aiPlay(game: Game, player: Player) -> int:
    while not game.isGameOver():
        # clearTerminal()
        # printBoard(game)
        nextMove = player.chooseAction()
        game.move(nextMove)
    return game.getScore()


def manual(game: Game) -> int:
    while not game.isGameOver():
        printBoard(game)
        nextMove = ''
        while nextMove not in ACTIONS:
            nextMove = input("Next Move: ")

        game.move(ACTIONS[nextMove])
        clearTerminal()
    return game.getScore()


if __name__ == '__main__':
    game = Game()
    player = Player(game, alpha=0.1, randomFactor=0.25)

    if len(sys.argv) >= 2 and sys.argv[1] == 'ai':
        scores = []
        highestScore = 0
        b = time.time()
        for i in range(5):
            newScore = aiPlay(game, player)
            scores.append(newScore)
            highestScore = max(highestScore, newScore)
            game.reset()
        print("Time taken: ", time.time() - b)
        print("Highest score: ", highestScore)
        print("Average score: ", sum(scores) / len(scores))     

        # Plot the scores of the AI over time.
        fig, ax = plt.subplots()
        ax.plot(scores)
        plt.show()
    else:
        newScore = manual(game)
