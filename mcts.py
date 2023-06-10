import random
import time
import math
from copy import deepcopy

from state import State
from meta import GameMeta

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
        self.outcome = GameMeta.PLAYERS['none']

    def add_children(self, children: dict):
        for child in children:
            self.children[child.move] = child

    def value(self):
        if self.N == 0:
            return 0 if Constants.EXPLORATION_COEFFICIENT == 0 else float('inf')
        else:
            return self.Q / self.N + Constants.EXPLORATION_COEFFICIENT * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, state=State()):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
        self.node_type = Node

    def select_node(self) -> tuple:
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            state.register_move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.register_move(node.move)

        return node, state

    def expand(self, parent: Node, state: State) -> bool:
        if state.game_over():
            return False

        children = [self.node_type(move, parent) for move in state.get_empty_columns()]
        parent.add_children(children)

        return True

    def roll_out(self, state: State):
        while not state.game_over():
            state.register_move(random.choice(state.get_empty_columns()))

        return state.get_outcome()

    def back_propagate(self, node: Node, turn: int, outcome: int):
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward

    def search(self, num_interations: int = Constants.NUMBER_OF_ITERATIONS):
        start_time = time.process_time()

        num_rollouts = 0
        for _ in range(num_interations):
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.to_play, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def get_best_move(self):
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    def register_move(self, move):
        if move in self.root.children:
            self.root_state.register_move(move)
            self.root = self.root.children[move]
            return

        self.root_state.register_move(move)
        self.root = self.node_type(None, None)

    def move_next(self):
        self.search()
        num_rollouts, run_time = self.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = self.get_best_move()
        self.register_move(move)
        return move

    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time
