import numpy as np

class GameResults:
    ONGOING = 0
    PLAYER_ONE_WON = 1
    PLAYER_TWO_WON = 2
    DRAW = 3

class BoardConstants:
    NUM_OF_COLUMNS = 7
    NUM_OF_ROWS = 6
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    BLANK = 0

class State:
    def __init__(self):
        self.board = np.array([[BoardConstants.BLANK] * BoardConstants.NUM_OF_COLUMNS for _ in range(BoardConstants.NUM_OF_ROWS)])
        self.player_to_play = BoardConstants.PLAYER_ONE
        self.last_row = -1
        self.last_column = -1

    def register_move(self, col):
        row = [id for id, x in enumerate(self.board[:, col]) if x == BoardConstants.BLANK][-1]
        self.board[row][col] = self.player_to_play
        self.player_to_play = self.get_last_player()
        self.last_row = row
        self.last_column = col

    def get_last_player(self):
        return BoardConstants.PLAYER_TWO if self.player_to_play == BoardConstants.PLAYER_ONE else BoardConstants.PLAYER_ONE

    def get_empty_columns(self):
        return [id for id, col in enumerate(self.board[0]) if col == BoardConstants.BLANK]

    def get_winning_player(self):
        if self.last_row != -1 and self.check_win_for_previous(self.last_row, self.last_column):
            return self.get_last_player()
        return 0
    
    def game_over(self):
        return self.get_winning_player() != 0 or len(self.get_empty_columns()) == 0

    def get_game_result(self):
        winning_player = self.get_winning_player()
        if winning_player == 0 and len(self.get_empty_columns()) == 0:
            return GameResults.DRAW

        return GameResults.PLAYER_ONE_WON if winning_player == BoardConstants.PLAYER_ONE else GameResults.PLAYER_TWO_WON
    
    def check_array(self, array, player, sequence_number):
        if(len(array) < 4):
            return False
        count = 0
        for x in array:
            if x == player:
                count += 1
            else:
                count = 0
            if count >= sequence_number:
                return True
        return False

    def check_win_for_previous(self, row, col):
        player = self.board[row][col]

        # row
        if self.check_array(self.board[row], player, 4):
            return True

        # column
        if self.check_array(self.board[:, col], player, 4):
            return True

        # diagonal
        if self.check_array(self.board.diagonal(offset=col - row), player, 4):
            return True
        
        # antidiagonal
        if self.check_array(np.fliplr(self.board).diagonal(offset=self.board.shape[1] - col - 1 - row), player, 4):
            return True

        return False

    def count_potential_wins(self, col):
        row = [id for id, x in enumerate(self.board[:, col]) if x == BoardConstants.BLANK][-1]
        potential_wins = 0

        # row
        if self.check_array(self.board[row], self.player_to_play, 3):
            potential_wins += 1

        # column
        if self.check_array(self.board[:, col], self.player_to_play, 3):
            potential_wins += 1

        # diagonal
        if self.check_array(self.board.diagonal(offset=col - row), self.player_to_play, 3):
            potential_wins += 1
        
        # antidiagonal
        if self.check_array(np.fliplr(self.board).diagonal(offset=self.board.shape[1] - col - 1 - row), self.player_to_play, 3):
            potential_wins += 1

        # row
        if self.check_array(self.board[row], self.get_last_player(), 3):
            potential_wins = 0

        # column
        if self.check_array(self.board[:, col], self.get_last_player(), 3):
            potential_wins = 0

        # diagonal
        if self.check_array(self.board.diagonal(offset=col - row), self.get_last_player(), 3):
            potential_wins = 0
        
        # antidiagonal
        if self.check_array(np.fliplr(self.board).diagonal(offset=self.board.shape[1] - col - 1 - row), self.get_last_player(), 3):
            potential_wins = 0

        return potential_wins

    def print_state(self):
        print('=' * 29)
        for x in range(1, 8):
            print(f'| {x}', end=' ')
        
        print('|')
        print('=' * 29)
        
        for r in self.board:
            print('|' + '|'.join([" X " if x == 1 else " O " if x == 2 else "   " for x in r]) + '|')

        print('=' * 29)

