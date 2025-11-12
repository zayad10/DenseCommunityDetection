from abc import ABC, abstractmethod
import networkx as nx
import dsd
import time
import heapq
import numpy as np
import time
from dsd import exact_densest

import numpy as np
from dsd import flowless
from dsd.fibheap import FibonacciHeap

from Datasets import Datasets




# Strategy Interface
class AlgorithmStrategy:
    @abstractmethod
    def apply_algorithm(self, undirected_dataset_graph):
        pass

    @staticmethod
    def subgraph_density(graph, nodes):
        """Calculate the density of a subgraph given its nodes"""
        if len(nodes) == 0:
            return 0.0
        subgraph = graph.subgraph(nodes)
        num_edges = subgraph.number_of_edges()
        num_nodes = len(nodes)
        return num_edges / num_nodes if num_nodes > 0 else 0.0

class CharikarsGreedy(AlgorithmStrategy):
    def __init__(self):
        self.algorithm_name = "Charikars Greedy"

    def apply_algorithm(self, undirected_dataset_graph):
        if undirected_dataset_graph.number_of_nodes() == 0:
            return set(), 0.0

        current_subgraph = undirected_dataset_graph.copy()
        current_subgraph_nodes = set(current_subgraph.nodes())

        best_density = 0.0
        best_subgraph_nodes = set(current_subgraph.nodes())

        while len(current_subgraph_nodes) > 0:
            num_edges = current_subgraph.number_of_edges()
            num_nodes = len(current_subgraph_nodes)
            current_density = num_edges / num_nodes if num_nodes > 0 else 0.0

            if current_density > best_density:
                best_density = current_density
                best_subgraph_nodes = current_subgraph_nodes.copy()

            min_vertex = min(current_subgraph_nodes, key=lambda v: (current_subgraph.degree(v), str(v)))

            current_subgraph_nodes.remove(min_vertex)
            current_subgraph.remove_node(min_vertex)

        return best_subgraph_nodes

class CharikarsGreedyMinHeap(AlgorithmStrategy):
    def __init__(self):
        self.algorithm_name = "Charikars Greedy Using MinHeap"

    def apply_algorithm(self, dataset_graph):
        h = dataset_graph.copy()
        remaining_nodes = set(h.nodes())

        # Initialize a min-heap with (degree, node) tuples
        heap = [(h.degree(node), node) for node in remaining_nodes]
        heapq.heapify(heap)

        best_density = 0.0
        best_subgraph_nodes = set()

        while remaining_nodes:
            num_edges = h.number_of_edges()
            num_nodes = len(remaining_nodes)
            current_density = num_edges / num_nodes if num_nodes > 0 else 0.0

            if current_density > best_density:
                best_density = current_density
                best_subgraph_nodes = remaining_nodes.copy()

            # Pop nodes from heap until we find one that is still valid
            min_vertex = None
            while heap:
                degree, node = heapq.heappop(heap)
                if node in remaining_nodes and h.degree(node) == degree:
                    min_vertex = node
                    break

            if min_vertex is None:
                break

            # Remove the selected node
            remaining_nodes.remove(min_vertex)

            # Get neighbors before removing the node
            neighbors = list(h.neighbors(min_vertex))
            h.remove_node(min_vertex)

            # Update the heap with new degrees of neighbors
            for neighbor in neighbors:
                if neighbor in remaining_nodes:
                    heapq.heappush(heap, (h.degree(neighbor), neighbor))

        return best_subgraph_nodes

class CharikarsGreedyFibonacciHeap(AlgorithmStrategy):
    def __init__(self):
        self.algorithm_name = "Charikars Greedy Using Fibonacci Heap"

    def apply_algorithm(self, dataset_graph):
        h = dataset_graph.copy()
        remaining_nodes = set(h.nodes())
        fh = FibonacciHeap()
        node_to_entry = {}

        # Initialize Fibonacci heap with node degrees
        for node in remaining_nodes:
            entry = fh.insert(h.degree(node), node)
            node_to_entry[node] = entry

        best_density = 0.0
        best_subgraph = set()

        while remaining_nodes:
            num_edges = h.number_of_edges()
            num_nodes = len(remaining_nodes)
            current_density = num_edges / num_nodes if num_nodes > 0 else 0.0

            if current_density > best_density:
                best_density = current_density
                best_subgraph = set(remaining_nodes)

            # Extract minimum degree node
            min_entry = fh.extract_min()
            if not min_entry:
                break
            min_degree, min_vertex = min_entry.key, min_entry.value

            # Validate entry (handle stale degrees)
            if min_vertex not in remaining_nodes or h.degree(min_vertex) != min_degree:
                continue

            # Remove node from tracking structures
            remaining_nodes.remove(min_vertex)
            del node_to_entry[min_vertex]

            # Process neighbors before removal
            neighbors = list(h.neighbors(min_vertex))
            h.remove_node(min_vertex)

            # Update neighbor degrees in Fibonacci heap
            for neighbor in neighbors:
                if neighbor in remaining_nodes:
                    new_degree = h.degree(neighbor)
                    try:
                        fh.decrease_key(node_to_entry[neighbor], new_degree)
                    except ValueError:
                        # Handle cases where new degree isn't smaller
                        pass

        return best_subgraph

class GreedyPlusPlus(AlgorithmStrategy):
    def __init__(self):
        self.algorithm_name = "Greedy++ (Flowless)"

    def apply_algorithm(self, undirected_dataset_graph, iterations=10):
        if undirected_dataset_graph.number_of_nodes() == 0:
            return set(), 0.0

        max_density_nodes = set(undirected_dataset_graph.nodes)
        max_density = 0.0

        if undirected_dataset_graph.number_of_edges() > 0:
            max_density = undirected_dataset_graph.number_of_edges() / len(max_density_nodes)

        vertex_loads = {vertex: 0 for vertex in undirected_dataset_graph.nodes}

        for i in range(iterations):
            current_subgraph = undirected_dataset_graph.copy()
            current_subgraph_nodes = set(current_subgraph.nodes)

            while current_subgraph_nodes:
                # Find node with minimum (load + degree)
                min_vertex = min(current_subgraph_nodes,
                                 key=lambda v: (vertex_loads[v] + current_subgraph.degree(v), str(v)))
                min_vertex_degree = current_subgraph.degree(min_vertex)
                vertex_loads[min_vertex] += min_vertex_degree

                current_subgraph_nodes.remove(min_vertex)
                current_subgraph.remove_node(min_vertex)

                if not current_subgraph_nodes:
                    continue

                current_subgraph_density = current_subgraph.number_of_edges() / len(current_subgraph_nodes)

                if current_subgraph_density > max_density:
                    max_density = current_subgraph_density
                    max_density_nodes = set(current_subgraph_nodes)

        return max_density_nodes

class GreedyPlusPlusPriorityQueue(AlgorithmStrategy):
    def __init__(self):
        self.algorithm_name = "Greedy++ (Flowless) using Priority Queue"

    def apply_algorithm(self, undirected_dataset_graph, iterations=10):
        if undirected_dataset_graph.number_of_nodes() == 0:
            return set(), 0.0

        max_density_nodes = set(undirected_dataset_graph.nodes)
        max_density = 0.0

        if undirected_dataset_graph.number_of_edges() > 0:
            max_density = undirected_dataset_graph.number_of_edges() / len(max_density_nodes)

        vertex_loads = {vertex: 0 for vertex in undirected_dataset_graph.nodes}

        for i in range(iterations-1):
            current_subgraph = undirected_dataset_graph.copy()
            current_subgraph_nodes = set(current_subgraph.nodes)

            fib_heap = FibonacciHeap()
            node_map = {}

            # Insert all vertices with (load + degree) priority
            for vertex in current_subgraph_nodes:
                priority = vertex_loads[vertex] + current_subgraph.degree(vertex)
                node = fib_heap.insert(priority, vertex)
                node_map[vertex] = node

            for j in range(len(current_subgraph_nodes) - 1): # until there's one vertex left where the degree would be 0.
                # Extract minimum priority vertex
                min_node = fib_heap.extract_min()
                min_vertex = min_node.value
                min_vertex_degree = current_subgraph.degree(min_vertex)
                vertex_loads[min_vertex] += min_vertex_degree

                # Process neighbors before removal
                neighbours = list(current_subgraph.neighbors(min_vertex))

                # Remove vertex from subgraph
                current_subgraph.remove_node(min_vertex)
                current_subgraph_nodes.remove(min_vertex)
                del node_map[min_vertex]

                # Update neighbor priorities
                for neighbour in neighbours:
                    if neighbour in node_map:
                        new_neighbour_priority = vertex_loads[neighbour] + current_subgraph.degree(neighbour)
                        fib_heap.decrease_key(node_map[neighbour], new_neighbour_priority)

                # Update maximum density
                if current_subgraph_nodes:
                    current_density = current_subgraph.number_of_edges() / len(current_subgraph_nodes)
                    if current_density > max_density:
                        max_density = current_density
                        max_density_nodes = set(current_subgraph_nodes)

        return max_density_nodes

class GoldbergsMaxDensitySubgraph(AlgorithmStrategy):
    def __init__(self):
        self.algorithm_name = "Goldberg's Maximum Density Subgraph"

    def apply_algorithm(self, undirected_dataset_graph):
        graph_nodes = undirected_dataset_graph.nodes
        if len(graph_nodes) == 0:
            return set(), 0.0

        n = len(graph_nodes)
        m = undirected_dataset_graph.number_of_edges()
        l = 0.0
        u = float(m)
        v1 = set()

        if m == 0:
            return set(list(graph_nodes)[:1]) if n > 0 else set(), 0.0

        smallest_possible_difference = 1.0 / (n * (n - 1)) if n > 1 else 1e-9
        iteration_count = 0
        degrees = dict(undirected_dataset_graph.degree())
        max_iterations = int(np.ceil(np.log2(m * n * (n - 1)))) + 10 # binary search convergence theory bound

        while u - l >= smallest_possible_difference and iteration_count < max_iterations:
            iteration_count += 1
            g = (u + l) / 2.0

            flow_graph = nx.DiGraph()
            source = 's'
            sink = 't'
            flow_graph.add_nodes_from([source, sink])
            flow_graph.add_nodes_from(graph_nodes)

            for u_node, v_node in undirected_dataset_graph.edges():
                flow_graph.add_edge(u_node, v_node, capacity=1)
                flow_graph.add_edge(v_node, u_node, capacity=1)

            for node in graph_nodes:
                flow_graph.add_edge(source, node, capacity=m)

            for node in graph_nodes:
                capacity = m + (2 * g) - degrees[node]
                flow_graph.add_edge(node, sink, capacity=capacity)

            try:
                cut_value, (S, T) = nx.minimum_cut(flow_graph, source, sink)

                if S == {source}:
                    u = g # No subgraph with density >= g will be found
                else:
                    l = g # A subgraph with density >= g exists
                    v1 = S - {source}

            except nx.NetworkXError:
                u = g # so that the binary search to get stuck or converge incorrectly so we treat it as "no denser subgraph found"
                continue

        return v1