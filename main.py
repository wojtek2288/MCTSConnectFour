import time
import random
import itertools
import multiprocessing
from mcts_connect4 import Connect4MCTS

from mcts_mvasap import MvasapMCTS

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

def computer_vs_computer(algorithm1, algorithm2, seed):
    state = State()
    algorithm1 = algorithm1(state, seed)
    algorithm2 = algorithm2(state, seed)

    while not state.game_over():
        state.print_state()

        move1 = algorithm1.move_next()
        algorithm2.register_move(move1)
        state.register_move(move1)

        state.print_state()

        if state.game_over():
            print("Player one won!")
            return 1

        move2 = algorithm2.move_next()
        state.register_move(move2)
        algorithm1.register_move(move2)

        #print("Opponent's move choice: ", algorithm_move)

        if state.game_over():
            state.print_state()
            print("Player two won!")
            return 2
    return 3

def welcome_to_the_grand_tournament_champion():
    competitors = [MCTS, MvasapMCTS, AmafMCTS]

    pairings = list(itertools.combinations(competitors, 2))
    pairings = pairings + [[y, x] for [x, y] in pairings]
    pairings = [[pairing[0], pairing[1], id] for id, pairing in enumerate(pairings)]
    results = []

    with multiprocessing.Pool() as pool:
        for result in pool.imap(run_pairing, pairings):
            results.append(result)

    print('\n===========RESULTS===========')
    for result in results:
        print(result)

def run_pairing(pairing):
    number_of_rounds = 10
    res_1 = 0
    res_2 = 0
    res_3 = 0
    for i in range(number_of_rounds):
        res = computer_vs_computer(pairing[0], pairing[1], i + pairing[2])
        if res == 1:
            res_1 += 1
        elif res == 2:
            res_2 += 1
        else:
            res_3 += 1
    return f'\n{pairing[0].__name__} vs {pairing[1].__name__}:\n{pairing[0].__name__} wins: {res_1}\n{pairing[1].__name__} wins: {res_2}\nDraws: {res_3}'

if __name__ == "__main__":
    #welcome_to_the_grand_tournament_champion()
    player_vs_computer(Connect4MCTS)
    # alg = int(input("1 - MCTS, 2 - AMAF: "))
    # if alg == 1:
    #     print("MCTS")
    #     player_vs_computer(MCTS)
    # elif alg == 2:
    #     print("AMAF")
    #     player_vs_computer(AmafMCTS)
    # computer_vs_computer(MCTS, AmafMCTS, 1)

    # modes = [["Player vs MCTS AI", MCTS], ["Player vs AmafMCTS AI", AmafMCTS]]
    # for id, mode in enumerate(modes):
    #     print(f'{id + 1}. {mode[0]}')

    # choice = int(input("Please choose game mode: "))

    # if choice not in range(len(modes) + 1):
    #     print("Incorrect game mode selected. Exiting.")
    
    # player_vs_computer(modes[choice - 1][1])