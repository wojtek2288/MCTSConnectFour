import random
from copy import deepcopy

from state import State
from mcts import MCTS, Node

class MvasapNode(Node):
    def __init__(self, move, parent):
        super().__init__(move, parent)
        self.visited_count = 0


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
            state.register_move(node.move_before)
            node.visited_count += 1

            if node.UCT_N == 0:
                return node, state

        if self.expand(node, state):
            node = self.random.choice(list(node.children.values()))
            state.register_move(node.move_before)

        return node, state
    
    def get_best_child(self, node):
        children = node.children.values()
        max_value = max(children, key = lambda node: node.UCT()).UCT()
        max_nodes = [node for node in children if node.UCT() == max_value]
        max_nodes_with_highest_visited_count = max(max_nodes, key = lambda node: node.visited_count)
        return max_nodes_with_highest_visited_count

