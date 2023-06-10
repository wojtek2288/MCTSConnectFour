from Connect4State import Connect4State
from mcts import MCTS
from mcts_amaf import AmafMCTS

def start_game(algorithm):
    state = Connect4State()
    algorithm = algorithm(state)

    while not state.game_over():
        print("Current state:")
        state.print_state()

        while True:
            move = int(input("Enter a column number to move: "))
            if move in state.get_legal_moves():
                break
            else:
                print("Please input a legal move.")

        state.register_move(move)
        algorithm.register_move(move)

        state.print_state()

        if state.game_over():
            print("Player one won!")
            break

        algorithm_move = algorithm.move_next()

        state.register_move(algorithm_move)

        print("Opponent's move choice: ", algorithm_move)

        if state.game_over():
            state.print_state()
            print("Player two won!")
            break

if __name__ == "__main__":
    modes = [["Player vs MCTS AI", MCTS], ["Player vs AmafMCTS AI", AmafMCTS]]
    for id, mode in enumerate(modes):
        print(f'{id + 1}. {mode[0]}')

    choice = int(input("Please choose game mode: "))

    if choice not in range(len(modes) + 1):
        print("Incorrect game mode selected. Exiting.")
    
    start_game(modes[choice - 1][1])