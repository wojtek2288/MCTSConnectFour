import time
import random

from state import State
from mcts import MCTS
from mcts_amaf import AmafMCTS

def player_vs_computer(algorithm):
    state = State()
    algorithm = algorithm(state)

    while not state.game_over():
        print("Current state:")
        state.print_state()

        while True:
            move = int(input("Enter a column number to move: "))
            move -= 1
            if move in state.get_empty_columns():
                break
            else:
                print("Please input a legal move.")

        state.register_move(move)
        algorithm.register_move(move)

        state.print_state()

        if state.game_over():
            print("Player one won!")
            break

        start = time.process_time()

        algorithm_move = algorithm.move_next()

        move_time = time.process_time() - start

        print(f'Algorithm move time: {move_time}s')

        state.register_move(algorithm_move)

        print("Opponent's move choice: ", algorithm_move)

        if state.game_over():
            state.print_state()
            print("Player two won!")
            break

def computer_vs_computer(algorithm1, algorithm2):
    state = State()
    algorithm1 = algorithm1(state)
    algorithm2 = algorithm2(state)

    while not state.game_over():
        state.print_state()

        move1 = algorithm1.move_next()
        algorithm2.register_move(move1)
        state.register_move(move1)

        state.print_state()

        if state.game_over():
            print("Player one won!")
            break

        move2 = algorithm2.move_next()
        state.register_move(move2)
        algorithm1.register_move(move2)

        #print("Opponent's move choice: ", algorithm_move)

        if state.game_over():
            state.print_state()
            print("Player two won!")
            break

if __name__ == "__main__":
    random.seed(1010)
    computer_vs_computer(MCTS, MCTS)

    # modes = [["Player vs MCTS AI", MCTS], ["Player vs AmafMCTS AI", AmafMCTS]]
    # for id, mode in enumerate(modes):
    #     print(f'{id + 1}. {mode[0]}')

    # choice = int(input("Please choose game mode: "))

    # if choice not in range(len(modes) + 1):
    #     print("Incorrect game mode selected. Exiting.")
    
    # player_vs_computer(modes[choice - 1][1])