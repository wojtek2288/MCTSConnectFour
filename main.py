import random
import time
import itertools
import multiprocessing
from mcts_connect4_opportunistic import Connect4OpportunisticMCTS

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
    algorithm1_time_sum = 0
    algorithm2_time_sum = 0
    algorithm1_counter = 0
    algorithm2_counter = 0

    while not state.game_over():
        state.print_state()
        start = time.process_time()
        move1 = algorithm1.move_next()
        algorithm1_counter += 1
        move_time = time.process_time() - start

        algorithm1_time_sum += move_time

        algorithm2.register_move(move1)
        state.register_move(move1)

        state.print_state()

        if state.game_over():
            print("Player one won!")
            return 1, algorithm1_time_sum / algorithm1_counter, algorithm2_time_sum / algorithm2_counter

        start = time.process_time()
        move2 = algorithm2.move_next()
        algorithm2_counter += 1
        move_time = time.process_time() - start

        algorithm2_time_sum += move_time

        state.register_move(move2)
        algorithm1.register_move(move2)

        #print("Opponent's move choice: ", algorithm_move)

        if state.game_over():
            state.print_state()
            print("Player two won!")
            return 2, algorithm1_time_sum / algorithm1_counter, algorithm2_time_sum / algorithm2_counter
    return 3, algorithm1_time_sum / algorithm1_counter, algorithm2_time_sum / algorithm2_counter

def welcome_to_the_grand_tournament_champion():
    competitors = [Connect4OpportunisticMCTS, MCTS, MvasapMCTS, AmafMCTS]

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
    t1_sum = 0
    t2_sum = 0
    for i in range(number_of_rounds):
        res, t1, t2 = computer_vs_computer(pairing[0], pairing[1], i + pairing[2])
        t1_sum += t1
        t2_sum += t2
        if res == 1:
            res_1 += 1
        elif res == 2:
            res_2 += 1
        else:
            res_3 += 1

    t1_avg = t1_sum / number_of_rounds
    t2_avg = t2_sum / number_of_rounds
    return f'\n{pairing[0].__name__} vs {pairing[1].__name__}:\n{pairing[0].__name__} wins: {res_1}\n{pairing[1].__name__} wins: {res_2}\nDraws: {res_3} \n {pairing[0].__name__} avarage time: {t1_avg}\n {pairing[1].__name__} avarage time: {t2_avg} \n'

def computer_vs_random(algorithm1, seed, start_with_random = True):
    state = State()
    algorithm1 = algorithm1(state, seed)
    random_wins = 0
    algorithm_wins = 0
    random_engine = random.Random(seed)

    while not state.game_over():

        if start_with_random:
            columns = state.get_empty_columns()
            move = random_engine.choice(columns)
            state.register_move(move)
            algorithm1.register_move(move)

            if state.game_over():
                random_wins += 1
                break

            algorithm_move = algorithm1.move_next()
            state.register_move(algorithm_move)

            if state.game_over():
                algorithm_wins += 1
                break
        else:
            algorithm_move = algorithm1.move_next()
            state.register_move(algorithm_move)

            if state.game_over():
                algorithm_wins += 1
                break

            columns = state.get_empty_columns()
            move = random_engine.choice(columns)
            state.register_move(move)
            algorithm1.register_move(move)

            if state.game_over():
                random_wins += 1
                break
    
    return algorithm_wins, random_wins

if __name__ == "__main__":
    alg_wins_sum = 0
    random_wins_sum = 0

    for i in range(10):
        print("Iteration: " + str(i))
        alg_wins, random_wins = computer_vs_random(MCTS, i)
        alg_wins_sum += alg_wins
        random_wins_sum += random_wins

    for i in range(10):
        print("Iteration: " + str(i))
        alg_wins, random_wins = computer_vs_random(MCTS, i, False)
        alg_wins_sum += alg_wins
        random_wins_sum += random_wins

    print("Alg wing: " + str(alg_wins_sum))
    print("Random wins: " + str(random_wins_sum))

    # player_vs_computer(ConnectTest4MCTS)
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