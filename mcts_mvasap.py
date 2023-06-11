import random
import math
from copy import deepcopy

from state import State, GameResults
from mcts import MCTS, Constants

class MvasapNode:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}
        self.visited_count = 0

    def add_children(self, children: dict):
        for child in children:
            self.children[child.move] = child

    def UCT(self):
        return Constants.INF if self.N == 0 else self.Q / self.N + Constants.EXPLORATION_COEFFICIENT * math.sqrt(math.log(self.parent.N) / self.N)


class MvasapMCTS(MCTS):
    def __init__(self, state=State(), seed=1):
        super().__init__(state, seed)
        self.root = MvasapNode(None, None)
        self.node_count = 0
        self.node_type = MvasapNode

    def select(self):
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            node = self.get_best_child(node)
            state.register_move(node.move)
            node.visited_count += 1

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.register_move(node.move)

        return node, state
    
    def get_best_child(self, node):
        children = node.children.values()
        max_value = max(children, key=lambda n: n.UCT()).UCT()
        max_nodes = [n for n in children if n.UCT() == max_value]
        max_nodes_with_lowest_visited_count = max(max_nodes, key=lambda n: n.visited_count)
        return max_nodes_with_lowest_visited_count

