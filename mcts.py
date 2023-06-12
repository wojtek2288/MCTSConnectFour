import random
import math
from copy import deepcopy

from state import State, GameResults

class Constants:
    NUMBER_OF_ITERATIONS = 5000
    EXPLORATION_COEFFICIENT = math.sqrt(2)
    INF = float('inf')

class Node:
    def __init__(self, move_before, parent):
        self.UCT_N = 0
        self.UCT_Q = 0
        self.move_before = move_before
        self.parent = parent
        self.children = {}

    def add(self, children):
        for child in children:
            self.children[child.move_before] = child

    def UCT(self):
        return Constants.INF if self.UCT_N == 0 else self.UCT_Q / self.UCT_N + Constants.EXPLORATION_COEFFICIENT * math.sqrt(math.log(self.parent.UCT_N) / self.UCT_N)


class MCTS:
    def __init__(self, state=State(), seed = 1):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.node_count = 0
        self.node_type = Node
        self.random = random.Random(seed)

    def select(self):
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            node = self.get_best_child(node)
            state.register_move(node.move_before)

            if node.UCT_N == 0:
                return node, state

        if self.expand(node, state):
            node = self.random.choice(list(node.children.values()))
            state.register_move(node.move_before)

        return node, state
    
    def get_best_child(self, node):
        children = node.children.values()
        max_value = max(children, key = lambda node: node.UCT()).UCT()
        return self.random.choice([n for n in children if n.UCT() == max_value])

    def expand(self, node, state):
        if state.end_state():
            return False

        children = [self.node_type(move, node) for move in state.get_empty_columns()]
        node.add(children)

        return True

    def simulate(self, state: State):
        while not state.end_state():
            state.register_move(self.random.choice(state.get_empty_columns()))

        return state.get_game_result()

    def back_propagate(self, node, player, result):
        reward = 0 if result == player else 1

        while node is not None:
            node.UCT_N += 1
            node.UCT_Q += reward
            reward = 0 if result == GameResults.DRAW else 1 - reward
            node = node.parent

    def search(self):
        for _ in range(Constants.NUMBER_OF_ITERATIONS):
            node, state = self.select()
            result = self.simulate(state)
            self.back_propagate(node, state, result)

    def register_move(self, column_id):
        if column_id in self.root.children:
            self.root_state.register_move(column_id)
            self.root = self.root.children[column_id]
        else:
            self.root_state.register_move(column_id)
            self.root = self.node_type(None, None)

    def move_next(self):
        self.search()
        move = self.get_best_child(self.root).move_before
        self.register_move(move)
        return move

