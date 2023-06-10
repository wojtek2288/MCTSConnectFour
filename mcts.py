import random
import math
from copy import deepcopy

from state import State, GameResults

class Constants:
    NUMBER_OF_ITERATIONS = 10000
    EXPLORATION_COEFFICIENT = math.sqrt(2)
    INF = float('inf')

class Node:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}

    def add_children(self, children: dict):
        for child in children:
            self.children[child.move] = child

    def UCT(self):
        return Constants.INF if self.N == 0 else self.Q / self.N + Constants.EXPLORATION_COEFFICIENT * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, state=State()):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.node_count = 0
        self.node_type = Node

    def select(self):
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            node = self.get_best_child(node)
            state.register_move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.register_move(node.move)

        return node, state
    
    def get_best_child(self, node):
        children = node.children.values()
        max_value = max(children, key=lambda n: n.UCT()).UCT()
        return random.choice([n for n in children if n.UCT() == max_value])

    def expand(self, parent: Node, state: State) -> bool:
        if state.game_over():
            return False

        children = [self.node_type(move, parent) for move in state.get_empty_columns()]
        parent.add_children(children)

        return True

    def simulate(self, state: State):
        while not state.game_over():
            state.register_move(random.choice(state.get_empty_columns()))

        return state.get_game_result()

    def back_propagate(self, node: Node, state: State, outcome: int):
        update_reward = outcome == GameResults.DRAW
        reward = 0 if outcome == state.player_to_play else 1 # the player to play is the one who lost

        while node is not None:
            node.N += 1
            if update_reward:    # we treat draws as a loss for both players
                node.Q += reward
                reward = 1 - reward
            node = node.parent

    def search(self):
        for _ in range(Constants.NUMBER_OF_ITERATIONS):
            node, state = self.select()
            outcome = self.simulate(state)
            self.back_propagate(node, state, outcome)

    def register_move(self, move):
        if move in self.root.children:
            self.root_state.register_move(move)
            self.root = self.root.children[move]
            return

        self.root_state.register_move(move)
        self.root = self.node_type(None, None)

    def move_next(self):
        self.search()
        move = self.get_best_child(self.root).move
        self.register_move(move)
        return move

