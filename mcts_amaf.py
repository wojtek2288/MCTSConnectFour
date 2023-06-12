import math
from mcts import MCTS, Constants, Node

from state import State, GameResults

class AmafConstants(Constants):
    UCT_AMAF_RATIO = 1.5

class AmafNode(Node):
    def __init__(self, move, parent):
        super().__init__(move, parent)
        self.AMAF_N = 0
        self.AMAF_Q = 0

    def AMAF_UCT(self):
        return AmafConstants.INF if self.UCT_N == 0 else (self.UCT_Q + self.AMAF_Q) / (self.UCT_N + self.AMAF_N) + AmafConstants.EXPLORATION_COEFFICIENT * math.sqrt(math.log(self.parent.UCT_N) / (self.UCT_N + self.AMAF_N))

class AmafMCTS(MCTS):
    def __init__(self, state=State(), seed=1):
        super().__init__(state, seed)
        self.root = AmafNode(None, None)
        self.node_count = 0
        self.node_type = AmafNode

    def get_best_child(self, node):
        children = node.children.values()
        max_value = max(children, key = lambda node: AmafConstants.UCT_AMAF_RATIO * node.UCT() + node.AMAF_UCT())
        return self.random.choice([node for node in children if AmafConstants.UCT_AMAF_RATIO * node.UCT() + node.AMAF_UCT() == AmafConstants.UCT_AMAF_RATIO * max_value.UCT() + max_value.AMAF_UCT()])

    def back_propagate(self, node: AmafNode, turn: int, outcome: int):
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.UCT_N += 1
            node.UCT_Q += reward
            if node.parent is not None:
                node.parent.AMAF_N += 1
                node.parent.AMAF_Q += reward
            node = node.parent
            if outcome == GameResults.DRAW:
                reward = 0
            else:
                reward = 1 - reward
