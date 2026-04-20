# Game Theory Simulation

This project simulates evolutionary game theory by pitting various decision-making strategies against one another in classic game theoretical environments. Players in a graph engage in repeated matches for a set amount of epochs. At the end of every epoch, the bottom performers "die off" and upper performers "reproduce." Over several epochs, we observe which strategies dominate the population based on survival of the fittest.

## Available Graph Topologies
Because relationships between populations dictate survival, this simulation structures population matchups across several universal mathematical topologies:
1. **Fully Connected**: Every player battles every other player. Provides pure strategic baseline benchmarks without positional limits.
2. **Cycle**: A 1D ring lattice where each player only interacts with their immediate left/right neighbors.
3. **Small World**: (Watts-Strogatz) A ring lattice where arbitrary edges are randomly re-wired across the world, creating "shortcuts" that mimic human social networks.
4. **Scale Free**: (Barabási–Albert) Preferential attachment simulating wealth disparity or "hubs" like the internet—a few nodes have massive connectivity, while most have very little.
5. **Erdős-Rényi**: A purely random probability structure.
6. **Grid**: A classic 2D spatial matrix arrangement heavily featured in biological cellular automata, restricting battles to North/South/East/West neighbors.

Below are the evolutionary tracking records for each game modeled natively against every network structure above.

---

## 1. Prisoner's Dilemma
**The Idea / Analogy:** Two suspects are arrested, but police don't have enough evidence for a major conviction. They offer each suspect a deal: betray your partner (Defect) or stay silent (Cooperate). The dilemma is that mutual cooperation yields a better collective outcome, but individual temptation makes defecting strictly better for a single player.

**Prizes (Payoff Matrix):**
*   **Cooperate / Cooperate:** Both get 2 points.
*   **Defect / Cooperate:** Defector gets 3 points, Cooperator gets 0.
*   **Cooperate / Defect:** Cooperator gets 0 points, Defector gets 3.
*   **Defect / Defect:** Both get 1 point.

<details>
<summary><b>Click to View Topologies</b></summary>
<br>

### Fully Connected
![Fully Connected](output/prisoner's_dilemma_-_fully_connected.png)
### Cycle
![Cycle](output/prisoner's_dilemma_-_cycle.png)
### Small World
![Small World](output/prisoner's_dilemma_-_small_world.png)
### Scale Free
![Scale Free](output/prisoner's_dilemma_-_scale_free.png)
### Erdős-Rényi
![Erdos-Renyi](output/prisoner's_dilemma_-_erdos-renyi.png)
### 2D Grid
![Grid](output/prisoner's_dilemma_-_grid.png)
</details>

---

## 2. Chicken
**The Idea / Analogy:** Two drivers are on a collision course. The one who swerves first (Cooperates) is the "chicken" and loses face. The one who keeps driving straight (Defects) wins. However, if neither swerves (Mutual Defection), they crash, leading to the worst possible outcome for both.

**Prizes (Payoff Matrix):**
*   **Cooperate / Cooperate:** Both get 0 points (tie).
*   **Defect / Cooperate:** Defector gets 1 point, Cooperator gets -1.
*   **Cooperate / Defect:** Cooperator gets -1 points, Defector gets 1.
*   **Defect / Defect:** Both get -2 points (crash).

<details>
<summary><b>Click to View Topologies</b></summary>
<br>

### Fully Connected
![Fully Connected](output/chicken_-_fully_connected.png)
### Cycle
![Cycle](output/chicken_-_cycle.png)
### Small World
![Small World](output/chicken_-_small_world.png)
### Scale Free
![Scale Free](output/chicken_-_scale_free.png)
### Erdős-Rényi
![Erdos-Renyi](output/chicken_-_erdos-renyi.png)
### 2D Grid
![Grid](output/chicken_-_grid.png)
</details>

---

## 3. Stag Hunt
**The Idea / Analogy:** Two individuals go out on a hunt. They can either cooperate to hunt a large stag, or individually hunt small rabbits. The stag requires cooperation to catch and yields a massive reward. A rabbit can be caught alone but yields a tiny reward. The safest play is the rabbit, but the highest reward requires trusting the other person.

**Prizes (Payoff Matrix):**
*   **Cooperate / Cooperate:** Both get 3 points (Stag).
*   **Defect / Cooperate:** Defector gets 2 points (Rabbit), Cooperator gets 0.
*   **Cooperate / Defect:** Cooperator gets 0 points, Defector gets 2 (Rabbit).
*   **Defect / Defect:** Both get 1 point (Rabbit each).

<details>
<summary><b>Click to View Topologies</b></summary>
<br>

### Fully Connected
![Fully Connected](output/stag_hunt_-_fully_connected.png)
### Cycle
![Cycle](output/stag_hunt_-_cycle.png)
### Small World
![Small World](output/stag_hunt_-_small_world.png)
### Scale Free
![Scale Free](output/stag_hunt_-_scale_free.png)
### Erdős-Rényi
![Erdos-Renyi](output/stag_hunt_-_erdos-renyi.png)
### 2D Grid
![Grid](output/stag_hunt_-_grid.png)
</details>

---

## 4. Battle of the Sexes
**The Idea / Analogy:** A couple wants to go to an event together but prefer different events (e.g., Opera vs. Boxing). They would rather be together at the event they dislike than apart at the event they like. The game focuses heavily on coordination rather than deception.

**Prizes (Payoff Matrix):**
*   **Cooperate / Cooperate:** Player A gets 2, Player B gets 1 (Event 1).
*   **Defect / Cooperate:** Both get 0 (Miskoordination).
*   **Cooperate / Defect:** Both get 0 (Miskoordination).
*   **Defect / Defect:** Player A gets 1, Player B gets 2 (Event 2).

<details>
<summary><b>Click to View Topologies</b></summary>
<br>

### Fully Connected
![Fully Connected](output/battle_of_the_sexes_-_fully_connected.png)
### Cycle
![Cycle](output/battle_of_the_sexes_-_cycle.png)
### Small World
![Small World](output/battle_of_the_sexes_-_small_world.png)
### Scale Free
![Scale Free](output/battle_of_the_sexes_-_scale_free.png)
### Erdős-Rényi
![Erdos-Renyi](output/battle_of_the_sexes_-_erdos-renyi.png)
### 2D Grid
![Grid](output/battle_of_the_sexes_-_grid.png)
</details>
