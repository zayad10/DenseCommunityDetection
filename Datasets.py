from DatasetsService import DatasetsService


class Datasets:
    def __init__(self):
        self.datasets = DatasetsService.load_datasets()

# # Usage
# if __name__ == "__main__":
#
#     ds = Datasets()
#     print(f"Successfully loaded Douban with {ds.datasets["Douban"].number_of_nodes()} nodes, and {ds.datasets["Douban"].number_of_edges()} edges")
#     print(f"Successfully loaded Gowalla with {ds.datasets["Gowalla"].number_of_nodes()} nodes, and {ds.datasets["Gowalla"].number_of_edges()} edges")
#     print(f"Successfully loaded Brightkite with {ds.datasets["Brightkite"].number_of_nodes()} nodes, and {ds.datasets["Brightkite"].number_of_edges()} edges")
#     print(f"Successfully loaded Livemocha with {ds.datasets["Livemocha"].number_of_nodes()} nodes, and {ds.datasets["Livemocha"].number_of_edges()} edges")
#     print(f"Successfully loaded Hamsterster with {ds.datasets["Hamsterster"].number_of_nodes()} nodes, and {ds.datasets["Hamsterster"].number_of_edges()} edges")
#     print(f"Successfully loaded Catster with {ds.datasets["Catster"].number_of_nodes()} nodes, and {ds.datasets["Catster"].number_of_edges()} edges")