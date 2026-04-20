import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from player_classes import *
from game_machine import *
from graph import *
from main import generate_players, run_epoch, GAME_MACHINES, simulation_step

game_machine = GAME_MACHINES["Prisioner`s Dilemma"]
players = generate_players()
game_graph = FullyConnectedGraph(len(players))

run_epoch(players, game_machine, game_graph)

n = len(players)
players_copy = players.copy()
players_copy.sort(key=lambda x: x.run_score, reverse=False)

for i, p in enumerate(players_copy):
    print(f"{i}: {p.strategy_name} - score: {p.run_score}")
