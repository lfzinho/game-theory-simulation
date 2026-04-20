import sys
import os

# Ensure the simulation can find modules in the src/ directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from player_classes import *
from game_machine import *
from graph import *
from plotter import Plotter
from tqdm import tqdm
from collections import Counter


CONSECUTIVE_MOVES = 10
EPOCHS = 12
GAME_MACHINES = {
    "Prisoner's Dilemma": GameMachine(
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


def generate_players(instances_per_class=50):
    classes = [
        AlwaysCooperatePlayer,
        AlwaysDefectPlayer,
        TitForTatPlayer,
        SuspiciousTitForTatPlayer,
        TitForTwoTatsPlayer,
        TatForTitPlayer,
        RandomPlayer,
    ]
    players = []
    for cls in classes:
        for _ in range(instances_per_class):
            players.append(cls())
    return players


def run_epoch(players, game_machine, game_graph):
    results = {}
    for edge in game_graph.get_edges():
        player_1 = players[edge[0]]
        player_2 = players[edge[1]]
        for i in range(CONSECUTIVE_MOVES):
            game_machine.play_game(player_1, player_2)
        results[(edge[0], edge[1])] = (player_1.score, player_2.score)
        player_1.finish_game()
        player_2.finish_game()
    return results


def simulation_step(players, death_threshold=0.25, reproduction_threshold=0.75):
    import random
    n = len(players)

    # assign survivability scores
    # Randomly shuffle first so that players with identical run_scores don't 
    # receive survivability purely based on their original list positions.
    players_copy = players.copy()
    random.shuffle(players_copy)
    players_copy.sort(key=lambda x: x.run_score, reverse=False)
    for i, player in enumerate(players_copy):
        player.survivability_score = i / (n - 1) if n > 1 else 0.5

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


def get_graph_generators(n):
    return {
        "Fully Connected": lambda: FullyConnectedGraph(n),
        "Cycle": lambda: CycleGraph(n),
        "Small World": lambda: SmallWorldGraph(n, k=4, p=0.1),
        "Scale Free": lambda: BarabasiAlbertGraph(n, m=3),
        "Erdos-Renyi": lambda: ErdosRenyiGraph(n, p=0.2),
        "Grid": lambda: GridGraph(n, wrap_around=True)
    }


def main():
    game_plotter = Plotter()
    results = {}
    
    # Check baseline nodes
    baseline_nodes = len(generate_players(instances_per_class=50))
    graph_generators = get_graph_generators(baseline_nodes)

    for graph_name, graph_gen in graph_generators.items():
        for game_name, game_machine in GAME_MACHINES.items():
            run_name = f"{game_name} - {graph_name}"
            players = generate_players(instances_per_class=50)
            game_graph = graph_gen()
            
            # Record initial population
            game_plotter.record_epoch(run_name, 0, players)

            for i in tqdm(range(EPOCHS), desc=f"Simulating {run_name}", unit="epoch"):
                run_epoch(players, game_machine, game_graph)
                players = simulation_step(players)

                # Record population after reproduction and death
                game_plotter.record_epoch(run_name, i + 1, players)

            # Print concise summary
            counts = Counter(p.strategy_name for p in players)
            print(f"Final population for {run_name}:")
            for strategy, count in counts.most_common():
                print(f"  {strategy}: {count}")
            print()
        print()

    print("Generating CSVs and Plots...")
    game_plotter.export_and_plot(output_dir="output")
    print("Export complete. Check the 'output' directory.")


if __name__ == "__main__":
    main()
