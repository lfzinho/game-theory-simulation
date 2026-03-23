from abc import ABC, abstractmethod
import numpy as np


class Graph(ABC):
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.adj_matrix = np.zeros((num_nodes, num_nodes))
        self.edge_values = np.empty((num_nodes, num_nodes), dtype=object)

    def add_edge(self, u, v):
        self.adj_matrix[u][v] = 1
        self.adj_matrix[v][u] = 1

    def set_edge_value(self, u, v, value):
        self.edge_values[u][v] = value
        self.edge_values[v][u] = value
    
    def get_edges(self):
        edges = []
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if self.adj_matrix[i][j] == 1:
                    edges.append((i, j))
        return edges


class FullyConnectedGraph(Graph):
    """Fully connected graph"""

    def __init__(self, num_nodes):
        super().__init__(num_nodes)
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                self.add_edge(i, j)


class CycleGraph(Graph):
    """Cycle graph"""

    def __init__(self, num_nodes):
        super().__init__(num_nodes)
        for i in range(num_nodes):
            self.add_edge(i, (i + 1) % num_nodes)


class SmallWorldGraph(Graph):
    """
    Watts-Strogatz Small World graph.
    Starts with a regular ring lattice and rewires edges with probability p.
    """

    def __init__(self, num_nodes, k, p):
        """
        Args:
            num_nodes: number of nodes
            k: each node is connected to k nearest neighbors in ring topology
            p: probability of rewiring each edge
        """
        super().__init__(num_nodes)
        if k % 2 != 0:
            k -= 1  # k must be even for a symmetric lattice

        # 1. Start with a ring lattice
        for i in range(num_nodes):
            for j in range(1, k // 2 + 1):
                self.add_edge(i, (i + j) % num_nodes)

        # 2. Rewire edges
        for i in range(num_nodes):
            # Only rewire the 'forward' edges to avoid double-visiting
            for j in range(1, k // 2 + 1):
                if np.random.rand() < p:
                    u = i
                    v = (i + j) % num_nodes
                    # Find a new target that is not the same node and not already connected
                    choices = [
                        n
                        for n in range(num_nodes)
                        if n != u and self.adj_matrix[u][n] == 0
                    ]
                    if choices:
                        # Remove old edge
                        self.adj_matrix[u][v] = 0
                        self.adj_matrix[v][u] = 0
                        # Add new edge
                        new_v = np.random.choice(choices)
                        self.add_edge(u, new_v)


class BarabasiAlbertGraph(Graph):
    """Scale-free graph (Preferential Attachment)"""

    def __init__(self, num_nodes, m):
        """
        Args:
            num_nodes: total number of nodes
            m: number of edges to attach from a new node to existing nodes
        """
        super().__init__(num_nodes)

        # 1. Start with a small clique (fully connected core) of m + 1 nodes
        initial_nodes = m + 1
        for i in range(initial_nodes):
            for j in range(i + 1, initial_nodes):
                self.add_edge(i, j)

        # 2. Add the remaining nodes one by one
        for i in range(initial_nodes, num_nodes):
            # Calculate current degree of all existing nodes (sum of rows in adj matrix)
            degrees = np.sum(self.adj_matrix[:i, :i], axis=1)
            total_degree = np.sum(degrees)

            # Probability of connecting to node j is proportional to its degree
            probabilities = degrees / total_degree

            # Select m unique nodes to connect to based on probabilities
            targets = np.random.choice(range(i), size=m, replace=False, p=probabilities)

            for target in targets:
                self.add_edge(target, i)
