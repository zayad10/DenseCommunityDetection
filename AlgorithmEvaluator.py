from Datasets import Datasets
from DatasetsService import DatasetsService
from AlgorithmStrategy import AlgorithmStrategy as AlgoStrat, GoldbergsMaxDensitySubgraph
import AlgorithmStrategy
import time
import tracemalloc
import psutil
import os
import networkx as nx

from EvaluationResultsView import AlgorithmResultsViewer


class AlgorithmEvaluator:
    def __init__(self, algorithm_strategy, dataset):
        self.accuracy = None
        self.identified_subgraph_nodes = None
        self.optimal_density = None
        self.optimal_nodes_overlap = None
        self.identified_subgraph_density = None
        self.identified_subgraph_size = None
        self.memory_used = None
        self.running_time = None
        self.algorithm = algorithm_strategy
        self.dataset = dataset
        self.reset_metrics()

    def reset_metrics(self):
        self.running_time = 0.0
        self.memory_used = 0.0
        self.accuracy = 0.0
        self.identified_subgraph_size = 0
        self.identified_subgraph_density = 0.0
        self.optimal_density = None
        self.identified_subgraph_nodes = set()

    def get_optimal(self):
        goldbergs_solution = AlgorithmStrategy.GoldbergsMaxDensitySubgraph()
        optimal_nodes = goldbergs_solution.apply_algorithm(self.dataset)
        self.optimal_nodes_overlap = AlgorithmEvaluator.get_similarity_with_optimal_nodes(self.identified_subgraph_nodes,optimal_nodes)

        return AlgoStrat.subgraph_density(self.dataset, optimal_nodes)

    @staticmethod
    def get_similarity_with_optimal_nodes(identified_densest_nodes, optimal_nodes):
        """Share of optimal_nodes that also appear in identified_nodes."""
        opt = set(optimal_nodes)
        if not opt:                     # avoid division-by-zero
            return 0.0
        return 100 * len(opt & set(identified_densest_nodes)) / len(opt)

    def evaluate_algorithm(self, algorithm_strategy, iterations=None):
        """Evaluate an algorithm strategy and record all metrics"""
        self.reset_metrics()

        # Start memory tracking
        tracemalloc.start()
        snapshot_before = tracemalloc.take_snapshot()

        process = psutil.Process(os.getpid())
        memory_before = process.memory_full_info().uss / 1024 / 1024  # MB

        # Start timing
        start_time = time.perf_counter()

        # Execute the algorithm
        try:
            if hasattr(algorithm_strategy, 'apply_algorithm'):
                AlgorithmResultsViewer.display_algorithm_and_dataset(algorithm_strategy, self.dataset)
                if (type(algorithm_strategy) in [
                    AlgorithmStrategy.GreedyPlusPlus,
                    AlgorithmStrategy.GreedyPlusPlusPriorityQueue
                ] and iterations is not None):
                    self.identified_subgraph_nodes = algorithm_strategy.apply_algorithm(
                        self.dataset, iterations
                    )
                else:
                    self.identified_subgraph_nodes = algorithm_strategy.apply_algorithm(
                        self.dataset
                    )
            else:
                raise AttributeError("Algorithm strategy must have apply_algorithm method")

        except Exception as e:
            print(f"Error executing algorithm: {e}")
            self.identified_subgraph_nodes = set()

        # Take final snapshot
        snapshot_after = tracemalloc.take_snapshot()

        # Stop timing
        end_time = time.perf_counter()
        self.running_time = end_time - start_time

        # Calculate cumulative memory allocations from tracemalloc
        stats = snapshot_after.compare_to(snapshot_before, 'lineno')
        total_allocated = sum(stat.size_diff for stat in stats if stat.size_diff > 0)
        tracemalloc_usage = total_allocated / 1024 / 1024  # Convert to MB

        # Calculate USS memory usage from psutil
        memory_after = process.memory_full_info().uss / 1024 / 1024  # MB
        uss_usage = memory_after - memory_before

        # Use the higher of the two memory measurements
        self.memory_used = max(tracemalloc_usage, uss_usage)

        tracemalloc.stop()

        # Calculate metrics
        self.identified_subgraph_size = len(self.identified_subgraph_nodes)
        self.identified_subgraph_density = AlgoStrat.subgraph_density(
            self.dataset, self.identified_subgraph_nodes
        )

        self.optimal_density = self.get_optimal()

        # Calculate accuracy
        self.calculate_accuracy()

    def calculate_accuracy(self):
        """Calculate accuracy as the ratio of found density to optimal density"""
        try:
            self.accuracy = (((self.identified_subgraph_density / self.optimal_density) * 100) + self.optimal_nodes_overlap) / 2.0

        except Exception as e:
            print(f"Error calculating algorithm accuracy: {e}")
            self.accuracy = 0.0

    def get_metrics_dict(self):
        return {
            'algorithm': type(self.algorithm).__name__,
            'running_time': self.running_time,
            'memory_used': self.memory_used,
            'identified_subgraph_size': self.identified_subgraph_size,
            'identified_subgraph_density': self.identified_subgraph_density,
            'optimal_density': self.optimal_density,
            'overlap_with_optimal_subgraph': self.optimal_nodes_overlap,
            'accuracy': self.accuracy,
            '#_dataset_nodes': self.dataset.number_of_nodes(),
            '#_dataset_edges': self.dataset.number_of_edges()
        }


if __name__ == "__main__":
    # Load datasets
    datasets = Datasets()

    # Example evaluation
    for dataset_name, dataset_graph in datasets.datasets.items():
        if dataset_name == "Hamsterster":
            print(f"\nEvaluating on dataset: {dataset_name}")

            # Test different algorithms
            algorithms = [
                AlgorithmStrategy.CharikarsGreedy(),
                AlgorithmStrategy.CharikarsGreedyFibonacciHeap(),
                AlgorithmStrategy.GoldbergsMaxDensitySubgraph(),
                AlgorithmStrategy.GreedyPlusPlus(),
                AlgorithmStrategy.GreedyPlusPlusPriorityQueue()
            ]

            for algorithm in algorithms:
                evaluator = AlgorithmEvaluator(algorithm, dataset_graph)
                evaluator.evaluate_algorithm(algorithm, iterations=15)
                AlgorithmResultsViewer.display_evaluation_results(evaluator)
                AlgorithmResultsViewer.draw_densest_component_zoom(dataset_graph, evaluator.identified_subgraph_nodes, dataset_name, algorithm.algorithm_name)
                #evaluator.display_evaluation_results()