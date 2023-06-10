import time
import math

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

    def update_amaf_stats(self, node: AmafNode, move: int, outcome: int):
        if move not in node.AMAF:
            node.AMAF[move] = {'N': 0, 'Q': 0}

        node.AMAF[move]['N'] += 1
        node.AMAF[move]['Q'] += outcome

    def search(self, num_interations: int = Constants.NUMBER_OF_ITERATIONS):
        start_time = time.process_time()

        num_rollouts = 0
        for _ in range(num_interations):
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.player_to_play, outcome)
            self.update_amaf_stats(self.root, node.move, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

