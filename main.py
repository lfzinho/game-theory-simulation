import sys
import os

# Ensure the simulation can find modules in the src/ directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from player_classes import *
from game_machine import *
from graph import *
from plotter import Plotter


CONSECUTIVE_MOVES = 10
EPOCHS = 12
GAME_MACHINES = {
    "Prisioner`s Dilemma": GameMachine(
        payoff_matrix={
            Move.COOPERATE: {Move.COOPERATE: (2, 2), Move.DEFECT: (0, 3)},
            Move.DEFECT: {Move.COOPERATE: (3, 0), Move.DEFECT: (1, 1)},
        }
    ),
    "Chicken": GameMachine(
        payoff_matrix={
            Move.COOPERATE: {Move.COOPERATE: (0, 0), Move.DEFECT: (-1, 1)},
            Move.DEFECT: {Move.COOPERATE: (1, -1), Move.DEFECT: (-2, -2)},
        }
    ),
    "Stag Hunt": GameMachine(
        payoff_matrix={
            Move.COOPERATE: {Move.COOPERATE: (3, 3), Move.DEFECT: (0, 2)},
            Move.DEFECT: {Move.COOPERATE: (2, 0), Move.DEFECT: (1, 1)},
        }
    ),
    "Battle of the Sexes": GameMachine(
        payoff_matrix={
            Move.COOPERATE: {Move.COOPERATE: (2, 1), Move.DEFECT: (0, 0)},
            Move.DEFECT: {Move.COOPERATE: (0, 0), Move.DEFECT: (1, 2)},
        }
    ),
}


def generate_players():
    return [
        AlwaysCooperatePlayer(),
        AlwaysCooperatePlayer(),
        AlwaysCooperatePlayer(),
        AlwaysCooperatePlayer(),
        AlwaysDefectPlayer(),
        AlwaysDefectPlayer(),
        AlwaysDefectPlayer(),
        AlwaysDefectPlayer(),
        TitForTatPlayer(),
        TitForTatPlayer(),
        TitForTatPlayer(),
        TitForTatPlayer(),
        SuspiciousTitForTatPlayer(),
        SuspiciousTitForTatPlayer(),
        SuspiciousTitForTatPlayer(),
        SuspiciousTitForTatPlayer(),
        TitForTwoTatsPlayer(),
        TitForTwoTatsPlayer(),
        TitForTwoTatsPlayer(),
        TitForTwoTatsPlayer(),
        TatForTitPlayer(),
        TatForTitPlayer(),
        TatForTitPlayer(),
        TatForTitPlayer(),
        RandomPlayer(),
        RandomPlayer(),
        RandomPlayer(),
        RandomPlayer(),
    ]


def run_epoch(players, game_machine, game_graph):
    results = {}
    for edge in game_graph.get_edges():
        player_1 = players[edge[0]]
        player_2 = players[edge[1]]
        for i in range(CONSECUTIVE_MOVES):
            game_machine.play_game(player_1, player_2)
        results[(player_1.name, player_2.name)] = (player_1.score, player_2.score)
        player_1.finish_game()
        player_2.finish_game()
    return results


def simulation_step(players, death_threshold=0.25, reproduction_threshold=0.75):
    n = len(players)

    # assign survivability scores
    players_copy = players.copy()
    players_copy.sort(key=lambda x: x.run_score, reverse=False)
    for i, player in enumerate(players_copy):
        player.survivability_score = i / (n - 1)

    # eliminate bottom 25% and reproduce top 75%
    new_generation = []
    for i in range(n):
        player_i = players[i]
        if player_i.survivability_score < death_threshold:
            pass
        elif (
            player_i.survivability_score >= death_threshold
            and player_i.survivability_score < reproduction_threshold
        ):
            new_generation.append(player_i)
        else:
            new_generation.append(player_i)
            new_generation.append(player_i.copy())

    for player in new_generation:
        player.run_score = 0

    return new_generation


def main():
    game_plotter = Plotter()
    results = {}
    for game_name, game_machine in GAME_MACHINES.items():
        players = generate_players()
        game_graph = FullyConnectedGraph(len(players))

        # Record initial population
        game_plotter.record_epoch(game_name, 0, players)

        for i in range(EPOCHS):
            run_epoch(players, game_machine, game_graph)
            # print(f"Epoch {i+1} completed")
            for j, player in enumerate(players):
                # print(j, player.strategy_name, player.run_score)
                pass
            players = simulation_step(players)

            # Record population after reproduction and death
            game_plotter.record_epoch(game_name, i + 1, players)
            # print()

        print(f"Final population for {game_name}:\n")
        for i, player in enumerate(players):
            print(i, player.strategy_name)
        print()

    print("Generating CSVs and Plots...")
    game_plotter.export_and_plot(output_dir="output")
    print("Export complete. Check the 'output' directory.")


if __name__ == "__main__":
    main()
