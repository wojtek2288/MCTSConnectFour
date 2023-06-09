import random
import time
import math
from copy import deepcopy

from Connect4State import Connect4State
from meta import GameMeta, MCTSMeta

class AmafNode:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.AMAF = {}
        self.children = {}
        self.outcome = GameMeta.PLAYERS['none']

    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child

    def value(self, explore: float = MCTSMeta.EXPLORATION):
        if self.N == 0:
            return 0 if explore == 0 else GameMeta.INF
        else:
            return (self.Q / self.N) + explore * math.sqrt(math.log(self.parent.N) / self.N)

    def amaf_value(self):
        if self.move in self.AMAF:
            amaf_stats = self.AMAF[self.move]
            if amaf_stats['N'] == 0:
                return 0
            else:
                return (amaf_stats['Q'] / amaf_stats['N']) + math.sqrt(math.log(self.parent.N) / amaf_stats['N'])
        else:
            return 0

class AmafMCTS:
    def __init__(self, state=Connect4State()):
        self.root_state = deepcopy(state)
        self.root = AmafNode(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    def select_node(self) -> tuple:
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_child = max(children, key=lambda n: n.value() + n.amaf_value())

            max_value = max_child.value() + max_child.amaf_value()
            max_nodes = [n for n in children if n.value() + n.amaf_value() == max_value]

            node = random.choice(max_nodes)
            state.move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.move(node.move)

        return node, state

    def expand(self, parent: AmafNode, state: Connect4State) -> bool:
        if state.game_over():
            return False

        children = [AmafNode(move, parent) for move in state.get_legal_moves()]
        parent.add_children(children)

        return True

    def roll_out(self, state: Connect4State) -> int:
        while not state.game_over():
            state.move(random.choice(state.get_legal_moves()))

        return state.get_outcome()

    def back_propagate(self, node: AmafNode, turn: int, outcome: int) -> None:
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward

    def update_amaf_stats(self, node: AmafNode, move: int, outcome: int) -> None:
        if move not in node.AMAF:
            node.AMAF[move] = {'N': 0, 'Q': 0}

        node.AMAF[move]['N'] += 1
        node.AMAF[move]['Q'] += outcome

    def search(self, num_interations: int = MCTSMeta.NUM_ITERATIONS):
        start_time = time.process_time()

        num_rollouts = 0
        for _ in range(num_interations):
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.to_play, outcome)
            self.update_amaf_stats(self.root, node.move, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def get_best_move(self):
        if self.root_state.game_over():
            return -1

        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    def move(self, move):
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return

        self.root_state.move(move)
        self.root = AmafNode(None, None)

    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time
