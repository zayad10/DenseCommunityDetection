import networkx

from AlgorithmEvaluator import AlgorithmEvaluator
from AlgorithmStrategy import AlgorithmStrategy, CharikarsGreedy, CharikarsGreedyMinHeap, GoldbergsMaxDensitySubgraph, \
    GreedyPlusPlus, GreedyPlusPlusPriorityQueue
from Datasets import Datasets
from EvaluationResultsView import AlgorithmResultsViewer


class EvaluateAlgorithms:
    def __init__(self, iterations):
        self.iterations = iterations
        pass

    def evaluate_all_on_all_datasets(self):
        datasets = Datasets()
        results = []

        # Example evaluation
        for dataset_name, dataset_graph in datasets.datasets.items():
            if dataset_name == "Hamsterster":
                print(f"\nEvaluating on dataset: {dataset_name}")

                # Test different algorithms
                algorithms = [
                    CharikarsGreedy(),
                    CharikarsGreedyMinHeap(),
                    GoldbergsMaxDensitySubgraph(),
                    GreedyPlusPlus(),
                    GreedyPlusPlusPriorityQueue()
                ]

                for algorithm in algorithms:
                    evaluator = AlgorithmEvaluator(algorithm, dataset_graph)
                    evaluator.evaluate_algorithm(algorithm, self.iterations)
                    results.append(evaluator.get_metrics_dict())
                    #algorithm.display_evaluation_results()
        return results

    def evaluate_all_on_single_dataset(self, dataset_graph, dataset_name):
        results = []

        # Example evaluation
        print(f"\nEvaluating on dataset: {dataset_name}")

        # Test different algorithms
        algorithms = [
            CharikarsGreedy(),
            CharikarsGreedyMinHeap(),
            GoldbergsMaxDensitySubgraph(),
            GreedyPlusPlus(),
            GreedyPlusPlusPriorityQueue()
        ]

        for algorithm in algorithms:
            evaluator = AlgorithmEvaluator(algorithm, dataset)
            evaluator.evaluate_algorithm(algorithm, self.iterations)
            result = evaluator.get_metrics_dict()
            AlgorithmResultsViewer.display_evaluation_results(result)
            results.append(evaluator.get_metrics_dict())
            #algorithm.display_evaluation_results()
        return results

    def evaluate_single_algorithm_on_all(self, algorithm):
        datasets = Datasets()
        results = []

        # Example evaluation
        for dataset_name, dataset_graph in datasets.datasets.items():
            print(f"\nEvaluating on dataset: {dataset_name}")

            evaluator = AlgorithmEvaluator(algorithm, dataset_graph)
            evaluator.evaluate_algorithm(algorithm, self.iterations)
            result = evaluator.get_metrics_dict()
            AlgorithmResultsViewer.display_result(result)
            results.append(evaluator.get_metrics_dict())
            #algorithm.display_evaluation_results()
        return results

    def evaluate_single_algorithm_on_single_dataset(self, algorithm, dataset_graph, dataset_name):
        results = []

        # Example evaluation
        print(f"\nEvaluating on dataset: {dataset_name}")

        evaluator = AlgorithmEvaluator(algorithm, dataset_graph)

        evaluator.evaluate_algorithm(algorithm, self.iterations)

        return evaluator.get_metrics_dict()


if __name__ == "__main__":
    datasets = Datasets()
    dataset = datasets.datasets["Hamsterster"]

    ev = EvaluateAlgorithms(15)

    #results = ev.evaluate_all_on_single_dataset(dataset)
    #result =

    results = ev.evaluate_all_on_single_dataset(dataset, "Hamsterster")
    print(len(results))
    for result in results:
        print(result.items())
        print(result.keys())
        print(result.values())
