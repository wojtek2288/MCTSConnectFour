import math
import random
from copy import deepcopy

from state import State
from mcts import MCTS, Node, Constants

class AmafNode(Node):
    def __init__(self, move, parent):
        super().__init__(move, parent)
        self.AMAF = {}

    def amaf_value(self):
        if self.move in self.AMAF:
            amaf_stats = self.AMAF[self.move]
            if amaf_stats['N'] == 0:
                return 0
            else:
                return (amaf_stats['Q'] / amaf_stats['N']) + math.sqrt(math.log(self.parent.N) / amaf_stats['N'])
        else:
            return 0

class AmafMCTS(MCTS):
    def __init__(self, state=State()):
        super().__init__(state)
        self.root = AmafNode(None, None)
        self.node_type = AmafNode


    def select(self):
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_child = max(children, key=lambda n: n.UCT() + n.amaf_value())

            max_value = max_child.UCT() + max_child.amaf_value()
            max_nodes = [n for n in children if n.UCT() + n.amaf_value() == max_value]

            node = random.choice(max_nodes)
            state.register_move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.register_move(node.move)

        return node, state
    
    def update_amaf_stats(self, node: AmafNode, move: int, outcome: int):
        if move not in node.AMAF:
            node.AMAF[move] = {'N': 0, 'Q': 0}

        node.AMAF[move]['N'] += 1
        node.AMAF[move]['Q'] += outcome

    def search(self, num_interations: int = Constants.NUMBER_OF_ITERATIONS):
        for _ in range(num_interations):
            node, state = self.select()
            outcome = self.simulate(state)
            self.back_propagate(node, state, outcome)
            self.update_amaf_stats(self.root, node.move, outcome)


