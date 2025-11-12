import os
import uuid
from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D


class AlgorithmResultsViewer:
    def __init__(self):
        pass

    # def display_results(self, results):
    #     # Handle both single result and list of results
    #     if isinstance(results, dict):
    #         self._display_single_result(results)
    #     elif isinstance(results, list):
    #         for i, result in enumerate(results):
    #             if i > 0:  # Add spacing between results
    #                 print("\n")
    #             self._display_single_result(result)
    #     else:
    #         print("Error: Results must be a dictionary or list of dictionaries")

    @staticmethod
    def display_algorithm_and_dataset(algorithm_strategy, dataset):
        print("=" * 60)
        print(f"Algorithm: {type(algorithm_strategy).__name__}")
        print(
            f"Dataset: {dataset.number_of_nodes()} nodes, {dataset.number_of_edges()} edges")
        print("=" * 60)
        AlgorithmResultsViewer.display_please_wait()

    @staticmethod
    def display_please_wait():
        print("Please standby for the results of this experiment to be computed and displayed...")

    @staticmethod
    def display_evaluation_results(algorithm_evaluator):
        """
        Display comprehensive evaluation results from an AlgorithmEvaluator object.

        Parameters:
        -----------
        algorithm_evaluator : AlgorithmEvaluator
            The AlgorithmEvaluator object containing the evaluation results
        """
        print("*** Experiment Results ***")
        print(f"Running Time: {algorithm_evaluator.running_time:.6f} seconds")
        print(f"Memory Usage: {algorithm_evaluator.memory_used:.2f} MB")
        print(f"Identified Subgraph Size: {algorithm_evaluator.identified_subgraph_size} nodes")
        print(f"Identified Subgraph Density: {algorithm_evaluator.identified_subgraph_density:.6f}")

        # Handle optional optimal density
        if algorithm_evaluator.optimal_density is not None:
            print(f"Optimal Density: {algorithm_evaluator.optimal_density:.6f}")
        else:
            print("Optimal Density: Unknown")
        print(f"Densest Subgraph Similarity with Optimal: {algorithm_evaluator.optimal_nodes_overlap:.2f}%")
        print(f"Overall Accuracy: {algorithm_evaluator.accuracy:.2f}%")
        print("=" * 60)

    @staticmethod
    def draw_densest_component_zoom(
            graph, densest_subgraph_nodes,  # ← unchanged
            graph_name, algorithm_name, margin=2):

        if not densest_subgraph_nodes:  # guard – unchanged
            subgraph_to_draw = graph
            nodes_to_draw = list(graph.nodes())
        else:  # collect margin-hop neighbourhood
            nodes_to_draw = set(densest_subgraph_nodes)
            for _ in range(margin):
                neighbours = set()
                for v in nodes_to_draw:
                    neighbours.update(graph.neighbors(v))
                nodes_to_draw.update(neighbours)
            subgraph_to_draw = graph.subgraph(nodes_to_draw)

        densest_subgraph = graph.subgraph(densest_subgraph_nodes)

        # ─── figure with two side-by-side panels ────────────────────────────────
        fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 7))
        fig.suptitle(f"{graph_name} – densest-subgraph views using ({algorithm_name})",
                     fontsize=16, weight='bold')

        # -------- left: neighbourhood view -------------------------------------
        pos_left = nx.spring_layout(subgraph_to_draw, seed=42)  # layout once
        nx.draw_networkx_edges(subgraph_to_draw, pos_left,
                               alpha=0.3, edge_color='lightgray',
                               width=1, ax=ax_left)
        densest_edges = [(u, v) for u, v in subgraph_to_draw.edges()
                         if u in densest_subgraph_nodes and v in densest_subgraph_nodes]
        nx.draw_networkx_edges(subgraph_to_draw, pos_left, edgelist=densest_edges,
                               alpha=0.9, edge_color='red', width=2, ax=ax_left)

        node_colours = ['red' if n in densest_subgraph_nodes else 'lightblue'
                        for n in subgraph_to_draw.nodes()]
        nx.draw_networkx_nodes(subgraph_to_draw, pos_left, node_color=node_colours,
                               node_size=400, ax=ax_left)
        nx.draw_networkx_labels(subgraph_to_draw, pos_left, font_size=8,
                                font_weight='bold', ax=ax_left)
        ax_left.set_title(f"Margin {margin} hops – {len(subgraph_to_draw)} nodes", fontsize=12)
        ax_left.axis('off')

        # -------- right: induced densest subgraph ------------------------------
        pos_right = nx.spring_layout(densest_subgraph, seed=42)
        nx.draw_networkx_edges(densest_subgraph, pos_right,
                               alpha=0.8, edge_color='red', width=2, ax=ax_right)
        nx.draw_networkx_nodes(densest_subgraph, pos_right,
                               node_color='red', node_size=400, ax=ax_right)
        nx.draw_networkx_labels(densest_subgraph, pos_right, font_size=8,
                                font_weight='bold', ax=ax_right)
        ax_right.set_title(f"Induced densest subgraph – {len(densest_subgraph)} nodes",
                           fontsize=12)
        ax_right.axis('off')

        # one common legend (put it under the plots)
        legend_items = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red',
                   markersize=12, label='densest-subgraph node'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue',
                   markersize=12, label='neighbourhood node'),
            Line2D([0], [0], color='red', linewidth=2, label='densest-subgraph edge'),
            Line2D([0], [0], color='lightgray', linewidth=1, label='other edge')
        ]

        fig.legend(handles=legend_items, loc='lower center', ncol=4)
        AlgorithmResultsViewer.save_experiment_results_drawing(fig, graph_name, algorithm_name)

        plt.close(fig)  # free GUI backend

    @staticmethod
    def save_experiment_results_drawing(fig, graph_name, algorithm_name):
        folder = "experiment_results"
        os.makedirs(folder, exist_ok=True)

        # 20250617_131015  →  17 Jun 2025 13:10:15
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        # optional: replace blanks to avoid “  ” in filenames
        gname = graph_name.replace(" ", "_")
        aname = algorithm_name.replace(" ", "_")

        filename = f"{ts}_{gname}_{aname}.png"
        path = os.path.join(folder, filename)
        abs_path = os.path.abspath(path)

        fig.savefig(path)
        print(f"📊 Identified Densest Subgraph Graph Drawing saved to: {abs_path}")


