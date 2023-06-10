from meta import GameMeta
import numpy as np

class State:
    def __init__(self):
        self.board = np.array([[0] * GameMeta.COLS for _ in range(GameMeta.ROWS)])
        self.to_play = GameMeta.PLAYERS['one']
        self.height = [GameMeta.ROWS - 1] * GameMeta.COLS
        self.last_played = []

    def register_move(self, col):
        self.board[self.height[col]][col] = self.to_play
        self.last_played = [self.height[col], col]
        self.height[col] -= 1
        self.to_play = GameMeta.PLAYERS['two'] if self.to_play == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']

    def get_empty_columns(self):
        return [id for id, col in enumerate(self.board[0]) if col == 0]

    def check_win(self):
        if len(self.last_played) > 0 and self.check_win_from(self.last_played[0], self.last_played[1]):
            return self.board[self.last_played[0]][self.last_played[1]]
        return 0
    
    def check_array(self, array, player):
        if(len(array) < 4):
            return False
        count = 0
        for x in array:
            if x == player:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True
        return False

    def check_win_from(self, row, col):
        player = self.board[row][col]

        # row
        if self.check_array(self.board[row], player):
            return True

        # column
        if self.check_array(self.board[:, col], player):
            return True

        # diagonal
        if self.check_array(self.board.diagonal(offset=col - row), player):
            return True
        
        # antidiagonal
        if self.check_array(np.fliplr(self.board).diagonal(offset=self.board.shape[1] - col - 1 - row), player):
            return True

        return False

    def game_over(self):
        return self.check_win() or len(self.get_empty_columns()) == 0

    def get_outcome(self):
        if len(self.get_empty_columns()) == 0 and self.check_win() == 0:
            return GameMeta.OUTCOMES['draw']

        return GameMeta.OUTCOMES['one'] if self.check_win() == GameMeta.PLAYERS['one'] else GameMeta.OUTCOMES['two']

    def print_state(self):
        print('=' * 29)
        for x in range(7):
            print(f'| {x}', end=' ')
        
        print('|')
        print('=' * 29)
        
        for r in self.board:
            print('|' + '|'.join([" X " if x == 1 else " O " if x == 2 else "   " for x in r]) + '|')

        print('=' * 29)

