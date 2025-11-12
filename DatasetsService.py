from GraphLoader import GraphLoader

class DatasetsService:
    def load_datasets():
        datasets = dict()
        datasets["Douban"] = GraphLoader.load_graph("datasets/douban.txt")
        datasets["Gowalla"] = GraphLoader.load_graph("datasets/gowalla.txt")
        datasets["Brightkite"] = GraphLoader.load_graph("datasets/brightkite.txt")
        datasets["Livemocha"] = GraphLoader.load_graph("datasets/livemocha.txt")
        datasets["Hamsterster"] = GraphLoader.load_graph("datasets/hamsterster.txt")
        datasets["Catster"] = GraphLoader.load_graph("datasets/catster.txt")

        return datasets
