from copy import deepcopy
import math
from mcts import MCTS, Constants, Node

from state import State

class Connect4Constants(Constants):
    UCT_HEURISTIC_RATIO = 1.5

class Connect4Node(Node):
    def __init__(self, move, parent):
        super().__init__(move, parent)

    def potencial_wins_heuristic(self, state):
        heuristic_value = 0

        for child in self.children.values():
            potential_wins = state.count_potential_wins(child.move)
            heuristic_value += potential_wins

        return heuristic_value

class Connect4MCTS(MCTS):
    def __init__(self, state=State(), seed=1):
        super().__init__(state, seed)
        self.root = Connect4Node(None, None)
        self.node_count = 0
        self.node_type = Connect4Node

    def select(self):
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            node = self.get_best_child(node, state)
            state.register_move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = self.random.choice(list(node.children.values()))
            state.register_move(node.move)

        return node, state

    def get_best_child(self, node, state):
        children = node.children.values()
        max_value = max(children, key=lambda n: Connect4Constants.UCT_HEURISTIC_RATIO * n.UCT() + n.potencial_wins_heuristic(state))
        return self.random.choice([n for n in children if Connect4Constants.UCT_HEURISTIC_RATIO * n.UCT() + n.potencial_wins_heuristic(state) == Connect4Constants.UCT_HEURISTIC_RATIO * max_value.UCT() + max_value.potencial_wins_heuristic(state)])

    def move_next(self):
        self.search()
        move = self.get_best_child(self.root, self.root_state).move
        self.register_move(move)
        return move