import sys
from Datasets import Datasets
from DatasetsService import DatasetsService
import AlgorithmStrategy
from AlgorithmEvaluator import AlgorithmEvaluator
from EvaluationResultsView import AlgorithmResultsViewer


class UI:
    def __init__(self):
        self.welcome_message = ("👋 Welcome user, to the Dense Subgraph Discovery Algorithm for Community Detection Evaluator.\n"
                                "Please interact with the main menu.")
        self.datasets = Datasets()
        self.available_algorithms = {
            '1': ('Charikar\'s Greedy', AlgorithmStrategy.CharikarsGreedy),
            '2': ('Charikar\'s Greedy with Fibonacci Heap', AlgorithmStrategy.CharikarsGreedyFibonacciHeap),
            '3': ('Goldberg\'s Maximum Density Subgraph', AlgorithmStrategy.GoldbergsMaxDensitySubgraph),
            '4': ('Greedy++ (Flowless)', AlgorithmStrategy.GreedyPlusPlus),
            '5': ('Greedy++ with Priority Queue (Flowless)', AlgorithmStrategy.GreedyPlusPlusPriorityQueue)
        }
        self.selected_datasets = []
        self.selected_algorithms = []
        self.iterations = 10

    def display_welcome_message(self):
        print("\n" + "=" * 60)
        print(self.welcome_message)
        print("=" * 60)

    def display_main_menu(self):
        print("\n🏠 MAIN MENU")
        print("1. Select Datasets")
        print("2. Select Algorithms")
        print("3. Configure Selected Algorithm Parameters")
        print("4. Run Currently Configured Experiment")
        print("5. View Current Experiment Configuration")
        print("6. Run Quick Experiment (All algorithms ran once on each dataset)")
        print("7. Exit")
        print("-" * 40)

    def display_datasets_menu(self):
        print("\n📑AVAILABLE DATASETS")
        dataset_items = list(self.datasets.datasets.items())

        for i, (name, graph) in enumerate(dataset_items, 1):
            nodes = graph.number_of_nodes()
            edges = graph.number_of_edges()
            status = "✓" if name in self.selected_datasets else " "
            print(f"{i}. [{status}] {name} (Nodes: {nodes}, Edges: {edges})")

        print(f"{len(dataset_items) + 1}. Select All")
        print(f"{len(dataset_items) + 2}. ⚠ Clear Selection")
        print(f"{len(dataset_items) + 3}. ⬅ Back to Main Menu")
        print("-" * 40)

    def display_algorithms_menu(self):
        print("\n🔬 AVAILABLE ALGORITHMS")

        for key, (name, _) in self.available_algorithms.items():
            status = "✔" if key in [str(i) for i, _ in enumerate(self.selected_algorithms, 1)] else " "
            selected_index = None
            for i, (selected_key, _) in enumerate(self.selected_algorithms):
                if selected_key == key:
                    status = "✔"
                    break
            print(f"{key}. [{status}] {name}")

        print("6. Select All")
        print("7. ⚠ Clear Selection")
        print("8. ⬅ Back to Main Menu")
        print("-" * 40)

    def select_datasets(self):
        while True:
            self.display_datasets_menu()
            choice = input("Enter your choice: ").strip()

            if not choice:
                continue

            dataset_items = list(self.datasets.datasets.items())

            try:
                choice_num = int(choice)

                if 1 <= choice_num <= len(dataset_items):
                    dataset_name = dataset_items[choice_num - 1][0]
                    if dataset_name in self.selected_datasets:
                        self.selected_datasets.remove(dataset_name)
                        print(f"❌ Removed {dataset_name}")
                    else:
                        self.selected_datasets.append(dataset_name)
                        print(f"✅ Added {dataset_name}")

                elif choice_num == len(dataset_items) + 1:  # Select All
                    self.selected_datasets = [name for name, _ in dataset_items]
                    print("✅ Selected all datasets")

                elif choice_num == len(dataset_items) + 2:  # Clear Selection
                    self.selected_datasets.clear()
                    print("❌ Cleared dataset selection")

                elif choice_num == len(dataset_items) + 3:  # Back
                    break

                else:
                    print("⛔ Invalid choice")

            except ValueError:
                print("⛔ Please enter a valid number")

    def select_algorithms(self):
        while True:
            self.display_algorithms_menu()
            choice = input("Enter your choice: ").strip()

            if not choice:
                continue

            if choice in self.available_algorithms:
                # Check if already selected
                already_selected = any(key == choice for key, _ in self.selected_algorithms)

                if already_selected:
                    self.selected_algorithms = [(k, v) for k, v in self.selected_algorithms if k != choice]
                    print(f"❌ Removed {self.available_algorithms[choice][0]}")
                else:
                    self.selected_algorithms.append((choice, self.available_algorithms[choice]))
                    print(f"✅ Added {self.available_algorithms[choice][0]}")

            elif choice == "6":  # Select All
                self.selected_algorithms = [(k, v) for k, v in self.available_algorithms.items()]
                print("✅ Selected all algorithms")

            elif choice == "7":  # Clear Selection
                self.selected_algorithms.clear()
                print("❌ Cleared algorithm selection")

            elif choice == "8":  # Back
                break

            else:
                print("⛔ Invalid choice")

    def configure_parameters(self):
        print("\n⚙️  PARAMETER CONFIGURATION")
        print(f"Current iterations for Greedy++ algorithms: {self.iterations}")
        print("1. 🤔 Change iterations count")
        print("2. ⬅ Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                new_iterations = int(input(f"Enter new iterations count (current: {self.iterations}): "))
                if new_iterations > 0:
                    self.iterations = new_iterations
                    print(f"✅ Iterations set to {self.iterations}")
                else:
                    print("⛔ Iterations must be positive")
            except ValueError:
                print("⛔ Please enter a valid number")

    def view_current_selection(self):
        print("\n👁️  CURRENT SELECTION")
        print("\n📄 Selected Datasets:")
        if self.selected_datasets:
            for dataset in self.selected_datasets:
                graph = self.datasets.datasets[dataset]
                print(f"  • {dataset} (Nodes: {graph.number_of_nodes()}, Edges: {graph.number_of_edges()})")
        else:
            print(" None selected")

        print("\n🔬 Selected Algorithms:")
        if self.selected_algorithms:
            for _, (name, _) in self.selected_algorithms:
                print(f"  • {name}")
        else:
            print("  None selected")

        print(f"\n⚙️ Parameters:")
        print(f"  • Iterations (for Greedy++ algorithms): {self.iterations}")

        input("\nPress Enter to continue...")

    def run_evaluation(self):
        if not self.selected_datasets:
            print("⛔ No datasets selected. Please select datasets first.")
            return

        if not self.selected_algorithms:
            print("⛔ No algorithms selected. Please select algorithms first.")
            return

        print("\n🕵️️ STARTING EVALUATION")
        print(f"Datasets: {len(self.selected_datasets)}")
        print(f"Algorithms: {len(self.selected_algorithms)}")
        print(f"Total evaluations: {len(self.selected_datasets) * len(self.selected_algorithms)}")

        confirm = input("Do you want to proceed? (y/N): ").strip().lower()
        if confirm != 'y':
            print("⛔ Evaluation cancelled")
            return

        total_evaluations = 0

        for dataset_name in self.selected_datasets:
            dataset_graph = self.datasets.datasets[dataset_name]
            print(f"\n🔎 Evaluating on dataset: {dataset_name}")
            print("-" * 50)

            for _, (algo_name, algo_class) in self.selected_algorithms:
                total_evaluations += 1
                print(f"\n🔬 Running {algo_name}...")

                try:
                    algorithm_instance = algo_class()
                    evaluator = AlgorithmEvaluator(algorithm_instance, dataset_graph)

                    # Check if algorithm needs iterations parameter
                    if algo_class in [AlgorithmStrategy.GreedyPlusPlus, AlgorithmStrategy.GreedyPlusPlusPriorityQueue]:
                        evaluator.evaluate_algorithm(algorithm_instance, iterations=self.iterations)
                    else:
                        evaluator.evaluate_algorithm(algorithm_instance)

                    AlgorithmResultsViewer.display_evaluation_results(evaluator)

                    AlgorithmResultsViewer.draw_densest_component_zoom(
                     dataset_graph, evaluator.identified_subgraph_nodes,
                     dataset_name, algorithm_instance.algorithm_name
                    )

                except Exception as e:
                    print(f"⛔ Error evaluating {algo_name}: {e}")

        print(f"\n✅ Evaluation completed! Total Evaluations: {total_evaluations}")
        input("Press Enter to return to the main menu...")

    def run_quick_evaluation(self):
        print("\n💥 QUICK EVALUATION")
        print("This will run all algorithms on all available datasets.")

        confirm = input("Do you want to proceed? (y/N): ").strip().lower()
        if confirm != 'y':
            print("⛔ Quick evaluation cancelled")
            return

        # Temporarily save current selection
        temp_datasets = self.selected_datasets.copy()
        temp_algorithms = self.selected_algorithms.copy()

        # Select all datasets and algorithms
        self.selected_datasets = list(self.datasets.datasets.keys())
        self.selected_algorithms = [(k, v) for k, v in self.available_algorithms.items()]

        # Run evaluation
        self.run_evaluation()

        # Restore original selection
        self.selected_datasets = temp_datasets
        self.selected_algorithms = temp_algorithms

    def run(self):
        self.display_welcome_message()

        while True:
            try:
                self.display_main_menu()
                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.select_datasets()
                elif choice == "2":
                    self.select_algorithms()
                elif choice == "3":
                    self.configure_parameters()
                elif choice == "4":
                    self.run_evaluation()
                elif choice == "5":
                    self.view_current_selection()
                elif choice == "6":
                    self.run_quick_evaluation()
                elif choice == "7":
                    print("\n👋 Thank you for using the Dense Subgraph Discovery Algorithm Evaluator!")
                    sys.exit(0)
                else:
                    print("⛔ Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"⛔ An error occurred: {e}")
                input("Press Enter to continue...")
