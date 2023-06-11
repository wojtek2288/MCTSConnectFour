from mcts import MCTS
from state import State

class Connect4OpportunisticMCTS(MCTS):
    def __init__(self, state=State(), seed=1):
        super().__init__(state, seed)

    def move_next(self):
        # winning move
        move = self.root_state.get_winning_move(self.root_state.last_last_row, self.root_state.last_last_column, self.root_state.player_to_play)

        if move != None:
            print("Winning move: " + str(move + 1))

        if move == None:
            # blocking move
            move = self.root_state.get_winning_move(self.root_state.last_row, self.root_state.last_column, self.root_state.get_last_player())

        if move != None:
            print("Blocking move: " + str(move + 1))

        if move == None:
            self.search()
            move = self.get_best_child(self.root).move

        self.register_move(move)
        return move