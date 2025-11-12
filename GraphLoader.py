import networkx as nx


# def load_graph(file_path):
#     """
#     Convert an edge list file to a NetworkX graph
#     and return the number of nodes and edges.
#     """
#     try:
#         # Read the edge list file directly with NetworkX
#         # The file contains space-separated node pairs (from_node to_node)
#         G = nx.read_edgelist(file_path, nodetype=int)
#
#         # Count nodes and edges
#         num_nodes = G.number_of_nodes()
#         num_edges = G.number_of_edges()
#
#         # Output results
#         print(f"Graph Analysis Results:")
#         print(f"Number of nodes: {num_nodes}")
#         print(f"Number of edges: {num_edges}")
#         print(f"Graph type: {'Directed' if G.is_directed() else 'Undirected'}")
#
#         return G, num_nodes, num_edges
#
#     except Exception as e:
#         print(f"Error processing the edge list file: {e}")
#         return None, 0, 0
#
#
# # # Alternative manual approach if you need more control
# # def manual_edgelist_to_networkx(file_path):
# #     """
# #     Manually read edge list and create NetworkX graph.
# #     """
# #     try:
# #         # Create empty graph
# #         G = nx.Graph()  # Use nx.DiGraph() for directed graphs
# #
# #         # Read file line by line
# #         with open(file_path, 'r') as f:
# #             for line in f:
# #                 # Skip empty lines
# #                 if line.strip():
# #                     # Split the line and convert to integers
# #                     from_node, to_node = map(int, line.strip().split())
# #                     # Add edge to graph
# #                     G.add_edge(from_node, to_node)
# #
# #         # Count nodes and edges
# #         num_nodes = G.number_of_nodes()
# #         num_edges = G.number_of_edges()
# #
# #         # Output results
# #         print(f"Graph Analysis Results:")
# #         print(f"Number of nodes: {num_nodes}")
# #         print(f"Number of edges: {num_edges}")
# #         print(f"Graph type: {'Directed' if G.is_directed() else 'Undirected'}")
# #
# #         return G, num_nodes, num_edges
# #
# #     except Exception as e:
# #         print(f"Error processing the edge list file: {e}")
# #         return None, 0, 0
# #
# # def convert_tab_to_comma(input_file_path, output_file_path):
# #     """
# #     Reads a tab-separated file and writes a comma-separated file.
# #     """
# #     with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
# #         for line in infile:
# #             # Replace each tab character with a comma
# #             new_line = line.replace('\t', ',')
# #             outfile.write(new_line)
#
# # Usage
# if __name__ == "__main__":
#     file_path = r"C:\Users\zayad\PycharmProjects\CommunityDiscoveryDSP\facebook_combined.txt"
#
#     print("Method 1: Using NetworkX read_edgelist")
#     graph1, nodes1, edges1 = load_graph(file_path)

import networkx as nx
from typing import Optional


class GraphLoader:
    """Loads graphs from tab-separated edge list files."""

    @staticmethod
    def load_graph(file_path: str) -> Optional[nx.Graph]:
        """
        Load a NetworkX graph from a tab-separated edge list file.

        Args:
            file_path: Path to tab-separated edge list file

        Returns:
            NetworkX Graph object or None if loading fails
        """
        try:
            return nx.read_edgelist(file_path, nodetype=int)
        except Exception as e:
            print(f"Error loading graph from {file_path}: {e}")
            return None


# Usage
if __name__ == "__main__":
    loader = GraphLoader()
    file_path = "datasets/facebook_combined.txt"

    graph = loader.load_graph(file_path)

    if graph:
        print(f"Successfully loaded graph with {graph.number_of_nodes()} nodes, and {graph.number_of_edges()} edges")

