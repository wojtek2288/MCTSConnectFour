import random
import time

from Connect4State import Connect4State
from mcts import MCTS

def main():
    print("Choose option:\n")
    print("1. Play against MCTS AI")
    print("2. Play against random AI")

    option = int(input("Enter option:"))
    while option != 1 and option != 2:
        print("Illegal option")
        option = int(input("Enter option: "))

    if option == 1:
        play_mcts()
    elif option == 2:
        play_random()

def play_random():
    state = Connect4State()

    while not state.game_over():
        print("Current state:")
        state.print()

        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        state.move(user_move)

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")
        time.sleep(2)
        move = random.choice(state.get_legal_moves())

        print("Random AI choose move: ", move)

        state.move(move)

        if state.game_over():
            state.print()
            print("Player two won!")
            break

def play_mcts():
    state = Connect4State()
    mcts = MCTS(state)

    while not state.game_over():
        print("Current state:")
        state.print()

        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        state.move(user_move)
        mcts.move(user_move)

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search()
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.get_best_move()

        print("MCTS AI choose move: ", move)

        state.move(move)
        mcts.move(move)

        if state.game_over():
            state.print()
            print("Player two won!")
            break

if __name__ == "__main__":
    main()
