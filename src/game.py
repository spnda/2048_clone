import numpy
import numpy.typing
import typing

ACTIONS = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

TileType = typing.Tuple[int, int]
ActionType = typing.Tuple[int, int]

# Maximum possible points according to https://www.reddit.com/r/2048/comments/214njx/highest_possible_score_for_2048_warning_math/
MaximumScore = 3932156

class Game(object):
    changedTiles: typing.Dict[typing.Tuple[int, int], bool]
    tiles: numpy.typing.NDArray[numpy.int64]

    def __init__(self, boardSize = 4):
        self.boardSize = boardSize
        self.reset()


    def getScore(self) -> int:
        """
        Returns the current score of the game, which is incremented by the value of the tile
        that gets combined.
        """
        return self.score


    def isOnBoard(self, tile: TileType) -> bool:
        return 0 <= tile[0] < self.boardSize and 0 <= tile[1] < self.boardSize


    def canCombine(self, tile1: TileType, tile2: TileType) -> bool:
        """
        Checks if two tiles can be combined, by checking if they are the same value and not empty.
        """
        if not self.isOnBoard(tile1) or not self.isOnBoard(tile2):
            return False

        x1, y1 = tile1
        x2, y2 = tile2
        return self.tiles[x1, y1] != 0 and self.tiles[x2, y2] != 0 and self.tiles[x1, y1] == self.tiles[x2, y2]


    def canMoveInDirection(self, tile: TileType, action: ActionType) -> bool:
        """
        Checks if a tile can move in a direction (at least 1), by checking if the tile is on
        the edge of the board or if the tile would move onto an empty space, but not if a tile
        would merge with another.
        """
        x, y = tile
        dx, dy = action
        if not self.isOnBoard((x + dx, y + dy)):
            return False
        return self.tiles[x + dx, y + dy] == 0


    def canMove(self, tile: TileType) -> bool:
        """
        Checks if a tile can move in any direction.
        """
        for _, action in ACTIONS.items():
            if self.canMoveInDirection(tile, action):
                return True
        return False


    def isGameOver(self) -> bool:
        """
        Checks if the game is over by checking if there are any empty spaces or if any tiles can
        be combined.
        """
        for (x, y), tile in numpy.ndenumerate(self.tiles):
            if tile == 0:
                return False
            if self.canMove((x, y)):
                return False
        return True


    def move(self, action: ActionType):
        dx, dy = action

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                x = self.boardSize - 1 - i if dx == 1 else i
                y = self.boardSize - 1 - j if dy == 1 else j

                if self.tiles[x, y] == 0:
                    continue
                
                if self.canMoveInDirection((x, y), action):
                    # As we start at the opposite of the direction, we need to move multiple steps here.
                    xn = x + dx
                    yn = y + dy
                    while True:
                        if self.canMoveInDirection((xn, yn), action):
                            xn += dx
                            yn += dy
                        else:
                            break
                    self.tiles[xn, yn] = self.tiles[x, y]
                    self.tiles[x, y] = 0
                    self.changedTiles[(xn, yn)] = True
                    x = xn
                    y = yn

                if self.isOnBoard((x + dx, y + dy)) and self.canCombine((x, y), (x + dx, y + dy)):
                    self.tiles[x + dx, y + dy] *= 2
                    self.tiles[x, y] = 0
                    self.changedTiles[(x + dx, y + dy)] = True
                    self.score += self.tiles[x + dx, y + dy]

        if len(self.changedTiles) > 0:
            self.placeRandomTileOnBoard()
        self.changedTiles.clear()


    def placeRandomTileOnBoard(self):
        """
        Places a random tile on the board, anywhere that is empty. 90% chance
        for a 2, 10% chance for a 4.
        """
        i = 0
        while i < 16:
            x, y = tuple(numpy.random.randint(self.boardSize, size=2))
            if self.tiles[x, y] == 0:
                self.tiles[x, y] = 2 if numpy.random.random() < 0.9 else 4
                break
            i += 1


    def reset(self):
        self.score = 0
        # We'll try to use this arrays of arrays in column major order.
        self.tiles = numpy.zeros((self.boardSize, self.boardSize), dtype=int)
        self.tiles[0:, :self.boardSize] = 0
        
        # Dictionary to keep track of tiles that changed within a turn.
        self.changedTiles = {}
        
        # The game always starts with two tiles on the board
        self.placeRandomTileOnBoard()
        self.placeRandomTileOnBoard()
